# README Workflow Divergence Report

Date: 2026-03-05
Scope: `productivity-skills` root README plus `project-docs-maintainer` README-maintenance references and checker behavior.
Status: aligned to the canonical `skills_readme_maintenance` naming and current section schema.

## Current Alignment State

- Canonical README maintenance name: `skills_readme_maintenance`
- Legacy compatibility alias: `skills_readme_alignment`
  - retained for compatibility only
  - no longer treated as a primary path in repo docs
- Root `README.md` now emphasizes canonical skills first and keeps compatibility-only surfaces brief.

## Implemented Baseline

- Required public-curated README sections and TOC rules are aligned with the current checker contract.
- Discoverability rules and install command patterns match the current `npx skills add ...` syntax.
- Shared `AGENTS.md` snippet guidance now lives in `docs/agents-standards-snippets.md` instead of duplicated per-skill references.
- `project-docs-maintainer` remains the canonical owner of README maintenance and roadmap maintenance behavior.

## Validation Command

```bash
uv run python project-docs-maintainer/scripts/skills_readme_maintenance.py \
  --workspace /Users/galew/Workspace \
  --repo-glob 'productivity-skills' \
  --print-md \
  --print-json
```

## Expected Clean Result

- `repos_with_issues`: `0`
- `schema_violations`: `0`
- `command_integrity_issues`: `0`

## Remaining Compatibility Notes

- Keep the legacy alias accepted in maintenance surfaces that must preserve backward compatibility.
- Do not reintroduce alias-first wording in `README.md`, `SKILL.md`, or `agents/openai.yaml`.
