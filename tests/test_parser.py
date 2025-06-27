import json
from pathlib import Path
import importlib.util
import types
import sys

package_path = Path(__file__).resolve().parents[1] / "scheduler"
pkg = types.ModuleType("scheduler")
pkg.__path__ = [str(package_path)]
sys.modules.setdefault("scheduler", pkg)

_spec = importlib.util.spec_from_file_location(
    "scheduler.parser",
    package_path / "parser.py",
)
parser = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(parser)
load_json = parser.load_json

def test_load_json_with_hierarchy(tmp_path: Path):
    data = {
        "tasks": [
            {"id": "A", "duration": 2},
            {"id": "B", "duration": 3, "predecessors": ["A"]}
        ],
        "resources": [{"id": "r1", "capacity": 2}],
        "calendars": [{"id": "global", "working_hours": 8}]
    }
    file = tmp_path / "input.json"
    file.write_text(json.dumps(data))

    tasks, resources, calendars = load_json(file)

    assert len(tasks) == 2
    assert tasks[1].predecessors == ["A"]
    assert resources[0].id == "r1"
    assert calendars[0].id == "global"
