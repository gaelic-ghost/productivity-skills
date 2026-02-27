# productivity-skills

Curated Codex skills focused on productivity workflows, intended for sharing and installation via skills tooling.

## How To Add (Skills CLI)

```bash
npx @vercel/skills add gaelic-ghost/productivity-skills
```

```bash
npx skills add gaelic-ghost/productivity-skills
```

CLI flags from the [`skills` package docs](https://www.npmjs.com/package/skills):

- `-a, --agent <agents...>`: target specific agents (recommended here: `-a codex`)
- `-g, --global`: install globally instead of project-local

Examples:

```bash
# Project-local install for Codex
npx skills add gaelic-ghost/productivity-skills -a codex

# Global install for Codex
npx skills add gaelic-ghost/productivity-skills -a codex -g
```

## Included skills

- `project-roadmap-manager`
- `workspace-cleanup-audit`
- `things-week-ahead-digest`
- `talktomepy-tts`

## Customization guides

Each skill directory includes a `README.md` with personalization points, common tuning profiles, example Codex prompts, and validation checklists.

- [`project-roadmap-manager/README.md`](./project-roadmap-manager/README.md)
- [`workspace-cleanup-audit/README.md`](./workspace-cleanup-audit/README.md)
- [`things-week-ahead-digest/README.md`](./things-week-ahead-digest/README.md)
- [`talktomepy-tts/README.md`](./talktomepy-tts/README.md)

## Source and curation

All skills were copied from `~/.codex/skills` using git-tracked files only.

## License

Apache License 2.0. See [LICENSE](./LICENSE).
