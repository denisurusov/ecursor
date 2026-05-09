# SSR + ADR + DDR Template Pack + Session Documentation Strategy

**Date**: 2025-05-09  
**Purpose**: Standardize how we document AI-assisted sessions and design decisions.

## Why Structured Session Summaries + Decision Records Matter

Having a consistent structure for AI sessions (SSR), Architecture Significant Requirements (ASR), and decisions (ADR/DDR) is important because:

- It creates a permanent, searchable **"why"** behind the code, not just the "what".
- Prevents knowledge loss when revisiting old work or onboarding others.
- Makes it easy to trace requirements (from prompts) → decisions → implementation.
- Turns transient AI conversations into valuable institutional knowledge.
- Improves long-term maintainability and architectural clarity.

## Templates Included in this Pack

### 1. SSR Template (`docs/templates/ssr/ssr-template.md`)
For **AI session summaries** — captures the session objective, ASRs derived from prompts, key changes, and links to any ADR/DDR decisions made during the session.

### 2. ADR Template (`docs/templates/ssr/adr-template.md`)
For **architecturally significant** decisions (technology choices, system structure, scalability, security models, data strategy, etc.).

### 3. DDR Template (`docs/templates/ssr/ddr-template.md`)
For **day-to-day design decisions** (UI patterns, code organization, API design, state management, error handling, component choices, etc.).

## Future Automation Note

**TODO / Future improvement**:  
Configure automation (Cursor `stop` hook + Python script, or GitButler + MCP) so that at the end of each significant session the AI automatically:
- Generates a well-structured SSR
- Detects important decisions and creates skeleton ADR/DDR files using the right template
- Supports switching between different templates (Nygard, MADR, Y-Statement, custom, etc.) per project

This automation should be configurable via `.cursorrules` or project settings.