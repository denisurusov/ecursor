# Templates

Canonical home for all reusable doc templates in this repo.

Templates are organized by family in subfolders so new categories can be added without crowding the root.

## Current families

| Family | Path | Purpose |
|--------|------|---------|
| SSR / ADR / DDR | [`ssr/`](./ssr/) | AI session summaries and architecture/design decision records. See [`docs/proposals/SSR/`](../proposals/SSR/) for the rationale behind these templates. |

## Adding a new template family

1. Create a new subfolder under `docs/templates/` (e.g. `rfcs/`, `runbooks/`).
2. Add the template files inside it, named `<kind>-template.md`.
3. Add a row to the table above pointing at the new folder.
4. If a Cursor rule, hook, or other automation should reference it, update those references too (search the repo for `docs/templates/`).

## Conventions

- One canonical copy per template — never duplicate templates into proposal or example folders. Proposals can link to a template, not copy it.
- Filled-in instances live elsewhere (e.g. ADRs/DDRs in `docs/decisions/`, SSRs in `docs/ai-sessions/`).
