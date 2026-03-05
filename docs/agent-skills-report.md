# Agent Skills Report

## Purpose and Method
This report documents agent skills in this repository using only repository sources: each skill's `SKILL.md` plus targeted `references/*.md` files. It focuses on automation use-cases, operational workflows, and user-facing UI/UX paths without inferring undocumented behavior.

## Skills at a Glance

| Skill | Primary domain | Automation suitability (App/CLI) | Mutation profile |
| --- | --- | --- | --- |
| `project-docs-maintainer` | Workspace docs alignment, `*-skills` README standards, and roadmap checklist maintenance | App: Strong/Strong/Conditional, CLI: Strong/Strong/Conditional (mode-dependent) | `bounded-write` |
| `project-roadmap-maintainer` | Deprecated compatibility shim for roadmap requests | Compatibility wrapper only | `read-only` |
| `project-skills-orchestrator-agent` | Skill routing/composition and install guidance | Not explicitly rated; routing workflow documented | `read-only` |
| `project-workspace-cleaner` | Read-only workspace cleanup audits and ranking | App: Strong, CLI: Strong | `read-only` |
| `things-digest-generator` | Things week-ahead planning digest generation | App: Strong, CLI: Conditional | `read-only` |
| `things-reminders-manager` | Things reminder create/update with duplicate/date safeguards | App/CLI templates provided (no explicit rating) | `mutation-capable` |

## Detailed Skill Profiles

### project-docs-maintainer

#### Automation Use-Cases
- Recurring workspace documentation drift audits (`workspace_docs_alignment`).
- Profile-aware README standards audits for `*-skills` repositories (`skills_readme_alignment`).
- Checklist roadmap consistency checks and bounded roadmap migration/updates (`roadmap_maintenance`).
- Two-pass automation patterns: audit-only/check-only or bounded apply mode depending on mode and request.

#### Workflow
1. Select mode from user intent.
2. Run pass-1 audit/check.
3. Review issue categories and impacted targets.
4. Optionally run bounded fix/apply path.
5. Re-check touched targets and return Markdown + JSON results.

#### UI/UX Path
- Trigger intents: docs drift, README standards alignment, roadmap checklist maintenance/migration.
- Decision points: mode selection (`workspace_docs_alignment`/`skills_readme_alignment`/`roadmap_maintenance`), check-only vs apply/fixes, AGENTS snippet insertion approval.
- User-visible outputs: structured summaries, JSON-ready fields, report file paths, and exact `No findings.` on clean runs.
- End states: archive when no issues and no errors; otherwise keep in inbox triage with prioritized findings.

#### Inputs and Outputs
- Inputs: mode-specific flags (`--workspace` or `--project-root`, plus optional excludes/paths and check/apply toggles).
- Outputs: Markdown summary plus machine-readable JSON report with run context, findings, actions, and errors.

#### Guardrails and Failure Handling
- Never auto-commit/push.
- Never edit source code, manifests, lockfiles, CI files, or generated artifacts.
- AGENTS edits only after explicit approval, snippet insertion only.
- For roadmap mode apply, edits are bounded to target `ROADMAP.md` only.
- On sandbox/permission blocks, report blocked operation and minimum required access.

#### Automation Readiness Notes
- Default safe posture: read-only audit/check-only variants.
- Bounded apply/fix variants are suitable with workspace-write access and explicit request intent.

#### Source References
- `project-docs-maintainer/SKILL.md`
- `project-docs-maintainer/references/automation-prompts.md`
- `project-docs-maintainer/references/automation-prompts-skills-readme.md`
- `project-docs-maintainer/references/roadmap-automation-prompts.md`
- `project-docs-maintainer/scripts/docs_alignment_maintainer.py`
- `project-docs-maintainer/scripts/readme_alignment_maintainer.py`
- `project-docs-maintainer/scripts/roadmap_alignment_maintainer.py`

### project-roadmap-maintainer

#### Automation Use-Cases
- Backward-compatible entrypoint for legacy invocations/install references.
- Redirect-only flow to canonical roadmap mode under docs maintainer.

#### Workflow
1. Detect compatibility invocation.
2. Redirect to `$project-docs-maintainer` with `mode=roadmap_maintenance`.
3. Preserve check-only/apply intent and target path context.

