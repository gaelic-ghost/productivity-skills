# README vs project-docs-maintainer Alignment Report

Date: 2026-03-05
Scope: `productivity-skills` only (`README.md` and `project-docs-maintainer` references/checker behavior)
Remediation status: Implemented for `skills_readme_alignment` workflow (pilot repo).

## Scope Confirmation

- Updated workflow scope: `skills_readme_alignment` for `*-skills` repositories.
- Not changed: `workspace_docs_alignment` behavior in `docs_alignment_maintainer.py`.

## Contract Updates Implemented

### 1. Required section schema

- Removed `## Customization Workflow Matrix` from required section contract.
- Added required compact `## Table of Contents` for profiled `*-skills` README files.

### 2. TOC validation rules (new)

- TOC must be first H2.
- TOC must use top-level bullets only.
- TOC entries must follow `- [Section](#fragment)` format.
- TOC must not self-link.
- TOC entries must target existing H2 headings.
- TOC must include all H2 headings except `Table of Contents`.

### 3. Reference document alignment

- Updated:
  - `/Users/galew/Workspace/productivity-skills/project-docs-maintainer/references/section-schema.md`
  - `/Users/galew/Workspace/productivity-skills/project-docs-maintainer/references/discoverability-rules.md`
  - `/Users/galew/Workspace/productivity-skills/project-docs-maintainer/references/profile-model.md`
  - `/Users/galew/Workspace/productivity-skills/project-docs-maintainer/references/output-contract.md`
- Result: references now match implemented checker contract and output shape.

### 4. README pilot normalization (`productivity-skills`)

- Added canonical required sections and heading names.
- Added required `More resources` discoverability subsections and anchor line.
- Added base install command and de-duplicated install command patterns.
- Renamed `## Search Keywords` to canonical `## Keywords`.

## Validation Output

Read-only audit command:

```bash
uv run python project-docs-maintainer/scripts/readme_alignment_maintainer.py \
  --workspace /Users/galew/Workspace \
  --repo-glob 'productivity-skills' \
  --print-md \
  --print-json
```

Current result:

- Repos with issues: `0`
- Schema violations: `0`
- Command integrity issues: `0`

## Potential Next Actions

1. Apply same normalized contract to other public-curated `*-skills` repos (`apple-dev-skills`, `python-skills`).
2. Optionally add release-history enforcement in checker if that requirement should remain strict.
3. Keep `workspace_docs_alignment` unchanged unless separately requested.

## Validation Notes

- `workspace_docs_alignment` CLI surface is unchanged (`docs_alignment_maintainer.py --help` verified).
