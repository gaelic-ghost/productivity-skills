# Repo Reality Audit

This document is maintainer-only. It defines how to verify that repo docs match the code and that skill runtime resources stay self-contained.

## Source Of Truth Order

Use this order when checking any behavior claim:

1. skill `scripts/*` or the actual MCP/tool sequence
2. skill `agents/openai.yaml`
3. skill `SKILL.md`
4. skill-local `references/*`
5. repo-level maintainer docs in `docs/maintainers/*`

If two layers disagree, fix the lower-trust layer or narrow its claims.

## Audience Boundaries

- `README.md` is user-facing only.
- `AGENTS.md` is repo-maintainer guidance only.
- Installed skills must be understandable from their own directories.
- Skill runtime docs must not depend on `../docs/...`.
- Repo-level maintainer docs may describe patterns and audits, but they are not part of installed skill operation.

## Current Repo Reality

### Skill Runtime Surfaces

- `project-docs-maintainer`
  - Scripts: `scripts/skills_readme_maintenance.py`, `scripts/roadmap_alignment_maintainer.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `project-roadmap-maintainer`
  - Redirect-only compatibility surface
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `project-skills-orchestrator-agent`
  - Metadata-only routing skill with `references/skill-routing-matrix.md`
- `project-workspace-cleaner`
  - Script: `scripts/scan_workspace_cleanup.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `things-digest-generator`
  - Script: `scripts/build_digest.py`
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`
- `things-reminders-manager`
  - MCP sequence is the source of truth
  - Metadata: `agents/openai.yaml`
  - Runtime docs: `SKILL.md`, `references/*`

### Maintainer Surfaces

- `docs/maintainers/workflow-atlas.md`
- `docs/maintainers/documentation-rubric.md`
- `docs/maintainers/documentation-tracker.md`
- `docs/maintainers/agents-standards-snippets.md`

## Audit Procedure

For each skill:

1. Read the implementation source of truth.
2. Check `agents/openai.yaml` for trigger and output wording.
3. Check `SKILL.md` for inputs, workflow, output contract, and guardrails.
4. Check every referenced file for stale, orphaned, or cross-boundary guidance.
5. Confirm every referenced path exists.

Required checks:

- inputs match actual accepted flags or actual MCP/tool inputs
- workflow steps match real implementation order
- output contracts match text and JSON emitted by code
- exact phrases like `No findings.` match actual output
- blocked/error branches are documented only if they really exist
- compatibility aliases stay secondary

## Current Invariants

- `project-workspace-cleaner` reserves exact `No findings.` for complete clean runs with no skipped paths.
- `things-digest-generator` uses deterministic `Input error:` failures for missing or invalid JSON fallback inputs.
- `project-roadmap-maintainer` is compatibility-only and never owns roadmap behavior.
- `project-docs-maintainer` is the canonical owner of `skills_readme_maintenance` and `roadmap_maintenance`.
