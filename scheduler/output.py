import json
from pathlib import Path
from typing import Dict, List

from .data import Task, Resource


def write_schedule(
    path: Path,
    tasks: List[Task],
    schedule: Dict[str, Dict[str, int]],
    resources: List[Resource] | None = None,
) -> None:
    """Write schedule along with task and resource info to JSON file."""

    data = {
        "tasks": [
            {
                "id": t.id,
                "duration": t.duration,
                "demands": t.demands,
                "predecessors": t.predecessors,
            }
            for t in tasks
        ],
        "schedule": [
            {
                "id": t.id,
                "start": schedule[t.id]["start"],
                "end": schedule[t.id]["end"],
            }
            for t in tasks
        ],
    }

    if resources is not None:
        data["resources"] = [
            {
                "id": r.id,
                "capacity": r.capacity,
            }
            for r in resources
        ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
