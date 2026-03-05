---
name: project-roadmap-maintainer
description: Compatibility-only redirect for legacy roadmap maintenance invocations. Use only when a prompt explicitly names `project-roadmap-maintainer` or depends on that legacy surface, then redirect to `project-docs-maintainer` with `mode=roadmap_maintenance`.
---

# Project Roadmap Maintainer

This skill is not a canonical maintainer. It exists only to preserve legacy prompts.

## Inputs

- A legacy roadmap request that explicitly targets `$project-roadmap-maintainer`
- Preserve:
  - project root
  - roadmap path
  - run intent (`check-only` or `apply`)

## Workflow

1. Acknowledge that this is a compatibility-only invocation.
2. Redirect immediately to `$project-docs-maintainer` with `mode=roadmap_maintenance`.
3. Preserve the original target path and run intent.
4. Hand off to the canonical roadmap references for behavior details.

## Output Contract

- Return a redirect, not an independent roadmap workflow.
- The redirect must state:
  - canonical skill: `$project-docs-maintainer`
  - canonical mode: `roadmap_maintenance`
  - preserved run intent and target path

## Guardrails

- Do not present this skill as the owner of roadmap maintenance behavior.
- Do not duplicate roadmap rules or schemas here.
- Keep compatibility wording brief.

## References

- `../project-docs-maintainer/SKILL.md`
- `../project-docs-maintainer/references/roadmap-automation-prompts.md`
- `../project-docs-maintainer/references/roadmap-config-schema.md`
- `../project-docs-maintainer/references/roadmap-customization.md`
