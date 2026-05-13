# AI Session Documentation Strategy

**Date**: 2025-05-09  
**Purpose**: Standardize how we document AI-assisted sessions and design decisions, and automate that documentation.

## Why This Matters

Having a consistent structure for AI sessions (SSR), Architecture Significant Requirements (ASR), and decisions (ADR/DDR) is important because:

- It creates a permanent, searchable **"why"** behind the code, not just the "what".
- Prevents knowledge loss when revisiting old work or onboarding others.
- Makes it easy to trace requirements (from prompts) → decisions → implementation.
- Turns transient AI conversations into valuable institutional knowledge.
- Improves long-term maintainability and architectural clarity.

## Templates

### SSR Template (`docs/templates/ssr/ssr-template.md`)
For **AI session summaries** — captures the session objective, ASRs derived from prompts, key changes, and links to any ADR/DDR decisions made during the session.

### ADR Template (`docs/templates/ssr/adr-template.md`)
For **architecturally significant** decisions (technology choices, system structure, scalability, security models, data strategy, etc.).

### DDR Template (`docs/templates/ssr/ddr-template.md`)
For **day-to-day design decisions** (UI patterns, code organization, API design, state management, error handling, component choices, etc.).

## Automation Options

### Option 1 — GitButler + Cursor Hooks (Recommended for full automation)

GitButler has native support for Cursor hooks. It automatically creates branches per Agent session, generates smart commit messages from transcripts, and tracks AI actions.

- Highest level of automation with almost zero custom code
- Smart, context-aware commit messages
- Clean branch-per-session workflow
- Truly cross-platform (Windows, macOS, Linux)

**Effort**: Low (install GitButler + simple `hooks.json`)  
**Best for**: Heavy users or teams wanting set-and-forget traceability.

### Option 2 — Single Python Hook (Best pure cross-platform script)

One `session-summary.py` file triggered by Cursor's `stop` hook. It reads the latest `agent-transcript.jsonl`, generates a markdown summary, commits it to `docs/ai-sessions/`, and pushes.

- Single file works everywhere (no Windows vs Linux versions)
- Full control over summary quality (can even call an LLM for better summaries)
- No extra desktop apps needed

**Effort**: Medium (one Python file + `hooks.json`)  
**Best for**: Developers who prefer lightweight, code-based solutions and already use Python.

### Option 3 — Rules-Based Prompting (Zero scripts / Zero tools)

Add instructions to `.cursorrules` (or project rules) telling the Agent: "At the end of every major task, create a session summary in `docs/ai-sessions/` and tell me it's ready to commit & push."

- Zero setup and zero maintenance
- Works immediately on any machine
- No hooks, no extra tools, no Python

**Effort**: Very low  
**Trade-off**: Not fully automatic — relies on the Agent remembering and you accepting the commit.

## Recommendation

| Goal | Best option |
|---|---|
| Set-and-forget automation | **GitButler** |
| No extra desktop apps | **Python hook** |
| Quickest start today | **Rules-based** |

All three approaches store the history in your Git repo, giving you a searchable, permanent GenAI audit trail outside your local machine. The automation should be configurable via `.cursorrules` or project settings.
