---
name: project-docs-maintainer
description: Audit and maintain project documentation alignment plus checklist roadmap maintenance with a deterministic two-pass workflow. Use when repository docs drift from tooling/manifests, when *-skills README standards need profile-aware alignment, when roadmap checklists require migration/normalization, or when you need Markdown plus JSON reports with optional bounded fixes.
---

# Project Docs Maintainer

Run documentation maintenance in explicit modes so behavior stays deterministic and bounded.

## Modes

- `workspace_docs_alignment`: general repository documentation drift checks and safe fixes.
- `skills_readme_alignment`: profile-aware README standards checks and safe fixes for `*-skills` repositories.
- `roadmap_maintenance`: checklist-style `ROADMAP.md` validation, migration, and bounded updates.

## Inputs

Pass runtime inputs from the calling prompt:

- `--mode <workspace_docs_alignment|skills_readme_alignment>`
- `--workspace <path>`
- Optional `--exclude <path>` (repeatable)
- Optional mode-specific flags shown below
- For roadmap mode: `--project-root <path>`, optional `--roadmap-path <path>`, and `--run-mode <check-only|apply>`.

## Workflow

1. Choose mode based on user intent.
2. Run pass 1 audit.
3. Review issue categories and impacted repositories.
4. If requested and safe, run pass 2 with `--apply-fixes`.
5. Re-check touched repositories and report Markdown plus JSON results.
6. For roadmap requests, run roadmap check-only or apply workflows using bounded `ROADMAP.md` edits.

## Commands

`workspace_docs_alignment` audit:

```bash
uv run python scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --print-md \
  --print-json
```

`workspace_docs_alignment` audit + fixes:

```bash
uv run python scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --apply-fixes \
  --md-out /tmp/docs-alignment-report.md \
  --json-out /tmp/docs-alignment-report.json
```

`skills_readme_alignment` audit:

```bash
uv run python scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --print-md \
  --print-json
```

`skills_readme_alignment` audit + fixes:

```bash
uv run python scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --apply-fixes \
  --md-out /tmp/readme-alignment-report.md \
  --json-out /tmp/readme-alignment-report.json
```

`roadmap_maintenance` check-only:

```bash
uv run python scripts/roadmap_alignment_maintainer.py \
  --project-root ~/Workspace/my-project \
  --run-mode check-only \
  --print-md \
  --print-json
```

`roadmap_maintenance` apply:

```bash
uv run python scripts/roadmap_alignment_maintainer.py \
  --project-root ~/Workspace/my-project \
  --run-mode apply \
  --md-out /tmp/roadmap-alignment-report.md \
  --json-out /tmp/roadmap-alignment-report.json
```

## Safety Rules

- Never commit changes automatically.
- Edit documentation files only.
- Never edit source code, manifests, lockfiles, or CI files.
- Keep broad AGENTS rewrites out-of-scope for automated fixes.
- Allow snippet suggestion by default and only perform targeted `AGENTS.md` edits after explicit user approval.
- Apply only bounded replacements and minimal structural normalization.
- In `roadmap_maintenance` apply mode, edit only the target `ROADMAP.md` file.

## Output Contract

All modes must provide:

- Human-readable Markdown summary.
- Machine-readable JSON report.
- Clear list of touched files and remaining issues.

## AGENTS Snippets

Use local snippet source:

- `references/agents-snippets.md`

Provide snippets when users ask for reusable standards, policy templates, or cross-repo consistency guidance.

## Snippet Suggestion Workflow

1. Detect requests for reusable standards or repeated policy setup.
2. Offer relevant snippet block(s) from `references/agents-snippets.md`.
3. Specify target location in user `AGENTS.md` and minimal adaptation notes.
4. Ask for explicit confirmation before editing any `AGENTS.md`.
5. Report what was suggested and what was applied.

## Automation Templates

Use `$project-docs-maintainer` in automation prompts.

Templates:

- `references/automation-prompts.md` for `workspace_docs_alignment`
- `references/automation-prompts-skills-readme.md` for `skills_readme_alignment`
- `references/roadmap-automation-prompts.md` for `roadmap_maintenance`

## References

- `references/checks-common.md`
- `references/checks-swift.md`
- `references/checks-js-ts.md`
- `references/checks-python.md`
- `references/checks-rust.md`
- `references/fix-policies.md`
- `references/output-contract.md`
- `references/profile-model.md`
- `references/section-schema.md`
- `references/style-rules.md`
- `references/discoverability-rules.md`
- `references/verification-checklist.md`
- `references/seed-artifacts.md`
- `references/automation-prompts.md`
- `references/automation-prompts-skills-readme.md`
- `references/roadmap-automation-prompts.md`
- `references/roadmap-config-schema.md`
- `references/roadmap-customization.md`