#### UI/UX Path
- Trigger intents: legacy calls to `$project-roadmap-maintainer`.
- Decision points: none beyond preserving run intent/paths.
- User-visible outputs: deprecation notice plus canonical redirected invocation.
- End states: handoff to docs maintainer roadmap mode.

#### Inputs and Outputs
- Inputs: legacy roadmap maintenance requests.
- Outputs: canonical redirect instructions, not independent roadmap execution behavior.

#### Guardrails and Failure Handling
- Must not present itself as canonical roadmap owner.
- Must point to docs maintainer roadmap references for behavior/schema.

#### Automation Readiness Notes
- Transitional compatibility shim for one deprecation cycle.

#### Source References
- `project-roadmap-maintainer/SKILL.md`
- `project-roadmap-maintainer/agents/openai.yaml`

### project-skills-orchestrator-agent

#### Automation Use-Cases
- Front-door routing from user intent to one primary skill and optional secondary skill.
- Install guidance for missing capabilities with exact `npx skills add` commands.
- Composition-aware handoff with ready-to-use next prompt.

#### Workflow
1. Classify request intent by domain.
2. Select primary and optional secondary skill.
3. Provide install commands for missing skills.
4. Suggest AGENTS snippets when standards requests are present.
5. Wait for user confirmation before installation-related progression.

#### UI/UX Path
- Trigger intents: "which skill should I use", multi-domain requests, missing skill capability.
- Decision points: domain mapping selection, single-skill vs composed routing, installed vs missing path.
- User-visible outputs: response shape (`Selected Skill`, `Why`, `Install (if needed)`, `Next Prompt`) and one install command per missing skill.
- End states: routed handoff to selected skill/mode.

#### Inputs and Outputs
- Inputs: natural-language user request and observed environment capability.
- Outputs: deterministic routing recommendation plus explicit install guidance.

#### Guardrails and Failure Handling
- Never auto-install.
- Never claim install success without user confirmation.
- Prefer routed-skill snippets before orchestrator-generic snippets.

#### Automation Readiness Notes
- Read-only coordination skill; best used as orchestration layer ahead of task skills.

#### Source References
- `project-skills-orchestrator-agent/SKILL.md`
- `project-skills-orchestrator-agent/references/skill-routing-matrix.md`

### project-workspace-cleaner

#### Automation Use-Cases
- Recurring read-only workspace hygiene scans.
- Priority ranking of stale build/cache/transient artifacts.
- Markdown + JSON reporting for cleanup triage.

#### Workflow
1. Load customization config with precedence.
2. Run workspace cleanup scanner.
3. Rank findings by severity/size.
4. Report top findings and repo-level totals.
5. Provide cleanup recommendations as text only.

#### UI/UX Path
- Trigger intents: disk hygiene audits, stale artifact detection, cleanup prioritization.
- Decision points: threshold tuning (`min_mb`, `stale_days`, `max_findings`) and scope path.
- User-visible outputs: ranked findings with required fields, repo summary, exact `No findings.` when thresholds produce no findings.
- End states: archive when no findings; inbox triage otherwise.

#### Inputs and Outputs
- Inputs: workspace root and threshold parameters.
- Outputs: Markdown summary and JSON report with per-finding metadata and repo aggregates.

#### Guardrails and Failure Handling
- Strict read-only behavior.
- Never delete/move/edit files; never run cleanup commands automatically.
- Partial-results handling when some paths are inaccessible.

#### Automation Readiness Notes
- High readiness for unattended scheduled scans under read-only sandboxing.

#### Source References
- `project-workspace-cleaner/SKILL.md`
- `project-workspace-cleaner/references/automation-prompts.md`

### things-digest-generator

#### Automation Use-Cases
- Weekly/daily Things planning digests.
- Priority and risk surfacing from open + recently completed tasks.
- MCP-first data collection with JSON fallback.

#### Workflow
1. Load customization config.
2. Read areas, open projects, open todos, and recent completed tasks (MCP-first).
3. Build urgency buckets and activity scores.
4. Identify top active projects/areas.
5. Generate bounded suggestions.
6. Format output in required section order.

#### UI/UX Path
- Trigger intents: Things check-ins, week-ahead planning, prioritized suggestions.
- Decision points: source mode (`mcp` vs `json`), permission/tool availability, horizon/verbosity settings.
- User-visible outputs: ordered sections (`Snapshot`, `Recently Active`, `Week/Weekend Ahead`, `Suggestions`), exact `No findings.` for no actionable data.
- End states: archive on no-data runs; inbox triage otherwise.

