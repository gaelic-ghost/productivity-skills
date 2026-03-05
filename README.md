# productivity-skills

Curated Codex skills for productivity workflows, maintenance automation, and operational hygiene.

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

## Active Skills

- `project-skills-orchestrator-agent`
  - Front-door router that selects the best skill and prints exact install commands for missing skills.
- `project-docs-maintainer`
  - Audit and safely align workspace docs and `*-skills` README standards using explicit modes.
- `project-roadmap-maintainer`
  - Maintain a canonical checklist-style `ROADMAP.md` for milestones, tickets, and exit criteria.
- `project-workspace-cleaner`
  - Read-only workspace hygiene scanner that ranks cleanup chores.
- `things-reminders-manager`
  - Deterministic Things reminder create/update workflow with duplicate and date safeguards.
- `things-digest-generator`
  - Weekly Things digest generator with prioritized next-step suggestions.

## Migration Table (Old -> New)

| Old skill name | New skill name |
| --- | --- |
| `docs-alignment-maintainer` | `project-docs-maintainer` |
| `skills-readme-alignment-maintainer` | `project-docs-maintainer` (merged mode) |
| `project-roadmap-manager` | `project-roadmap-maintainer` |
| `workspace-cleanup-audit` | `project-workspace-cleaner` |
| `things-mcp-reminder-wrapper` | `things-reminders-manager` |
| `things-week-ahead-digest` | `things-digest-generator` |

## Quick Start

Install the orchestrator first:

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-skills-orchestrator-agent
```

Then ask your agent to route your request and suggest any missing installs.

## Install Individually

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-skills-orchestrator-agent
npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer
npx skills add gaelic-ghost/productivity-skills --skill project-roadmap-maintainer
npx skills add gaelic-ghost/productivity-skills --skill project-workspace-cleaner
npx skills add gaelic-ghost/productivity-skills --skill things-reminders-manager
npx skills add gaelic-ghost/productivity-skills --skill things-digest-generator
```

Install all skills:

```bash
npx skills add gaelic-ghost/productivity-skills --all
```

## Update Installed Skills

```bash
npx skills check
npx skills update
```

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── AGENTS.md
├── ROADMAP.md
├── docs/
│   └── agents-standards-snippets.md
├── project-docs-maintainer/
├── project-roadmap-maintainer/
├── project-skills-orchestrator-agent/
├── project-workspace-cleaner/
├── things-digest-generator/
└── things-reminders-manager/
```

## Notes

- Each skill keeps `SKILL.md` concise and pushes deeper details into `references/`.
- `project-docs-maintainer` supports `workspace_docs_alignment` and `skills_readme_alignment` modes.

## Search Keywords

Codex skills, skills orchestration, docs alignment, roadmap maintenance, workspace cleanup, Things reminders, Things digest, productivity automation.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
