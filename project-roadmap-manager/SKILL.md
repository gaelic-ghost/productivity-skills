---
name: project-roadmap-manager
description: Create and maintain a repository-root ROADMAP.md as the canonical checklist roadmap record. Use when bootstrapping a roadmap, accepting/completing plans, updating milestone scope or status, adding ticket-sized checklist work, tracking exit criteria progress, or migrating legacy table-style ROADMAP.md files to the checklist standard.
---

# Project Roadmap Manager

Maintain `ROADMAP.md` in the project root as the canonical roadmap record.

Use a checklist-first roadmap structure:

- `Vision`
- `Product principles`
- `Milestone Progress` (checkbox list)
- Per-milestone sections with `Scope`, `Tickets`, and `Exit criteria`

Preserve useful strategic appendices when present (for example `Architectural decision log`, `Risks and mitigations`, `Backlog candidates`).

## Workflow

1. Load active customization config:
   - Prefer `<skill_root>/config/customization.yaml`.
   - Fall back to `<skill_root>/config/customization.template.yaml`.
   - Apply active settings under `settings`.
   - Treat deprecated settings as compatibility hints only.
2. Identify project root and target file:
   - Use `<project_root>/ROADMAP.md`.
   - If root is ambiguous, infer from repository root.
3. Ensure `ROADMAP.md` exists:
   - If missing, create it using this skill's checklist template.
4. Detect roadmap format:
   - Checklist standard (already canonical).
   - Legacy table format (`Current Milestone` and/or `Milestones` table).
5. If legacy format is detected:
   - Auto-migrate in-place to checklist standard.
   - Preserve useful historical context without duplicate/conflicting state.
6. Classify request into event type:
   - Project bootstrap.
   - Plan acceptance/completion.
   - Milestone roadmap set or changed.
   - Milestone reached/blocked/de-scoped.
   - Roadmap reference/query.
7. Apply event rules and keep checklist sections consistent.

## Canonical ROADMAP.md Template

Use this structure when creating a new roadmap:

```markdown
# Project Roadmap

## Vision

<One paragraph describing end-state and user value.>

## Product principles

- <Principle 1>
- <Principle 2>

## Milestone Progress

- [ ] Milestone 0: Foundation (in progress)
- [ ] Milestone 1: Core delivery (not started)

## Milestone 0: Foundation

Scope:

- <Scope bullet>

Tickets:

- [ ] <Ticket-sized task>
- [ ] [P] <Parallelizable ticket-sized task>

Exit criteria:

- [ ] <Outcome check>

## Milestone 1: Core delivery

Scope:

- <Scope bullet>

Tickets:

- [ ] <Ticket-sized task>

Exit criteria:

- [ ] <Outcome check>

## Architectural decision log

### ADR-001: <Decision title>

Decision:

- <Decision>

Rationale:

- <Rationale>

Revisit trigger:

- <Trigger>

## Risks and mitigations

- Risk: <Risk>
  Mitigation: <Mitigation>

## Backlog candidates

- <Candidate item>
```

## Checklist Semantics

- Use only markdown checkboxes: `[ ]` and `[x]`.
- Use `[P]` inline marker on `Tickets` items that are parallelizable.
- Keep milestone numbering and naming deterministic within the file.
- Reflect milestone-level progress in `Milestone Progress` without overstating completion.
- Do not require target dates to exist.

## Legacy Auto-Migration Rules

Detect legacy format when either is present:

- `## Current Milestone`
- `## Milestones` with a markdown table

Migration behavior:

1. Build checklist milestone sections from legacy milestone rows and current milestone details.
2. Convert legacy status signals into:
   - `Milestone Progress` checkbox state and concise note.
   - Milestone-local status context where needed.
3. Preserve useful historical text from `Plan History` and `Change Log` under retained sections when non-conflicting, or under `## Legacy Notes` if consolidation is required.
4. Remove superseded legacy table/current-milestone sections after successful migration.
5. Never leave duplicate conflicting state across old and new models.

## Event Handling Rules

### Project Bootstrap

- Create `ROADMAP.md` if absent.
- Initialize checklist-standard sections in canonical order.
- Add at least one milestone with `Scope`, `Tickets`, and `Exit criteria`.

### Plan Acceptance or Completion

- Update affected milestone sections (`Scope`, `Tickets`, `Exit criteria`).
- Update `Milestone Progress` to match accepted/completed state.
- Keep edits bounded to roadmap-relevant sections.

### Milestone Roadmap Set/Update

- Update existing milestone by heading if present.
- Add new milestone section only when no matching section exists.
- Avoid duplicate milestone headings and contradictory checklist states.
- Keep ticket items ticket-sized and use `[P]` only when meaningful.

### Milestone Reached/Changed

- Update milestone-local checklists and `Milestone Progress` together.
- Keep completed milestones marked consistently across top progress and section outcomes.

### Roadmap Reference Requests

- Point explicitly to `<project_root>/ROADMAP.md`.
- Cite section names from checklist model (`Milestone Progress`, specific milestone sections, `Tickets`, `Exit criteria`, or preserved strategic appendices).
- If missing, create it first, then reference it.

## Customization Workflow

When user asks to customize this skill:

1. Read active config from `config/customization.yaml`; if missing, use `config/customization.template.yaml`.
2. Confirm behavior choices for active checklist-era knobs:
   - `statusValues`
   - `planHistoryVerbosity`
   - `changeLogVerbosity`
3. If legacy knobs appear, treat them as compatibility-only and report deprecation behavior.
4. Propose 2-4 option bundles with one recommended default.
5. Create or update `config/customization.yaml` from template and set:
   - `schemaVersion: 1`
   - `isCustomized: true`
   - `profile: <selected-profile>`
6. Validate with a dry-run roadmap update and report changed keys plus behavior deltas.

## Customization Reference

- Detailed knobs and examples: `references/customization.md`
- YAML schema and allowed values: `references/config-schema.md`

## Quality Bar

- Preserve useful existing roadmap content.
- Keep edits minimal and deterministic.
- Ensure every milestone section includes both `Tickets` and `Exit criteria`.
- Keep `Milestone Progress` aligned with milestone section state.
- Do not require target-date fields.
- If legacy format was present, complete migration without leaving conflicting duplicated structures.

## Automation Templates

Use `$project-roadmap-manager` inside automation prompts so Codex consistently applies checklist roadmap update rules.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including bounded-edit guardrails and placeholders, use:
- `references/automation-prompts.md`

## References

- Automation prompt templates: `references/automation-prompts.md`
- Customization guide: `references/customization.md`
- Customization schema: `references/config-schema.md`