#### Inputs and Outputs
- Inputs: MCP tools or four JSON inputs, planning horizon, digest output path.
- Outputs: Markdown digest with deterministic section order and concise operational tone.

#### Guardrails and Failure Handling
- Never modify Things data unless explicitly requested.
- If MCP fails, fall back to JSON when provided.
- If both sources unavailable, report precise missing permissions/paths and stop.

#### Automation Readiness Notes
- Strong for recurring app automations; CLI best when MCP or JSON exports exist.

#### Source References
- `things-digest-generator/SKILL.md`
- `things-digest-generator/references/automation-prompts.md`
- `things-digest-generator/references/output-format.md`

### things-reminders-manager

#### Automation Use-Cases
- Safe reminder creation and rescheduling in Things.
- Duplicate-avoidant update-first mutation paths.
- Relative-date normalization to absolute confirmations.

#### Workflow
1. Resolve local date anchor (`America/New_York` default unless user specifies otherwise).
2. Check Things capability/auth readiness.
3. Normalize relative date terms.
4. Search open tasks for candidate matches.
5. Choose update vs create path with duplicate safeguards.
6. Enforce token requirements for updates.
7. Execute mutation (`things_update_todo` or `things_add_todo`).
8. Return deterministic result metadata.

#### UI/UX Path
- Trigger intents: add reminder, reschedule, correct existing task, ambiguous update-vs-create requests.
- Decision points: auth/token status, zero/one/multiple match outcomes, date ambiguity, correction intent.
- User-visible outputs: action state (`created`, `updated`, or blocked), task title, normalized absolute schedule, explicit blockers.
- End states: successful mutation with explicit absolute confirmation, or blocked path requiring permissions/disambiguation.

#### Inputs and Outputs
- Inputs: reminder request, local date/time context, Things MCP query/update tools.
- Outputs: mutation result summary with explicit action and normalized schedule.

#### Guardrails and Failure Handling
- Never assume relative dates without local-date resolution.
- Never claim mutation success without tool confirmation.
- Never silently create duplicates when update intent is clear.
- Stop and report exact blocker when token is required but unavailable.

#### Automation Readiness Notes
- Suitable for intentional mutation runs with pre-validated auth.
- Requires stronger preflight checks than read-only reporting skills.

#### Source References
- `things-reminders-manager/SKILL.md`
- `things-reminders-manager/references/automation-prompts.md`
- `things-reminders-manager/references/mcp-sequence.md`

## Cross-Skill Workflow Composition
- Orchestrator-defined primary/secondary pairings:
  - Roadmap intent -> `project-docs-maintainer` (`mode=roadmap_maintenance`) (+ optional `project-roadmap-maintainer` compatibility shim)
  - Docs alignment intent -> `project-docs-maintainer` (`mode=workspace_docs_alignment` or `mode=skills_readme_alignment`) (+ optional roadmap shim for legacy redirect)
  - Things reminders intent -> `things-reminders-manager` (+ optional `things-digest-generator`)
  - Things digest intent -> `things-digest-generator` (+ optional `things-reminders-manager`)
  - Workspace cleanup intent -> `project-workspace-cleaner` (+ optional `project-docs-maintainer`)
- Shared UX composition pattern:
  - Route intent.
  - Provide install command(s) if needed.
  - Hand off with explicit next prompt to selected skill and mode.

## Recommended Automation Patterns
- `project-docs-maintainer`: default to read-only audit/check-only; use bounded apply/fix paths only when explicitly requested.
- `project-roadmap-maintainer`: use only when handling legacy invocations; redirect to docs maintainer roadmap mode.
- `project-skills-orchestrator-agent`: run as front-door coordinator before task skill execution.
- `project-workspace-cleaner`: schedule recurring read-only scans with threshold tuning.
- `things-digest-generator`: schedule recurring digest generation using MCP-first, JSON fallback.
- `things-reminders-manager`: use for intentional mutation runs with mandatory auth/date preflight.

## Gaps / Follow-Ups
- The compatibility shim lifecycle is policy-defined but does not yet include an explicit retirement date.
- `things-reminders-manager` templates remain less structured than other skills (no standard Suitability/Placeholders/Customization sections).
