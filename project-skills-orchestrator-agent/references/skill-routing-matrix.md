# Skill Routing Matrix

## Domain Mapping

| Intent signal | Primary skill | Optional secondary skill |
| --- | --- | --- |
| Roadmap planning, milestone updates, ROADMAP.md maintenance | `project-docs-maintainer` (`mode=roadmap_maintenance`) | none |
| `*-skills` README drift, README standards audits | `project-docs-maintainer` (`mode=skills_readme_maintenance`) | none |
| Things reminders, rescheduling, update-vs-create todo mutation | `things-reminders-manager` | `things-digest-generator` only when the user explicitly asks for planning context too |
| Things weekly planning digest, priorities, week-ahead summary | `things-digest-generator` | `things-reminders-manager` only when the user explicitly asks for reminder mutation too |
| Workspace cleanup chores, stale artifacts, disk hygiene ranking | `project-workspace-cleaner` | none |

## Composition Rule

- Default to exactly one selected skill.
- Add a second skill only when the user explicitly asks for both:
  - planning plus mutation
  - audit plus follow-up action
  - digest plus reminder mutation
- Otherwise do not compose.

## Legacy Handling

- Route to `project-roadmap-maintainer` only when the user explicitly targets the legacy roadmap-maintainer surface.
- Treat `skills_readme_alignment` as a compatibility alias for `skills_readme_maintenance`, not as a primary route.

## Install Guidance

When a selected skill is unavailable, output:

```bash
npx skills add gaelic-ghost/productivity-skills --skill <skill-name>
```

`Install (if needed)` must be:

- `none` when all required skills are already available
- one exact install command when one required skill is missing
- one exact install command per skill only for an allowed two-skill composed route

## Example Response Shape

- `Selected Skill`: `project-docs-maintainer`
- `Why`: Request asks for `*-skills` README maintenance or roadmap maintenance through canonical docs-maintainer modes.
- `Install (if needed)`: `npx skills add gaelic-ghost/productivity-skills --skill project-docs-maintainer`
- `Next Prompt`: Use `$project-docs-maintainer` with `mode=skills_readme_maintenance` or `mode=roadmap_maintenance` and the appropriate target path.
