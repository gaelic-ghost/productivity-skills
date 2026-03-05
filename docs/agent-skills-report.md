# Agent Skills Report

Date: 2026-03-05

This report reflects the canonical post-cleanup documentation model for this repository: concise `SKILL.md` files, shared cross-cutting snippet guidance in `docs/agents-standards-snippets.md`, and compatibility-only paths kept brief.

## Repo-Wide Standards

- Primary skill docs use the same core sections: `Inputs`, `Workflow`, `Output Contract`, `Guardrails`, and `References`.
- `SKILL.md` files keep the main runtime path only; customization, schemas, and automation prompt templates live in `references/`.
- Canonical names are promoted everywhere; compatibility aliases and deprecated shims are documented only where needed to preserve legacy prompts.

## Skills At A Glance

| Skill | Canonical role | Primary output | Mutation profile |
| --- | --- | --- | --- |
| `project-docs-maintainer` | Canonical maintainer for `*-skills` README drift and checklist roadmap maintenance | Markdown + JSON audit/apply report | `bounded-write` |
| `project-roadmap-maintainer` | Compatibility-only redirect for legacy roadmap requests | Redirect to `project-docs-maintainer` roadmap mode | `read-only` |
| `project-skills-orchestrator-agent` | Front-door router to the right skill | `Selected Skill`, `Why`, `Install (if needed)`, `Next Prompt` | `read-only` |
| `project-workspace-cleaner` | Read-only workspace cleanup audit | Ranked findings plus repo summary | `read-only` |
| `things-digest-generator` | Things planning digest builder | Ordered markdown digest sections | `read-only` |
| `things-reminders-manager` | Update-first Things reminder mutation flow | Deterministic reminder result with absolute schedule | `mutation-capable` |

## Canonical Skill Notes

### `project-docs-maintainer`

- Primary modes: `skills_readme_maintenance` and `roadmap_maintenance`
- Clean run contract: exact `No findings.`
- Canonical references:
  - `project-docs-maintainer/references/output-contract.md`
  - `project-docs-maintainer/references/skills-readme-maintenance-automation-prompts.md`
  - `project-docs-maintainer/references/roadmap-automation-prompts.md`

### `project-roadmap-maintainer`

- Compatibility surface only
- Never owns roadmap behavior independently
- Always redirects to `$project-docs-maintainer` with `mode=roadmap_maintenance`

### `project-skills-orchestrator-agent`

- Selects one primary skill by default
- Prefers canonical skills over compatibility shims
- Uses the exact install command shape:
  - `npx skills add gaelic-ghost/productivity-skills --skill <skill-name>`

### `project-workspace-cleaner`

- Config precedence:
  1. CLI flags
  2. `config/customization.yaml`
  3. `config/customization.template.yaml`
  4. script defaults
- Per-finding fields:
  - `severity`
  - `score`
  - `repo`
  - `directory`
  - `category`
  - `size_human`
  - `why_flagged`
  - `suggested_cleanup`

### `things-digest-generator`

- Prefers Things MCP reads first and can fall back to JSON exports
- Canonical digest sections:
  - `Snapshot`
  - `Recently Active`
  - `Week/Weekend Ahead`
  - `Suggestions`
- Optional `Executive Summary` appears only when `outputStyle=executive`

### `things-reminders-manager`

- Uses update-first duplicate handling
- Resolves relative dates against local current date/time before mutation
- Deterministic result fields:
  - `action`
  - `task title`
  - `normalized absolute schedule`
  - `blockers`, when present

## Shared References

- Shared `AGENTS.md` snippets: `docs/agents-standards-snippets.md`
- Documentation review rubric: `docs/skill-documentation-rubric.md`
- Cleanup tracker: `docs/skill-documentation-tracker.md`
- Workflow atlas: `docs/skill-workflow-atlas.md`
