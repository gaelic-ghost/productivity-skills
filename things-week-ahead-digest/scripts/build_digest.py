#!/usr/bin/env python3
"""Build a Things planning digest from exported MCP JSON responses."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--areas", required=True, help="Path to areas JSON")
    parser.add_argument("--projects", required=True, help="Path to projects JSON")
    parser.add_argument("--open-todos", required=True, help="Path to open todos JSON")
    parser.add_argument(
        "--recent-done",
        default="",
        help="Path to completed todos JSON (last 7 days preferred)",
    )
    parser.add_argument(
        "--detailed-todos",
        default="",
        help="Path to todo-detail JSON list with notes/checklist-like content",
    )
    parser.add_argument(
        "--days-ahead",
        type=int,
        default=4,
        help="How many days ahead to include in week/weekend view",
    )
    parser.add_argument(
        "--today",
        default="",
        help="Override date in YYYY-MM-DD (defaults to local today)",
    )
    return parser.parse_args()


def read_items(path: str) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return [item for item in payload["items"] if isinstance(item, dict)]
    raise ValueError(f"Unsupported JSON shape in {path}")


def parse_date(raw: str) -> date | None:
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def checklist_hint_score(notes: str) -> int:
    if not notes:
        return 0
    markers = ("- [ ]", "- [x]", "[ ]", "[x]", "\n- ", "\n* ", "\n1. ")
    score = sum(1 for marker in markers if marker in notes)
    if notes.count("\n") >= 4:
        score += 1
    return min(score, 3)


def short_task(task: dict[str, Any]) -> str:
    title = str(task.get("title") or "Untitled")
    project = str(task.get("project_title") or "")
    area = str(task.get("area_title") or "")
    if project:
        return f"{title} ({project})"
    if area:
        return f"{title} ({area})"
    return title


@dataclass
class Activity:
    title: str
    area_title: str = ""
    open_count: int = 0
    due_soon: int = 0
    overdue: int = 0
    completed_7d: int = 0
    checklist_hints: int = 0

    @property
    def score(self) -> float:
        return (
            self.completed_7d * 3
            + self.due_soon * 2
            + self.overdue * 3
            + min(self.open_count, 10) * 0.5
            + self.checklist_hints * 1.5
        )


def inc_activity(
    table: dict[str, Activity], key: str, title: str, area_title: str = ""
) -> Activity:
    entry = table.get(key)
    if entry is None:
        entry = Activity(title=title, area_title=area_title)
        table[key] = entry
    return entry


def render_digest(
    areas: list[dict[str, Any]],
    projects: list[dict[str, Any]],
    open_todos: list[dict[str, Any]],
    recent_done: list[dict[str, Any]],
    detailed_todos: list[dict[str, Any]],
    today: date,
    days_ahead: int,
) -> str:
    area_names = {str(a.get("id")): str(a.get("title") or "Unknown") for a in areas}
    project_names = {
        str(p.get("id")): str(p.get("title") or "Unknown Project") for p in projects
    }

    proj_activity: dict[str, Activity] = {}
    area_activity: dict[str, Activity] = {}
    open_by_project: dict[str, list[dict[str, Any]]] = defaultdict(list)

    overdue_count = 0
    due_soon_count = 0
    window_tasks: list[tuple[date, dict[str, Any]]] = []
    weekend_tasks = 0

    window_end = today + timedelta(days=days_ahead)

    for todo in open_todos:
        project_id = str(todo.get("project_id") or "")
        area_id = str(todo.get("area_id") or "")
        project_title = str(todo.get("project_title") or project_names.get(project_id) or "Unscoped")
        area_title = str(todo.get("area_title") or area_names.get(area_id) or "Unknown Area")

        due = parse_date(str(todo.get("deadline") or ""))
        if due is not None:
            if due < today:
                overdue_count += 1
            if due <= today + timedelta(days=3):
                due_soon_count += 1
            if today <= due <= window_end:
                window_tasks.append((due, todo))
                if due.weekday() >= 5:
                    weekend_tasks += 1

        p_key = project_id or f"project:{project_title}"
        p_entry = inc_activity(proj_activity, p_key, project_title, area_title)
        p_entry.open_count += 1
        if due and due < today:
            p_entry.overdue += 1
        if due and due <= today + timedelta(days=3):
            p_entry.due_soon += 1
        p_entry.checklist_hints += checklist_hint_score(str(todo.get("notes") or ""))

        a_key = area_id or f"area:{area_title}"
        a_entry = inc_activity(area_activity, a_key, area_title, area_title)
        a_entry.open_count += 1
        if due and due < today:
            a_entry.overdue += 1
        if due and due <= today + timedelta(days=3):
            a_entry.due_soon += 1
        a_entry.checklist_hints += checklist_hint_score(str(todo.get("notes") or ""))

        open_by_project[p_key].append(todo)

    for todo in recent_done:
        project_id = str(todo.get("project_id") or "")
        area_id = str(todo.get("area_id") or "")
        project_title = str(todo.get("project_title") or project_names.get(project_id) or "Unscoped")
        area_title = str(todo.get("area_title") or area_names.get(area_id) or "Unknown Area")

        p_key = project_id or f"project:{project_title}"
        inc_activity(proj_activity, p_key, project_title, area_title).completed_7d += 1
        a_key = area_id or f"area:{area_title}"
        inc_activity(area_activity, a_key, area_title, area_title).completed_7d += 1

    for todo in detailed_todos:
        project_id = str(todo.get("project_id") or "")
        area_id = str(todo.get("area_id") or "")
        project_title = str(todo.get("project_title") or project_names.get(project_id) or "Unscoped")
        area_title = str(todo.get("area_title") or area_names.get(area_id) or "Unknown Area")
        hint = checklist_hint_score(str(todo.get("notes") or ""))
        if hint <= 0:
            continue
        p_key = project_id or f"project:{project_title}"
        inc_activity(proj_activity, p_key, project_title, area_title).checklist_hints += hint
        a_key = area_id or f"area:{area_title}"
        inc_activity(area_activity, a_key, area_title, area_title).checklist_hints += hint

    top_projects = sorted(
        proj_activity.values(), key=lambda item: item.score, reverse=True
    )[:3]
    top_areas = sorted(
        area_activity.values(), key=lambda item: item.score, reverse=True
    )[:2]
    window_tasks.sort(key=lambda row: row[0])

    lines: list[str] = []
    lines.append(f"# Things Planning Digest - {today.isoformat()}")
    lines.append("")
    lines.append("## Snapshot")
    lines.append(f"- Open todos: {len(open_todos)}")
    lines.append(f"- Overdue: {overdue_count}")
    lines.append(f"- Due in next 72h: {due_soon_count}")
    lines.append(f"- Recently completed (7d): {len(recent_done)}")
    most_active_area = top_areas[0].title if top_areas else "None currently"
    lines.append(f"- Most active area: {most_active_area}")
    lines.append("")
    lines.append("## Recently Active")
    lines.append("### Projects")
    if not top_projects:
        lines.append("1. None currently")
    else:
        for idx, item in enumerate(top_projects, start=1):
            area_suffix = f" ({item.area_title})" if item.area_title else ""
            lines.append(
                f"{idx}. {item.title}{area_suffix} - "
                f"open:{item.open_count}, due soon:{item.due_soon}, "
                f"overdue:{item.overdue}, completed 7d:{item.completed_7d}"
            )
    lines.append("")
    lines.append("### Areas")
    if not top_areas:
        lines.append("1. None currently")
    else:
        for idx, item in enumerate(top_areas, start=1):
            lines.append(
                f"{idx}. {item.title} - open:{item.open_count}, due soon:{item.due_soon}, "
                f"overdue:{item.overdue}, completed 7d:{item.completed_7d}"
            )
    lines.append("")
    lines.append("## Week/Weekend Ahead")
    if not window_tasks:
        lines.append("- None currently")
    else:
        for due, todo in window_tasks[:8]:
            weekday = due.strftime("%a")
            lines.append(f"- {weekday} {due.isoformat()}: {short_task(todo)}")
    lines.append("")
    lines.append("## Suggestions")

    suggestions: list[str] = []
    if overdue_count > 0:
        suggestions.append(
            f"Triage {overdue_count} overdue todo(s) first and reschedule or complete each one today."
        )

    for item in top_projects[:2]:
        candidates = sorted(
            open_by_project.get(
                next(
                    (
                        key
                        for key, value in proj_activity.items()
                        if value.title == item.title and value.area_title == item.area_title
                    ),
                    "",
                ),
                [],
            ),
            key=lambda todo: parse_date(str(todo.get("deadline") or "")) or date.max,
        )
        if not candidates:
            continue
        task = candidates[0]
        task_title = str(task.get("title") or "a top task")
        suggestions.append(f"Start with '{task_title}' to move {item.title} forward today.")

    if weekend_tasks > 0:
        suggestions.append(
            "Block a weekend prep session for deadline-bound tasks due on Saturday or Sunday."
        )
    elif window_tasks:
        suggestions.append("Reserve a 30-minute planning pass for the next 4 days of deadlines.")

    checklist_total = sum(item.checklist_hints for item in top_projects)
    if checklist_total > 0:
        suggestions.append(
            "Split one checklist-heavy todo into smaller next actions to reduce context switching."
        )

    if not suggestions:
        suggestions.append("Pick one high-impact todo and complete it before adding new tasks.")

    for idx, suggestion in enumerate(suggestions[:5], start=1):
        lines.append(f"{idx}. {suggestion}")

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    today = (
        date.fromisoformat(args.today)
        if args.today
        else datetime.now().astimezone().date()
    )

    areas = read_items(args.areas)
    projects = read_items(args.projects)
    open_todos = read_items(args.open_todos)
    recent_done = read_items(args.recent_done) if args.recent_done else []
    detailed_todos = read_items(args.detailed_todos) if args.detailed_todos else []

    digest = render_digest(
        areas=areas,
        projects=projects,
        open_todos=open_todos,
        recent_done=recent_done,
        detailed_todos=detailed_todos,
        today=today,
        days_ahead=args.days_ahead,
    )
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
