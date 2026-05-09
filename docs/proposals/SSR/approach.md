# Cursor AI Session Tracking Options

**Date**: 2025-05-09  
**Goal**: Automatically (or semi-automatically) generate and commit session summaries so there is a permanent, non-local trace of what Cursor Agent / GenAI has done (prompts, impacted files, commands executed, etc.).

## 1. GitButler + Cursor Hooks (Recommended for full automation)
**Description**:  
GitButler has native support for Cursor hooks. It automatically creates branches per Agent session, generates smart commit messages from transcripts, and tracks AI actions.

**Value Proposition**:
- Highest level of automation with almost zero custom code
- Smart, context-aware commit messages
- Clean branch-per-session workflow
- Truly cross-platform (Windows, macOS, Linux)
- Professional traceability in Git history

**Effort**: Low (install GitButler + simple `hooks.json`)

**Best for**: Heavy users or teams wanting set-and-forget traceability.

## 2. Single Python Hook (Best pure cross-platform script)
**Description**:  
One `session-summary.py` file triggered by Cursor’s `stop` hook. It reads the latest `agent-transcript.jsonl`, generates a markdown summary, commits it to `docs/ai-sessions/`, and pushes.

**Value Proposition**:
- Single file works everywhere (no Windows vs Linux versions)
- Full control over summary quality (can even call an LLM for better summaries)
- No extra desktop apps needed
- Easy to extend or customize

**Effort**: Medium (one Python file + `hooks.json`)

**Best for**: Developers who prefer lightweight, code-based solutions and already use Python.

## 3. Rules-Based Prompting (Zero scripts / Zero tools)
**Description**:  
Add instructions to `.cursorrules` (or project rules) telling the Agent: “At the end of every major task, create a session summary in `docs/ai-sessions/` and tell me it’s ready to commit & push.”

**Value Proposition**:
- Zero setup and zero maintenance
- Works immediately on any machine
- No hooks, no extra tools, no Python
- Fully portable

**Effort**: Very low

**Trade-off**: Not fully automatic — relies on the Agent remembering and you accepting the commit.

## Recommendation
- **Best overall**: **GitButler** (if you’re okay installing one tool)  
- **Best no-extra-tools**: **Python hook**  
- **Quickest start**: **Rules-based**

All three approaches store the history in your Git repo, giving you searchable, permanent GenAI audit trail outside your local machine.