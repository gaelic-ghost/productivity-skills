# AGENTS.md

## Repository Expectations

- For work in this repository, edit skills only under `/Users/galew/Workspace/productivity-skills`.
- Never modify production-installed skills under `~/.agents/skills` while working in this development repository.

## Standards and Guidance

Always consult these resources when creating, updating, reviewing, or sharing skills:

- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills)
- OpenAI Codex AGENTS.md configuration: [developers.openai.com/codex/configuration/agents-md](https://developers.openai.com/codex/configuration/agents-md)
- Claude Code Features Overview: [code.claude.com/docs/en/features-overview](https://code.claude.com/docs/en/features-overview)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Anthropic Agent Skills Best Practices: [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- The Complete Guide to Building Skill for Claude (PDF): [resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)
- Vercel KB Guidance: [vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context](https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context)

Applicability guidance:

- Always consult Skill Creator workflow for skill lifecycle work.
- Consult OpenAI Codex docs when behavior is OpenAI/Codex specific.
- Consult Claude docs when behavior is Claude skills/plugins specific.
- Consult Agent Skills Standard and Vercel guidance for cross-platform standards alignment.

## Repo-local Passive Standards

- Prefer `uv run` for Python command execution in examples and scripts.
- Keep skill instructions deterministic, concise, and safety-forward.
- Never auto-commit or auto-install; report required commands and wait for user confirmation.
- Keep cross-cutting standards in shared docs, and keep specialized procedures in skill-local references.

See `docs/agents-standards-snippets.md` for reusable copy/paste blocks.
