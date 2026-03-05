# AGENTS Snippets

Use these snippet blocks when users ask to standardize workflows across repositories. Suggest snippets first, then wait for explicit confirmation before editing any `AGENTS.md`.

## External Guidance Links

```markdown
- Skill Creator workflow: [$skill-creator](/Users/galew/.codex/skills/.system/skill-creator/SKILL.md)
- OpenAI Codex Skills: https://developers.openai.com/codex/skills
- OpenAI Codex AGENTS.md configuration: https://developers.openai.com/codex/configuration/agents-md
- Claude Code Features Overview: https://code.claude.com/docs/en/features-overview
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Anthropic Agent Skills Best Practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code Plugins: https://code.claude.com/docs/en/plugins
- The Complete Guide to Building Skill for Claude (PDF): https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- Agent Skills Standard: https://agentskills.io/home
- Vercel KB Guidance: https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context
```

## Python Execution Baseline

```markdown
- Use `uv run` for Python commands (`uv run python`, `uv run pytest`, `uv run ruff check`, `uv run mypy`) unless repository docs explicitly require otherwise.
```

## Safety Defaults

```markdown
- Never auto-commit changes.
- Never auto-install dependencies or tools without explicit user confirmation.
- Keep edits bounded to the requested scope.
- When blocked, report the exact blocker and the next required user action.
```

## Config Precedence Template

```markdown
Configuration precedence:
1. CLI flags
2. `config/customization.yaml`
3. `config/customization.template.yaml`
4. tool/script defaults
```

## Output Contract Template

```markdown
- Provide a short human-readable summary.
- Provide machine-readable JSON output when the workflow supports it.
- Include touched files, unresolved issues, and explicit error details.
```

## Relative Date Normalization Template

```markdown
- Resolve relative date terms (`today`, `tomorrow`, `next Monday`) against current local date/time first.
- Confirm scheduled dates in absolute form with timezone in user-visible output.
```
