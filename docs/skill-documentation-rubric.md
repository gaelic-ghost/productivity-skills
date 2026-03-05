# Skill Documentation Rubric

Use this rubric for both cleanup passes across this repository.

## Pass 1: Accurate and Current

Check each doc surface against the current repository state.

- Trigger clarity: `SKILL.md` frontmatter and `agents/openai.yaml` describe the same capability and trigger conditions.
- Canonical naming: mode names, script names, config paths, and compatibility notes match the current repo.
- Command accuracy: every documented command, flag, and file path exists.
- Contract accuracy: documented outputs match the actual report fields, section order, or mutation result shape.
- Deprecation accuracy: compatibility paths are clearly labeled as non-canonical and redirect to the right place.
- Reference integrity: every referenced file exists and is the right source for the claim it supports.

## Pass 2: Simplified and Improved

Refactor docs so the primary path is easy to follow without chasing branches.

- Single-path workflow: `SKILL.md` has one clear main path, not a menu of competing flows.
- Section consistency: prefer `Inputs`, `Workflow`, `Output Contract`, `Guardrails`, and `References`.
- Minimal primary surface: keep customization, automation templates, schemas, and examples in references unless they are first-class runtime behavior.
- Naming consistency: use the same term everywhere for the same thing.
- Input contract clarity: state required inputs, optional overrides, defaults, and config precedence without ambiguity.
- Output contract clarity: state exactly what the user gets back and when exact clean-run text such as `No findings.` is valid.
- Reference modularity: shared material lives in one canonical source; skill-local references only hold skill-specific detail.
- Deprecated-path handling: compatibility notes stay brief and never overshadow the canonical path.

## Reviewer Questions

Ask these questions before closing a doc surface.

- Could another agent execute the skill correctly by reading `SKILL.md` first and references second?
- Is the first workflow the canonical workflow?
- Are any sections duplicated elsewhere without adding clarity?
- Does the file force the reader to choose among crossed paths that should instead be hidden behind one primary path?
- Would a grep for an old alias or deprecated mode still find primary-surface wording that should now be compatibility-only?

## Completion Rule

Mark a doc surface complete only when:

- Pass 1 has no known drift against scripts, config files, or current references.
- Pass 2 leaves one clear primary workflow and removes unnecessary duplication from the main path.
