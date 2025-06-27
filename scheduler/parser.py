import json
from pathlib import Path
from typing import List

from .data import Task, Resource, Calendar


def load_json(path: Path) -> tuple[List[Task], List[Resource], List[Calendar]]:
    """Load tasks, resources and calendars from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tasks = [
        Task(
            id=t["id"],
            duration=t["duration"],
            demands=t.get("demands", {}),
            predecessors=t.get("predecessors", []),
        )
        for t in data.get("tasks", [])
    ]

    resources = [Resource(id=r["id"], capacity=r["capacity"]) for r in data.get("resources", [])]

    calendars = [
        Calendar(id=c.get("id"), working_hours=c.get("working_hours", 8))
        for c in data.get("calendars", [])
    ]

    return tasks, resources, calendars
