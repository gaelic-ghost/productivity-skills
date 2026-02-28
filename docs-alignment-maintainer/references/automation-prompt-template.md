# Automation Prompt Template

Use this as the automation task prompt body.

```text
Use $docs-alignment-maintainer to scan and maintain docs alignment for repositories under the assigned workspace root.

Run:
python3 /Users/galew/Workspace/productivity-skills/docs-alignment-maintainer/scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --apply-fixes \
  --md-out /tmp/docs-alignment-report.md \
  --json-out /tmp/docs-alignment-report.json \
  --fail-on-issues

Then:
1. Summarize key findings (repos scanned, repos with issues, unresolved issue count).
2. List all modified docs files.
3. Call out any skipped or ambiguous fixes.
4. Include both artifact paths in the final response:
   - /tmp/docs-alignment-report.md
   - /tmp/docs-alignment-report.json
5. Do not commit any changes.
```

## Parameterized Variant

If the automation passes dynamic paths, use this pattern:

```text
Use $docs-alignment-maintainer.
Workspace root: {{workspace_root}}
Excluded paths: {{exclude_paths_csv}}

Run the script with `--workspace` set to `{{workspace_root}}` and one `--exclude` per excluded path.
Enable `--apply-fixes`, write Markdown and JSON reports under `/tmp`, and do not commit changes.
```
