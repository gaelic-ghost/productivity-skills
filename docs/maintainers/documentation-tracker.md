# Maintainer Documentation Tracker

Track repo-maintainer docs and runtime-doc boundary cleanup.

| Surface | Pass 1: accurate/current | Pass 2: simplified/improved | Notes |
| --- | --- | --- | --- |
| `AGENTS.md` | done | done | Maintainer-only role clarified; points to `docs/maintainers/`. |
| `README.md` | done | done | Reduced to user-facing install/use guidance only. |
| `docs/maintainers/agents-standards-snippets.md` | done | done | Maintainer-only snippet source. |
| `docs/maintainers/reality-audit.md` | done | done | Source-of-truth order and audit procedure documented. |
| `docs/maintainers/documentation-rubric.md` | done | done | Maintainer audit rubric moved out of runtime docs. |
| `docs/maintainers/workflow-atlas.md` | done | done | Repo workflow diagrams moved to maintainer-only docs. |
| `project-docs-maintainer/SKILL.md` | done | done | Reduced to canonical modes, outputs, guardrails, and references. |
| `project-docs-maintainer/agents/openai.yaml` | done | done | Prompt and summary aligned to canonical mode names only. |
| `project-docs-maintainer/references/*` | done | done | Runtime references remain skill-local only. |
| `project-roadmap-maintainer/SKILL.md` | done | done | Shrunk to a thin compatibility redirect. |
| `project-roadmap-maintainer/agents/openai.yaml` | done | done | Metadata now describes redirect-only behavior. |
| `project-roadmap-maintainer/references/*` | done | done | Redirect references kept internal to the runtime surface. |
| `project-skills-orchestrator-agent/SKILL.md` | done | done | Main path reduced to deterministic routing and install guidance. |
| `project-skills-orchestrator-agent/agents/openai.yaml` | done | done | Canonical routing prompt now prefers current skill names. |
| `project-skills-orchestrator-agent/references/skill-routing-matrix.md` | done | done | Routing table favors canonical skills and no longer points at repo docs. |
| `project-workspace-cleaner/SKILL.md` | done | done | Runtime path retained; customization and automation stay in references. |
| `project-workspace-cleaner/agents/openai.yaml` | done | done | Prompt aligned with config precedence and read-only contract. |
| `project-workspace-cleaner/references/*` | done | done | Skill-specific references retained with no repo-doc dependency. |
| `things-digest-generator/SKILL.md` | done | done | MCP-first digest workflow clarified with JSON fallback and exact output rules. |
| `things-digest-generator/agents/openai.yaml` | done | done | Prompt aligned with canonical data-collection path. |
| `things-digest-generator/references/output-format.md` | done | done | Updated to match optional executive summary behavior and clean-run rules. |
| `things-reminders-manager/SKILL.md` | done | done | Update-first mutation path clarified with deterministic blocked state. |
| `things-reminders-manager/agents/openai.yaml` | done | done | Prompt aligned with update-first, auth-aware workflow. |
| `things-reminders-manager/references/*` | done | done | Mutation-specific references retained with no repo-doc dependency. |
