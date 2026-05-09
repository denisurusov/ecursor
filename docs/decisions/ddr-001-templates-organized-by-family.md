# DDR-001: Templates organized by family in subfolders

**Status**: Accepted
**Date**: 2026-05-09
**Related ASRs**: ASR-02, ASR-03 (session `2026-05-09-templates-reorg`)

## Context

The repo introduced reusable doc templates (SSR, ADR, DDR) via a proposal under `docs/proposals/SSR/`. After acceptance, the same template files ended up living in two places — `docs/proposals/SSR/` and `docs/templates/` — which was already drifting (e.g. the SSR template's date placeholder differed between the two copies). We expect more template kinds in the future (RFCs, runbooks, post-mortems, etc.), so we need a layout that:

- Keeps a single source of truth so templates can't drift.
- Makes the canonical location obvious to humans, rules, and hooks.
- Scales without crowding a single flat directory as new template families are added.
- Cleanly separates *living* templates from the *frozen* proposals that introduced them.

## Decision

We will treat `docs/templates/` as the **single canonical home** for all live, reusable templates in this repo, and organize templates into **per-family subfolders** rather than a flat directory.

Concretely:

- Live templates live only at `docs/templates/<family>/<kind>-template.md` (e.g. `docs/templates/ssr/adr-template.md`).
- A short `docs/templates/README.md` indexes the families and documents the convention for adding new ones.
- Proposals (`docs/proposals/<topic>/`) describe rationale and may *link* to templates but must never *copy* them.
- Filled-in instances of templates live elsewhere by purpose: ADRs/DDRs in `docs/decisions/`, SSRs in `docs/ai-sessions/`.
- Anything that references a template path (Cursor rules, hooks, scripts) points at `docs/templates/<family>/...`.

## Alternatives Considered

- **Flat `docs/templates/*-template.md`** → Rejected: works for a few templates but degrades quickly as families multiply (no grouping, harder discovery, no natural place for family-level READMEs or assets).
- **Templates inside each proposal folder (`docs/proposals/<topic>/`)** → Rejected: couples *living* artifacts to *frozen* proposals, guarantees drift (already observed), and forces consumers to know which proposal "owns" a given template.
- **Top-level `templates/` directory** → Rejected: pulls doc-only assets out of `docs/`, splitting documentation across two roots for no real benefit at this scale.
- **Single canonical location but pointer/symlink stubs in proposals** → Rejected: symlinks behave inconsistently across Windows/Git, and stub Markdown files re-introduce the duplication risk we're solving.

## Consequences

**Positive**

- One obvious place to look for any template, for both humans and automation.
- New template families added without touching existing ones — just a new subfolder + a row in the README.
- Proposals stay immutable historical records; live templates evolve independently.
- Eliminates the drift class of bug we already observed between the two SSR template copies.

**Negative**

- Slight indirection: paths are one segment longer (`docs/templates/ssr/adr-template.md` vs `docs/templates/adr-template.md`).
- Existing references must be updated when introduced (already done for `.cursor/rules/ai-session-documentation.mdc` and `docs/proposals/SSR/summary.md` in this session).
- Convention only — discipline (or lint/CI checks) is required to prevent future contributors from re-introducing template copies inside proposal folders.
