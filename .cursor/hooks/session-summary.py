#!/usr/bin/env python3
"""Cursor `stop` hook: draft an SSR markdown file from the latest agent transcript.

Reads stdin (stop-hook JSON) to avoid blocking the pipe, then writes under
docs/ai-sessions/. Requires GitButler CLI (`but`) only if you use the second
stop hook; this script only needs Python.

Optional env:
  SSR_AUTO_COMMIT=1  — git add + commit the new SSR (never pushes).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path


def _read_stop_payload() -> dict:
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return {}
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _find_git_root(start: Path) -> Path | None:
    for p in [start, *start.parents]:
        if (p / ".git").is_dir():
            return p
    return None


def _workspace_slug(root: Path) -> str:
    s = str(root.resolve())
    if len(s) >= 2 and s[1] == ":":
        drive = s[0].lower()
        rest = s[2:].replace("\\", "-").replace("/", "-")
        rest = re.sub(r"-+", "-", rest).strip("-")
        return f"{drive}-{rest}" if rest else drive
    return re.sub(r"-+", "-", s.replace("/", "-").strip("-"))


def _transcripts_root_for_project(project_root: Path) -> Path | None:
    projects = Path.home() / ".cursor" / "projects"
    if not projects.is_dir():
        return None
    slug = _workspace_slug(project_root)
    direct = projects / slug / "agent-transcripts"
    if direct.is_dir():
        return direct
    needle = project_root.name.lower()
    for child in projects.iterdir():
        if not child.is_dir():
            continue
        if needle not in child.name.lower():
            continue
        cand = child / "agent-transcripts"
        if cand.is_dir():
            return cand
    return None


def _latest_transcript(transcripts_root: Path) -> Path | None:
    files = list(transcripts_root.rglob("*.jsonl"))
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def _strip_user_query(text: str) -> str:
    m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def _iter_content_blocks(message: dict):
    content = message.get("content")
    if not isinstance(content, list):
        return
    for block in content:
        if isinstance(block, dict):
            yield block


def _parse_transcript(path: Path) -> tuple[list[str], OrderedDict[str, set[str]], list[str]]:
    """Returns (user_prompts, rel_files_by_action, shell_commands)."""
    project_root = _find_git_root(Path.cwd())
    if not project_root:
        project_root = Path.cwd()

    user_prompts: list[str] = []
    files_by_action: OrderedDict[str, set[str]] = OrderedDict()
    shell_commands: list[str] = []

    def add_file(action: str, abs_path: str) -> None:
        try:
            p = Path(abs_path)
            if not p.is_absolute():
                rel = abs_path
            else:
                try:
                    rel = str(p.resolve().relative_to(project_root.resolve()))
                except ValueError:
                    rel = abs_path
        except OSError:
            rel = abs_path
        rel = rel.replace("\\", "/")
        files_by_action.setdefault(action, set()).add(rel)

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        role = row.get("role")
        msg = row.get("message") or {}
        if role == "user":
            for block in _iter_content_blocks(msg):
                if block.get("type") != "text":
                    continue
                text = block.get("text") or ""
                if "user_query" in text or role == "user":
                    q = _strip_user_query(text)
                    if q and (not user_prompts or q != user_prompts[-1]):
                        user_prompts.append(q)
        if role == "assistant":
            for block in _iter_content_blocks(msg):
                if block.get("type") != "tool_use":
                    continue
                name = block.get("name") or ""
                inp = block.get("input") or {}
                if name in ("Write", "StrReplace", "Delete"):
                    fp = inp.get("path") or inp.get("file_path")
                    if isinstance(fp, str):
                        add_file("Modified" if name != "Delete" else "Deleted", fp)
                elif name == "Read":
                    fp = inp.get("path")
                    if isinstance(fp, str):
                        add_file("Read", fp)
                elif name == "Glob":
                    td = inp.get("target_directory")
                    gp = inp.get("glob_pattern") or ""
                    if isinstance(td, str):
                        try:
                            p = Path(td)
                            if p.is_absolute():
                                rel = str(p.resolve().relative_to(project_root.resolve()))
                            else:
                                rel = td
                        except (ValueError, OSError):
                            rel = td
                        rel = rel.replace("\\", "/")
                        label = f"{rel} ({gp})" if gp else rel
                        files_by_action.setdefault("Glob", set()).add(label)
                elif name == "Shell":
                    cmd = inp.get("command")
                    if isinstance(cmd, str) and cmd.strip():
                        shell_commands.append(cmd.strip())

    return user_prompts, files_by_action, shell_commands


def _write_ssr(
    out_dir: Path,
    transcript_path: Path,
    status: str,
    prompts: list[str],
    files_by_action: OrderedDict[str, set[str]],
    shell_commands: list[str],
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    stem = transcript_path.parent.name[:8]
    out = out_dir / f"{ts[:10]}-cursor-{stem}.md"

    objective = prompts[0] if prompts else "(see transcript)"
    duration = "~unknown"

    lines: list[str] = [
        "# AI Session Summary Record (SSR)",
        "",
        f"**Session ID**: cursor-{stem}",
        f"**Date**: {ts[:10]} (UTC)",
        f"**Duration**: {duration}",
        f"**Agent stop status**: {status}",
        f"**Transcript**: `{transcript_path}`",
        f"**Objective**: {objective}",
        "",
        "## Architecture Significant Requirements (ASRs)",
        "",
        "| ID | Requirement (ASR) | Related Prompt |",
        "|----|-------------------|----------------|",
    ]
    for i, p in enumerate(prompts[:12], start=1):
        safe = p.replace("|", "\\|").replace("\n", " ")[:200]
        lines.append(f"| ASR-{i:02d} | {safe} | prompt #{i} |")
    if not prompts:
        lines.append("| ASR-01 | (none parsed) | — |")

    lines += [
        "",
        "## Tasks Completed",
        "",
        "- [ ] *(fill in after review — or edit checklist during the session)*",
        "",
        "## Key Changes",
        "",
        "| File/Path | Type | Description |",
        "|-----------|------|-------------|",
    ]
    for action, paths in files_by_action.items():
        for fp in sorted(paths):
            desc = ""
            lines.append(f"| `{fp}` | {action} | {desc} |")
    if not any(files_by_action.values()):
        lines.append("| — | — | *(no file paths parsed from transcript)* |")

    lines += [
        "",
        "## Architecture & Design Decisions",
        "",
        "| ID | Title | Type | Status | Summary |",
        "|----|-------|------|--------|---------|",
        "| — | — | — | — | *(link ADR/DDR under docs/decisions/ when applicable)* |",
        "",
        "## Commands Executed",
        "",
        "```bash",
    ]
    if shell_commands:
        lines.extend(shell_commands[-50:])
    else:
        lines.append("# (none parsed from transcript)")
    lines.append("```")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def _maybe_git_commit(project_root: Path, ssr_path: Path) -> None:
    if os.environ.get("SSR_AUTO_COMMIT", "").strip() not in ("1", "true", "yes"):
        return
    try:
        subprocess.run(
            ["git", "add", str(ssr_path.relative_to(project_root))],
            cwd=project_root,
            check=False,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"docs(ai): add session summary {ssr_path.name}"],
            cwd=project_root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        pass


def main() -> int:
    payload = _read_stop_payload()
    status = payload.get("status", "unknown")

    project_root = _find_git_root(Path.cwd())
    if not project_root:
        project_root = Path.cwd()

    troot = _transcripts_root_for_project(project_root)
    if not troot:
        print("[session-summary] no agent-transcripts dir found", file=sys.stderr)
        return 0

    transcript = _latest_transcript(troot)
    if not transcript:
        print("[session-summary] no .jsonl transcript found", file=sys.stderr)
        return 0

    prompts, files, shells = _parse_transcript(transcript)
    out_dir = project_root / "docs" / "ai-sessions"
    ssr_path = _write_ssr(out_dir, transcript, status, prompts, files, shells)
    print(f"[session-summary] wrote {ssr_path.relative_to(project_root)}", file=sys.stderr)
    _maybe_git_commit(project_root, ssr_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
