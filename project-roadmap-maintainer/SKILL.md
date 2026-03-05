---
name: project-roadmap-maintainer
description: Deprecated compatibility shim for roadmap maintenance. Redirects users to project-docs-maintainer roadmap mode while preserving existing invocation/install compatibility.
---

# Project Roadmap Maintainer (Deprecated Compatibility Shim)

This skill remains available for compatibility during a deprecation cycle.

Canonical roadmap behavior now lives in:

- `$project-docs-maintainer` with `mode=roadmap_maintenance`

## Compatibility Workflow

1. Acknowledge compatibility invocation.
2. Redirect to canonical mode with equivalent intent:
   - `Use $project-docs-maintainer with mode=roadmap_maintenance ...`
3. Preserve user intent (`check-only` or `apply`) and target paths.
4. Do not claim this shim is the canonical owner.

## Redirect Examples

- Legacy request: `Use $project-roadmap-maintainer to check roadmap consistency.`
- Redirected request: `Use $project-docs-maintainer with mode=roadmap_maintenance and --run-mode check-only ...`

- Legacy request: `Use $project-roadmap-maintainer to migrate this roadmap.`
- Redirected request: `Use $project-docs-maintainer with mode=roadmap_maintenance and --run-mode apply ...`

## References

- `../project-docs-maintainer/SKILL.md`
- `../project-docs-maintainer/references/roadmap-automation-prompts.md`
- `../project-docs-maintainer/references/roadmap-config-schema.md`
- `../project-docs-maintainer/references/roadmap-customization.md`
