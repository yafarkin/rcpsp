import json
from pathlib import Path
from typing import Dict, List

from .data import Task


def write_schedule(path: Path, tasks: List[Task], schedule: Dict[str, Dict[str, int]]) -> None:
    """Write schedule to JSON file."""
    data = {
        "schedule": [
            {"id": t.id, "start": schedule[t.id]["start"], "end": schedule[t.id]["end"]}
            for t in tasks
        ]
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
