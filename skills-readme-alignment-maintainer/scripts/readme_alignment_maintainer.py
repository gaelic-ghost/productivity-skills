#!/usr/bin/env python3
"""Two-pass README alignment maintainer for *-skills repositories."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PUBLIC_REPOS = {"apple-dev-skills", "productivity-skills", "python-skills"}
PRIVATE_REPOS = {"private-skills"}
BOOTSTRAP_REPOS = {"a11y-skills"}

EXPECTED_OWNER = "gaelic-ghost"

CORE_SECTION_KEYS = ["what", "guide", "quickstart", "individual", "find_cli", "layout", "notes", "license"]
PUBLIC_EXTRA_KEYS = ["find_skill", "keywords"]

SECTION_CANONICAL_HEADINGS = {
    "what": "What These Agent Skills Help With",
    "guide": "Skill Guide (When To Use What)",
    "quickstart": "Quick Start (Vercel Skills CLI)",
    "individual": "Install individually by Skill",
    "find_cli": "Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)",
    "layout": "Repository Layout",
    "notes": "Notes",
    "license": "License",
    "find_skill": "Find Skills like these with `Find Skills` by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)",
    "keywords": "Search Keywords",
}

SECTION_PATTERNS = {
    "what": r"^##\s+What These Agent Skills Help With\s*$",
    "guide": r"^##\s+Skill Guide \(When To Use What\)\s*$",
    "quickstart": r"^##\s+Quick Start \(Vercel Skills CLI\)\s*$",
    "individual": r"^##\s+Install individually by Skill\s*$",
    "find_cli": r"^##\s+Find Skills like these with.*`?skills`?\s+CLI",
    "layout": r"^##\s+Repository Layout\s*$",
    "notes": r"^##\s+Notes\s*$",
    "license": r"^##\s+License\s*$",
    "find_skill": r"^##\s+Find Skills like these with.*`?Find Skills`?",
    "keywords": r"^##\s+Search Keywords\s*$",
}

HEADING_ALIASES = {
    "how to add (skills cli)": "quickstart",
    "how to add (vercel skills cli)": "quickstart",
    "how to add with skills cli": "quickstart",
    "quickstart (skills cli)": "quickstart",
    "included skills": "guide",
    "included skill": "guide",
    "skills included": "guide",
    "install by skill": "individual",
    "install individually by skills": "individual",
}

HIGH_CONFIDENCE_HEADING_PATTERNS = [
    ("quickstart", re.compile(r"^quick\s*start.*skills\s*cli$", re.IGNORECASE)),
    ("quickstart", re.compile(r"^how\s+to\s+add.*skills\s*cli$", re.IGNORECASE)),
    ("individual", re.compile(r"^install\s+(?:individually|individual)\s+by\s+skills?$", re.IGNORECASE)),
    ("individual", re.compile(r"^install\s+by\s+skills?$", re.IGNORECASE)),
    ("guide", re.compile(r"^included\s+skills?$", re.IGNORECASE)),
    ("find_cli", re.compile(r"^find\s+skills?.*skills\s*cli.*$", re.IGNORECASE)),
    ("find_skill", re.compile(r"^find\s+skills?.*find\s+skills.*$", re.IGNORECASE)),
]

SECTION_TEMPLATES = {
    "what": "## What These Agent Skills Help With\n\nDescribe the audience and the workflows this repository improves.\n",
    "guide": "## Skill Guide (When To Use What)\n\n- `<skill-name>`\n  - Use when ...\n  - Helps by ...\n",
    "quickstart": (
        "## Quick Start (Vercel Skills CLI)\n\n"
        "```bash\n"
        "npx skills add gaelic-ghost/{repo}\n"
        "```\n"
    ),
    "individual": "## Install individually by Skill\n\nAdd one `npx skills add <owner/repo@skill>` command per skill.\n",
    "find_cli": (
        "## Find Skills like these with the `skills` CLI by Vercel — "
        "[vercel-labs/skills](https://github.com/vercel-labs/skills)\n\n"
        "```bash\n"
        "npx skills find \"xcode mcp\"\n"
        "npx skills find \"swift package workflow\"\n"
        "npx skills find \"dash docset apple docs\"\n"
        "```\n"
    ),
    "find_skill": (
        "## Find Skills like these with `Find Skills` by Vercel — "
        "[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)\n\n"
        "```bash\n"
        "npx skills add vercel-labs/agent-skills\n"
        "npx skills find \"skills repository hygiene\"\n"
        "```\n\n"
        "- Skills catalog: https://skills.sh/\n"
    ),
    "layout": "## Repository Layout\n\n```text\n.\n├── README.md\n└── <skill-directories>/\n```\n",
    "notes": "## Notes\n\n- Keep README commands and skill inventory synchronized.\n",
    "license": "## License\n\nSee [LICENSE](./LICENSE).\n",
    "keywords": "## Search Keywords\n\nCodex skills, automation, workflows, documentation alignment.\n",
}


@dataclass
class Issue:
    issue_id: str
    category: str
    severity: str
    repo: str
    doc_file: str
    evidence: str
    recommended_fix: str
    auto_fixable: bool
    fixed: bool = False
    normalized_from: Optional[str] = None
    normalized_to: Optional[str] = None
    normalization_method: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "issue_id": self.issue_id,
            "category": self.category,
            "severity": self.severity,
            "repo": self.repo,
            "doc_file": self.doc_file,
            "evidence": self.evidence,
            "recommended_fix": self.recommended_fix,
            "auto_fixable": self.auto_fixable,
            "fixed": self.fixed,
        }
        if self.normalized_from is not None:
            payload["normalized_from"] = self.normalized_from
        if self.normalized_to is not None:
            payload["normalized_to"] = self.normalized_to
        if self.normalization_method is not None:
            payload["normalization_method"] = self.normalization_method
        return payload


@dataclass
class HeadingNormalizationEvent:
    line: int
    section_key: str
    original_heading: str
    normalized_heading: str
    normalization_method: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "line": self.line,
            "section_key": self.section_key,
            "original_heading": self.original_heading,
            "normalized_heading": self.normalized_heading,
            "normalization_method": self.normalization_method,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and optionally align README standards for *-skills repos")
    parser.add_argument("--workspace", required=True, help="Workspace root")
    parser.add_argument("--repo-glob", default="*-skills", help="Repo directory glob")
    parser.add_argument("--exclude", action="append", default=[], help="Path to exclude (repeatable)")
    parser.add_argument("--apply-fixes", action="store_true", help="Apply bounded README fixes")
    parser.add_argument("--json-out", help="Write JSON report path")
    parser.add_argument("--md-out", help="Write Markdown report path")
    parser.add_argument("--print-json", action="store_true", help="Print JSON report")
    parser.add_argument("--print-md", action="store_true", help="Print Markdown report")
    parser.add_argument("--fail-on-issues", action="store_true", help="Exit non-zero when unresolved issues remain")
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def read_excludes(raw_excludes: Sequence[str]) -> List[Path]:
    excludes: List[Path] = []
    seen: set[str] = set()
    for raw in raw_excludes:
        p = Path(raw).expanduser().resolve()
        key = str(p)
        if key not in seen:
            excludes.append(p)
            seen.add(key)
    return excludes


def is_excluded(path: Path, excludes: Sequence[Path]) -> bool:
    resolved = path.resolve()
    for ex in excludes:
        try:
            resolved.relative_to(ex)
            return True
        except ValueError:
            continue
    return False


def discover_repos(workspace: Path, repo_glob: str, excludes: Sequence[Path]) -> List[Path]:
    repos: List[Path] = []
    for child in sorted(workspace.iterdir()):
        if not child.is_dir():
            continue
        if is_excluded(child, excludes):
            continue
        if fnmatch.fnmatch(child.name, repo_glob):
            repos.append(child)
    return repos


def detect_profile(repo_name: str) -> str:
    if repo_name in PUBLIC_REPOS:
        return "public-curated"
    if repo_name in PRIVATE_REPOS:
        return "private-internal"
    if repo_name in BOOTSTRAP_REPOS:
        return "bootstrap"
    return "generic"


def find_skill_dirs(repo: Path) -> List[str]:
    skills: List[str] = []
    for p in sorted(repo.glob("*/SKILL.md")):
        if p.parent.name not in {"scripts", "references", "assets", "agents"}:
            skills.append(p.parent.name)
    return skills


def heading_lines(text: str) -> List[Tuple[int, str]]:
    out: List[Tuple[int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        if line.startswith("## "):
            out.append((idx, line.strip()))
    return out


def canonical_heading_line(section_key: str) -> str:
    return f"## {SECTION_CANONICAL_HEADINGS[section_key]}"


def expected_section_keys(profile: str) -> List[str]:
    keys = list(CORE_SECTION_KEYS)
    if profile == "public-curated":
        keys.extend(PUBLIC_EXTRA_KEYS)
    return keys


def heading_body(line: str) -> str:
    return line[3:].strip() if line.startswith("## ") else line.strip()


def normalize_heading_lookup_key(value: str) -> str:
    key = re.sub(r"\s+", " ", value.strip().lower())
    key = key.replace("`", "")
    return key


def resolve_section_key_for_heading(line: str, allowed_keys: Sequence[str]) -> Tuple[Optional[str], Optional[str]]:
    body = heading_body(line)
    normalized_body = normalize_heading_lookup_key(body)
    allowed = set(allowed_keys)

    # Alias mappings are deterministic and preferred over pattern guesses.
    alias_key = HEADING_ALIASES.get(normalized_body)
    if alias_key and alias_key in allowed:
        return alias_key, "alias"

    matched_keys: List[str] = []
    for key, rx in HIGH_CONFIDENCE_HEADING_PATTERNS:
        if key in allowed and rx.search(normalized_body):
            matched_keys.append(key)
    if len(set(matched_keys)) == 1:
        return matched_keys[0], "pattern"
    if len(set(matched_keys)) > 1:
        return None, None

    return None, None


def find_matching_heading_indices(headings: List[Tuple[int, str]], pattern: str) -> List[int]:
    rx = re.compile(pattern, re.IGNORECASE)
    matches: List[int] = []
    for idx, (_lineno, heading) in enumerate(headings):
        if rx.search(heading):
            matches.append(idx)
    return matches


def first_match_heading_index(headings: List[Tuple[int, str]], pattern: str) -> Optional[int]:
    rx = re.compile(pattern, re.IGNORECASE)
    for idx, (_lineno, heading) in enumerate(headings):
        if rx.search(heading):
            return idx
    return None


def check_sections(repo: Path, profile: str, text: str) -> List[Issue]:
    issues: List[Issue] = []
    lines = text.splitlines()

    first_non_empty = next((line.strip() for line in lines if line.strip()), "")
    if not first_non_empty.startswith("# "):
        issues.append(
            Issue(
                issue_id="missing-title",
                category="schema-violation",
                severity="high",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README is missing an H1 title line.",
                recommended_fix="Add a top-level `# <repo-name>` heading.",
                auto_fixable=False,
            )
        )

    purpose_line = ""
    if first_non_empty.startswith("# "):
        try:
            title_idx = next(i for i, line in enumerate(lines) if line.strip() == first_non_empty)
            for line in lines[title_idx + 1 :]:
                stripped = line.strip()
                if not stripped:
                    continue
                purpose_line = stripped
                break
        except StopIteration:
            purpose_line = ""
    if not purpose_line or purpose_line.startswith("#"):
        issues.append(
            Issue(
                issue_id="missing-purpose-summary",
                category="schema-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README is missing a one-line purpose summary below the title.",
                recommended_fix="Add a concise one-line value proposition below the H1.",
                auto_fixable=False,
            )
        )

    headings = heading_lines(text)

    patterns = [(key, SECTION_PATTERNS[key]) for key in expected_section_keys(profile)]

    matched: List[Tuple[str, int]] = []
    for key, pattern in patterns:
        idx = first_match_heading_index(headings, pattern)
        if idx is None:
            issues.append(
                Issue(
                    issue_id=f"section-missing-{key}",
                    category="schema-violation",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Missing required section: {key}",
                    recommended_fix=f"Add required section `{key}`.",
                    auto_fixable=True,
                )
            )
        else:
            matched.append((key, idx))

    for lineno, line in headings:
        key, method = resolve_section_key_for_heading(line, [k for k, _ in patterns])
        if not key or not method:
            continue
        canonical = canonical_heading_line(key)
        if line == canonical:
            continue
        issues.append(
            Issue(
                issue_id="section-misnamed",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence=f"Heading at line {lineno} should be `{canonical}`.",
                recommended_fix="Rename heading to the canonical section title.",
                auto_fixable=True,
                normalized_from=line,
                normalized_to=canonical,
                normalization_method=method,
            )
        )

    for key, pattern in patterns:
        matches = find_matching_heading_indices(headings, pattern)
        if len(matches) > 1:
            issues.append(
                Issue(
                    issue_id="duplicate-canonical-section",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Multiple headings match required section `{key}`.",
                    recommended_fix="Manually consolidate duplicated section content under one canonical heading.",
                    auto_fixable=False,
                )
            )

    ordered_idxs = [idx for _, idx in matched]
    if ordered_idxs != sorted(ordered_idxs):
        issues.append(
            Issue(
                issue_id="section-order",
                category="schema-violation",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="Required sections are out of expected order.",
                recommended_fix="Reorder headings to canonical section schema.",
                auto_fixable=False,
            )
        )

    return issues


def find_todo_issues(repo: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    if re.search(r"\b(TODO|TBD|todo)\b", text):
        issues.append(
            Issue(
                issue_id="todo-placeholder",
                category="schema-violation",
                severity="medium",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="README contains TODO/TBD placeholders.",
                recommended_fix="Replace placeholders with concrete content.",
                auto_fixable=False,
            )
        )
    return issues


def parse_skills_add_commands(text: str) -> List[Tuple[str, str, Optional[str], str]]:
    rx = re.compile(r"^\s*npx\s+skills\s+add\s+([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)(?:@([A-Za-z0-9_.-]+))?", re.MULTILINE)
    out: List[Tuple[str, str, Optional[str], str]] = []
    for m in rx.finditer(text):
        owner, repo, skill = m.group(1), m.group(2), m.group(3)
        out.append((owner, repo, skill, m.group(0).strip()))
    return out


def check_commands(repo: Path, profile: str, text: str, skill_dirs: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    commands = parse_skills_add_commands(text)
    expected_repo = repo.name

    has_own_base = False
    own_cmd_counts: Dict[str, int] = {}

    for owner, repo_name, skill, line in commands:
        if owner == EXPECTED_OWNER and repo_name == expected_repo:
            has_own_base = True
            own_cmd_counts[line] = own_cmd_counts.get(line, 0) + 1
            if skill and skill not in skill_dirs:
                issues.append(
                    Issue(
                        issue_id=f"missing-skill-ref-{skill}",
                        category="command-integrity",
                        severity="high",
                        repo=repo.name,
                        doc_file=str(repo / "README.md"),
                        evidence=f"Install command references unknown skill `{skill}`.",
                        recommended_fix="Use only skill names that have a SKILL.md directory.",
                        auto_fixable=False,
                    )
                )

    if profile == "public-curated" and not has_own_base:
        issues.append(
            Issue(
                issue_id="missing-base-install-command",
                category="command-integrity",
                severity="high",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="No base `npx skills add gaelic-ghost/<repo>` command found.",
                recommended_fix="Add base skills install command for this repository.",
                auto_fixable=True,
            )
        )

    duplicates = [cmd for cmd, count in own_cmd_counts.items() if count > 1]
    if duplicates:
        issues.append(
            Issue(
                issue_id="duplicate-install-commands",
                category="command-integrity",
                severity="low",
                repo=repo.name,
                doc_file=str(repo / "README.md"),
                evidence="Duplicate install command blocks detected.",
                recommended_fix="Deduplicate repeated install commands.",
                auto_fixable=False,
            )
        )

    if profile == "public-curated":
        find_count = len(re.findall(r"^\s*npx\s+skills\s+find\s+", text, flags=re.MULTILINE))
        if find_count < 3:
            issues.append(
                Issue(
                    issue_id="insufficient-find-examples",
                    category="command-integrity",
                    severity="medium",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Only {find_count} `npx skills find` examples present.",
                    recommended_fix="Add at least 3 realistic skills find examples.",
                    auto_fixable=True,
                )
            )

    return issues


def check_links(repo: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    link_rx = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for link in link_rx.findall(text):
        if link.startswith(("http://", "https://", "mailto:")):
            continue
        if link.startswith("#"):
            continue
        path_part = link.split("#", 1)[0].strip()
        if not path_part:
            continue
        target = (repo / path_part).resolve()
        if not target.exists():
            issues.append(
                Issue(
                    issue_id=f"broken-link-{abs(hash(link)) % 100000}",
                    category="schema-violation",
                    severity="low",
                    repo=repo.name,
                    doc_file=str(repo / "README.md"),
                    evidence=f"Broken relative link target: {link}",
                    recommended_fix="Update or remove broken relative link.",
                    auto_fixable=False,
                )
            )
    return issues


def make_bootstrap_readme(repo: Path, skill_dirs: List[str]) -> str:
    lines = [
        f"# {repo.name}",
        "",
        "Codex skills focused on accessibility and speech-friendly automation workflows.",
        "",
        "## What These Agent Skills Help With",
        "",
        "This repository supports accessibility-centered agent workflows and practical speech/readability tooling.",
        "",
        "## Skill Guide (When To Use What)",
        "",
    ]
    for skill in skill_dirs:
        lines.extend([
            f"- `{skill}`",
            "  - Use when you need this accessibility-oriented workflow.",
            "  - Helps by providing repeatable, agent-safe steps.",
            "",
        ])
    lines.extend([
        "## Quick Start (Vercel Skills CLI)",
        "",
        "```bash",
        f"npx skills add {EXPECTED_OWNER}/{repo.name}",
        "```",
        "",
        "## Install individually by Skill",
        "",
    ])
    for skill in skill_dirs:
        lines.extend(["```bash", f"npx skills add {EXPECTED_OWNER}/{repo.name}@{skill}", "```", ""])

    lines.extend([
        "## Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)",
        "",
        "```bash",
        "npx skills find \"accessibility codex\"",
        "npx skills find \"speech automation\"",
        "npx skills find \"readability workflow\"",
        "```",
        "",
        "## Repository Layout",
        "",
        "```text",
        ".",
        "├── README.md",
        "└── <skill-directories>/",
        "```",
        "",
        "## Notes",
        "",
        "- Keep README commands aligned with available skills.",
        "",
        "## License",
        "",
        "Add a LICENSE file when this repository is ready for sharing.",
    ])
    return "\n".join(lines).strip() + "\n"


def normalize_headings(text: str, profile: str) -> Tuple[str, List[HeadingNormalizationEvent]]:
    allowed_keys = expected_section_keys(profile)
    out_lines = text.splitlines()
    events: List[HeadingNormalizationEvent] = []

    for idx, line in enumerate(out_lines):
        if not line.startswith("## "):
            continue
        section_key, method = resolve_section_key_for_heading(line, allowed_keys)
        if not section_key or not method:
            continue
        canonical = canonical_heading_line(section_key)
        if line == canonical:
            continue
        out_lines[idx] = canonical
        events.append(
            HeadingNormalizationEvent(
                line=idx + 1,
                section_key=section_key,
                original_heading=line,
                normalized_heading=canonical,
                normalization_method=method,
            )
        )

    out = "\n".join(out_lines)
    if text.endswith("\n"):
        out += "\n"
    return out, events


def append_missing_sections(text: str, repo_name: str, profile: str) -> Tuple[str, List[str], List[HeadingNormalizationEvent]]:
    out, events = normalize_headings(text, profile)
    appended: List[str] = []

    for key in expected_section_keys(profile):
        pattern = SECTION_PATTERNS[key]
        if re.search(pattern, out, flags=re.IGNORECASE | re.MULTILINE):
            continue
        template = SECTION_TEMPLATES[key].format(repo=repo_name)
        if not out.endswith("\n"):
            out += "\n"
        out += "\n" + template + "\n"
        appended.append(key)

    return out, appended, events


def dedupe_skills_add_lines(text: str) -> Tuple[str, int]:
    line_rx = re.compile(r"^\s*npx\s+skills\s+add\s+[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:@[A-Za-z0-9_.-]+)?\s*$")
    out_lines: List[str] = []
    seen: set[str] = set()
    removed = 0

    for line in text.splitlines():
        if line_rx.match(line):
            if line in seen:
                removed += 1
                continue
            seen.add(line)
        out_lines.append(line)

    out = "\n".join(out_lines)
    if text.endswith("\n"):
        out += "\n"
    return out, removed


def apply_fixes_for_repo(repo: Path, profile: str, skill_dirs: List[str]) -> Tuple[bool, List[Dict[str, object]], Optional[str]]:
    fixes: List[Dict[str, object]] = []
    readme = repo / "README.md"

    if not readme.exists():
        if profile == "bootstrap":
            write_text(readme, make_bootstrap_readme(repo, skill_dirs))
            fixes.append({"repo": repo.name, "file": str(readme), "rule": "create-missing-readme", "status": "applied", "reason": "bootstrap profile"})
            return True, fixes, None
        return False, fixes, "README.md missing and profile is not bootstrap"

    before = read_text(readme)
    after, appended, normalization_events = append_missing_sections(before, repo.name, profile)
    deduped_after, removed_command_count = dedupe_skills_add_lines(after)
    after = deduped_after

    changed = after != before
    if not changed:
        return False, fixes, "no bounded fix applied"

    write_text(readme, after)

    if normalization_events:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "normalize-misnamed-headings",
                "status": "applied",
                "reason": f"normalized {len(normalization_events)} heading(s)",
                "events": [event.to_dict() for event in normalization_events],
            }
        )
    if appended:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "append-missing-sections",
                "status": "applied",
                "reason": f"bounded section insertion: {', '.join(appended)}",
            }
        )
    if removed_command_count > 0:
        fixes.append(
            {
                "repo": repo.name,
                "file": str(readme),
                "rule": "dedupe-install-commands",
                "status": "applied",
                "reason": f"removed {removed_command_count} duplicate install command line(s)",
            }
        )

    return True, fixes, None


def summarize_markdown(report: Dict[str, object]) -> str:
    lines: List[str] = []
    rc = report["run_context"]
    lines.append("## Run Context")
    lines.append(f"- Timestamp: {rc['timestamp_utc']}")
    lines.append(f"- Workspace: {rc['workspace']}")
    lines.append(f"- Repo glob: {rc['repo_glob']}")
    lines.append(f"- Apply fixes: {rc['apply_fixes']}")
    lines.append("")

    lines.append("## Discovery Summary")
    lines.append(f"- Repos scanned: {len(report['repos_scanned'])}")
    lines.append(f"- Repos with issues: {len(report['repos_with_issues'])}")
    lines.append("")

    lines.append("## Profile Assignments")
    for name, profile in sorted(report["profile_assignments"].items()):
        lines.append(f"- {name}: {profile}")
    lines.append("")

    lines.append("## Schema Violations")
    if not report["schema_violations"]:
        lines.append("- None")
    else:
        for i in report["schema_violations"]:
            lines.append(f"- [{i['severity']}] {i['repo']}: {i['evidence']}")
    lines.append("")

    lines.append("## Command Integrity Issues")
    if not report["command_integrity_issues"]:
        lines.append("- None")
    else:
        for i in report["command_integrity_issues"]:
            lines.append(f"- [{i['severity']}] {i['repo']}: {i['evidence']}")
    lines.append("")

    lines.append("## Fixes Applied")
    if not report["fixes_applied"]:
        lines.append("- None")
    else:
        for f in report["fixes_applied"]:
            lines.append(f"- [{f['status']}] {f['repo']} -> {f['file']} ({f['rule']})")
    lines.append("")

    lines.append("## Post-Fix Status")
    ps = report["post_fix_status"]
    lines.append(f"- Unresolved issues: {ps['unresolved_issues']}")
    lines.append(f"- Resolved issues: {ps['resolved_issues']}")
    lines.append("")

    lines.append("## Errors")
    if not report["errors"]:
        lines.append("- None")
    else:
        for e in report["errors"]:
            lines.append(f"- {e['repo']}: {e['message']}")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists() or not workspace.is_dir():
        print(f"Workspace path invalid: {workspace}", file=sys.stderr)
        return 1

    excludes = read_excludes(args.exclude)
    repos = discover_repos(workspace, args.repo_glob, excludes)

    profile_assignments: Dict[str, str] = {}
    schema_issues: List[Issue] = []
    command_issues: List[Issue] = []
    errors: List[Dict[str, str]] = []
    fixes_applied: List[Dict[str, object]] = []

    for repo in repos:
        profile = detect_profile(repo.name)
        profile_assignments[repo.name] = profile

        readme = repo / "README.md"
        skill_dirs = find_skill_dirs(repo)

        if not readme.exists():
            schema_issues.append(
                Issue(
                    issue_id="missing-readme",
                    category="schema-violation",
                    severity="high",
                    repo=repo.name,
                    doc_file=str(readme),
                    evidence="README.md is missing.",
                    recommended_fix="Create README using profile-appropriate template.",
                    auto_fixable=(profile == "bootstrap"),
                )
            )
            continue

        text = read_text(readme)
        schema_issues.extend(check_sections(repo, profile, text))
        schema_issues.extend(find_todo_issues(repo, text))
        schema_issues.extend(check_links(repo, text))
        command_issues.extend(check_commands(repo, profile, text, skill_dirs))

    initial_unresolved = len(schema_issues) + len(command_issues)

    if args.apply_fixes:
        for repo in repos:
            profile = profile_assignments[repo.name]
            skill_dirs = find_skill_dirs(repo)
            try:
                changed, fixes, reason = apply_fixes_for_repo(repo, profile, skill_dirs)
                if fixes:
                    fixes_applied.extend(fixes)
                elif reason:
                    fixes_applied.append({"repo": repo.name, "file": str(repo / "README.md"), "rule": "no-op", "status": "skipped", "reason": reason})
                if changed:
                    # Re-evaluate repo after fix.
                    readme = repo / "README.md"
                    text = read_text(readme)
                    schema_issues = [i for i in schema_issues if i.repo != repo.name]
                    command_issues = [i for i in command_issues if i.repo != repo.name]
                    schema_issues.extend(check_sections(repo, profile, text))
                    schema_issues.extend(find_todo_issues(repo, text))
                    schema_issues.extend(check_links(repo, text))
                    command_issues.extend(check_commands(repo, profile, text, skill_dirs))
            except Exception as exc:
                errors.append({"repo": repo.name, "message": f"fix error: {exc}"})

    unresolved = len(schema_issues) + len(command_issues)

    repos_with_issues = sorted({i.repo for i in schema_issues + command_issues})

    report: Dict[str, object] = {
        "run_context": {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "workspace": str(workspace),
            "repo_glob": args.repo_glob,
            "apply_fixes": args.apply_fixes,
            "exclusions": [str(e) for e in excludes],
        },
        "repos_scanned": [str(r) for r in repos],
        "profile_assignments": profile_assignments,
        "schema_violations": [i.to_dict() for i in schema_issues],
        "command_integrity_issues": [i.to_dict() for i in command_issues],
        "repos_with_issues": repos_with_issues,
        "fixes_applied": fixes_applied,
        "post_fix_status": {
            "initial_issues": initial_unresolved,
            "unresolved_issues": unresolved,
            "resolved_issues": max(0, initial_unresolved - unresolved),
        },
        "errors": errors,
    }

    md_report = summarize_markdown(report)
    json_report = json.dumps(report, indent=2, sort_keys=True)

    if args.md_out:
        Path(args.md_out).expanduser().write_text(md_report, encoding="utf-8")
    if args.json_out:
        Path(args.json_out).expanduser().write_text(json_report + "\n", encoding="utf-8")
    if args.print_md:
        print(md_report, end="")
    if args.print_json:
        print(json_report)

    if args.fail_on_issues and unresolved > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
