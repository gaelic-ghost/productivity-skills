# productivity-skills

Curated Codex skills for productivity workflows, maintenance automation, and operational hygiene.

For standards and applicability guidance, see [AGENTS.md](./AGENTS.md).

## Table of Contents

- [What These Agent Skills Help With](#what-these-agent-skills-help-with)
- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)
- [Quick Start (Vercel Skills CLI)](#quick-start-vercel-skills-cli)
- [Install individually by Skill or Skill Pack](#install-individually-by-skill-or-skill-pack)
- [Update Skills](#update-skills)
- [More resources for similar Skills](#more-resources-for-similar-skills)
- [Repository Layout](#repository-layout)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What These Agent Skills Help With

This repository packages reusable Codex skills for orchestrating installs, maintaining docs and roadmaps, and managing personal productivity workflows.

## Skill Guide (When To Use What)

- `project-skills-orchestrator-agent`
  - Front-door router that selects the best skill and prints exact install commands for missing skills.
- `project-docs-maintainer`
  - Audit and safely align workspace docs, `*-skills` README standards, and checklist roadmap maintenance using explicit modes.
- `project-roadmap-maintainer`
  - Deprecated compatibility shim that redirects roadmap requests to `project-docs-maintainer` roadmap mode.
- `project-workspace-cleaner`
  - Read-only workspace hygiene scanner that ranks cleanup chores.
- `things-reminders-manager`
  - Deterministic Things reminder create/update workflow with duplicate and date safeguards.
- `things-digest-generator`
  - Weekly Things digest generator with prioritized next-step suggestions.

## Quick Start (Vercel Skills CLI)

Use the Vercel `skills` CLI to install from this repository.

```bash
# Install from this repository (interactive picker)
npx skills add gaelic-ghost/productivity-skills
```

Install the orchestrator first:

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-skills-orchestrator-agent
```

Then ask your agent to route your request and suggest any missing installs.

```bash
# Install all skills from this repository
npx skills add gaelic-ghost/productivity-skills --all
```

## Install individually by Skill or Skill Pack

```bash
npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer
npx skills add gaelic-ghost/productivity-skills --skill project-roadmap-maintainer
npx skills add gaelic-ghost/productivity-skills --skill project-workspace-cleaner
npx skills add gaelic-ghost/productivity-skills --skill things-reminders-manager
npx skills add gaelic-ghost/productivity-skills --skill things-digest-generator
```

Roadmap note:

- Canonical roadmap handling is now through `$project-docs-maintainer` with `mode=roadmap_maintenance`.
- `project-roadmap-maintainer` remains installable as a compatibility shim for one deprecation cycle.

## Update Skills

```bash
npx skills check
npx skills update
```

## More resources for similar Skills

### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "skills orchestration"
npx skills find "readme alignment maintainer"
npx skills find "things productivity automation"
```

### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
# `Find Skills` is a part of Vercel's `agent-skills` repo
npx skills add vercel-labs/agent-skills --skill find-skills
```

Then ask your Agent for help finding a skill for "" or ""

### Leaderboard

- Skills catalog: [skills.sh](https://skills.sh/)

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
- `project-docs-maintainer` supports `workspace_docs_alignment`, `skills_readme_alignment`, and `roadmap_maintenance` modes.

## Keywords

Codex skills, skills orchestration, docs alignment, roadmap maintenance, workspace cleanup, Things reminders, Things digest, productivity automation.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
