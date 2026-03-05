# Skill Routing Matrix

## Domain Mapping

| Intent signal | Primary skill | Optional secondary skill |
| --- | --- | --- |
| Roadmap planning, milestone updates, ROADMAP.md maintenance | `project-docs-maintainer` (`mode=roadmap_maintenance`) | `project-roadmap-maintainer` (deprecated shim) |
| Docs drift, README standards, docs alignment audits | `project-docs-maintainer` (`mode=workspace_docs_alignment` or `mode=skills_readme_alignment`) | `project-roadmap-maintainer` (deprecated shim only for legacy invocation routing) |
| Things reminders, rescheduling, update-vs-create todo mutation | `things-reminders-manager` | `things-digest-generator` |
| Things weekly planning digest, priorities, week-ahead summary | `things-digest-generator` | `things-reminders-manager` |
| Workspace cleanup chores, stale artifacts, disk hygiene ranking | `project-workspace-cleaner` | `project-docs-maintainer` |

## Snippet Routing Hints

Use AGENTS snippet suggestions when intent includes:

- "standardize this across repos"
- "give me AGENTS policy snippets"
- "create reusable guidance"
- "copy/paste standards"
Snippet sources:

- Orchestrator: `references/agents-snippets.md`
- Routed skill: `<selected-skill>/references/agents-snippets.md`

Prefer routed skill snippets first, then orchestrator snippets for generic policy blocks.

## Install Guidance

When a selected skill is unavailable, output:

```bash
npx skills add gaelic-ghost/productivity-skills --skill <skill-name>
```

For multi-skill composition, output one command per missing skill.

## Example Response Shape

- `Selected Skill`: `project-docs-maintainer`
- `Why`: Request asks for README/docs alignment or roadmap maintenance through canonical docs-maintainer modes.
- `Install (if needed)`: `npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer`
- `Next Prompt`: Use `$project-docs-maintainer` with `mode=skills_readme_alignment` (or `mode=roadmap_maintenance`) and appropriate target path.
