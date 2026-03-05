---
name: project-skills-orchestrator-agent
description: Route user requests to the best matching skill in this repository and provide install guidance when capabilities are missing. Use when users need help choosing, composing, or installing skills for roadmap management, docs maintenance, Things workflows, or workspace cleanup.
---

# Project Skills Orchestrator Agent

Use this skill as the front door for skill selection and composition.

## Workflow

1. Classify user intent by domain.
2. Select one primary skill and optional secondary skill.
3. If the capability is missing in current environment, output exact install command(s).
4. If user asks for reusable standards, suggest AGENTS snippets from local references.
5. Do not auto-install skills.
6. Ask user to confirm installation before proceeding.

## Routing Output Format

Return these sections in order:

- `Selected Skill`
- `Why`
- `Install (if needed)`
- `Next Prompt`

## Install Command Template

Use this exact command format:

```bash
npx skills add gaelic-ghost/productivity-skills --skill <skill-name>
```

Never claim installation success until user confirms completion.

## Active Skills

- `project-docs-maintainer`
- `project-roadmap-maintainer`
- `project-workspace-cleaner`
- `things-reminders-manager`
- `things-digest-generator`

Use `references/skill-routing-matrix.md` for domain-to-skill mapping and composition patterns.

## AGENTS Snippets

Use local snippet source:

- `references/agents-snippets.md`

Use this when routing reveals users need shared standards in addition to a task-specific skill.

## Snippet Suggestion Workflow

1. Detect requests for cross-repo standards or policy boilerplate.
2. Offer relevant snippet block(s) from `references/agents-snippets.md`.
3. Point to insertion target in user `AGENTS.md` and suggest minimal edits.
4. Require explicit user confirmation before editing any `AGENTS.md`.
5. Report suggested snippets and applied edits in separate lines.
