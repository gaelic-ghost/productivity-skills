---
name: project-skills-orchestrator-agent
description: Route user requests to the best matching canonical skill in this repository and provide install guidance when capabilities are missing. Use when users need help choosing, composing, or installing skills for docs maintenance, roadmap maintenance, Things workflows, or workspace cleanup.
---

# Project Skills Orchestrator Agent

Use this skill as the front door for choosing the right canonical skill.

## Inputs

- Natural-language user request
- Current installed-skill state, if known
- A second skill is allowed only when the user explicitly asks for both:
  - planning plus mutation
  - audit plus follow-up action
  - digest plus reminder mutation

## Workflow

1. Classify the request by domain using `references/skill-routing-matrix.md`.
2. Choose exactly one primary canonical skill by default.
3. Add a secondary skill only when the request explicitly asks for one of the allowed composed workflows.
4. If a required skill is missing, print the exact install command.
5. Hand back a ready-to-send next prompt for the selected skill.
6. Use the compatibility shim only when a user explicitly asks for the legacy roadmap surface.

## Output Contract

Return these sections in order:

- `Selected Skill`
- `Why`
- `Install (if needed)`
- `Next Prompt`

`Install (if needed)` must be:

- `none` when all required skills are already available
- one exact install command when one required skill is missing
- one exact install command per skill only for an allowed two-skill composed route

Use this exact install command format when needed:

```bash
npx skills add gaelic-ghost/productivity-skills --skill <skill-name>
```

## Guardrails

- Never auto-install a skill.
- Never claim install success without user confirmation.
- Prefer canonical skills over compatibility shims.
- Default to one selected skill.
- Keep shared-policy suggestions secondary to the routing decision.

## References

- `references/skill-routing-matrix.md`
