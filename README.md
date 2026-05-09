# ecursor

A working space to **explore, design, and prototype** practices and tooling that help teams use **Cursor** in **enterprise** settings: governance, traceability, repeatable workflows, and alignment with how organizations ship and review software.

This repository is intentionally experimental. Artifacts here are hypotheses and sketches—not a product roadmap for Cursor.

## What lives here

| Area | Purpose |
|------|---------|
| [`docs/proposals/`](docs/proposals/) | Written explorations of problems and approaches (e.g. AI session tracking, documentation patterns). |
| [`docs/decisions/`](docs/decisions/) | Architecture decisions (ADRs) and lighter design notes (DDRs) once something is chosen. |
| [`docs/ai-sessions/`](docs/ai-sessions/) | Session summaries (SSRs) from agent work, when hooks or rules generate them. |
| [`docs/templates/`](docs/templates/) | Reusable templates for SSRs, ADRs, and DDRs. |
| [`.cursor/`](.cursor/) | Project rules and hooks that encode conventions and light automation for this repo. |
| [`src/`](src/) | Small prototypes or samples when code is needed to try an idea. |

## Session documentation (SSR) proposal

The [SSR proposal](docs/proposals/SSR/summary.md) explains why structured **session summaries (SSR)**, **ADRs**, and **DDRs** matter for AI-assisted work, what the template pack covers, and ideas for future automation. For more detail on the approach, see [docs/proposals/SSR/approach.md](docs/proposals/SSR/approach.md)