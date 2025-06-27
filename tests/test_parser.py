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


def test_load_json_complex_project(tmp_path: Path):
    data = {
        "tasks": [
            {"id": "T1", "duration": 2, "demands": {"BA": 1}},
            {"id": "T2", "duration": 3, "demands": {"DEV_BE": 1}, "predecessors": ["T1"]},
            {"id": "T3", "duration": 2, "demands": {"DEV_FE": 1}, "predecessors": ["T1"]},
            {"id": "T4", "duration": 4, "demands": {"DEV_BE": 1}, "predecessors": ["T2"]},
            {"id": "T5", "duration": 3, "demands": {"DEV_BE": 1}, "predecessors": ["T2"]},
            {"id": "T6", "duration": 3, "demands": {"DEV_FE": 1}, "predecessors": ["T3"]},
            {"id": "T7", "duration": 2, "demands": {"QA": 1}, "predecessors": ["T4", "T5", "T6"]},
            {"id": "T8", "duration": 1, "demands": {"DEV_BE": 1}},
            {"id": "T9", "duration": 2, "demands": {"DEV_BE": 1}},
            {"id": "T10", "duration": 2, "demands": {"DEV_BE": 1}},
            {"id": "T11", "duration": 2, "demands": {"DEV_FE": 1}},
            {"id": "T12", "duration": 1, "demands": {"QA": 1}},
            {"id": "T13", "duration": 2, "demands": {"QA": 1}},
            {"id": "T14", "duration": 1, "demands": {"BA": 1}},
            {"id": "T15", "duration": 2, "demands": {"BA": 1}},
        ],
        "resources": [
            {"id": "BA", "capacity": 1},
            {"id": "DEV_BE", "capacity": 3},
            {"id": "DEV_FE", "capacity": 1},
            {"id": "QA", "capacity": 1},
        ],
    }
    file = tmp_path / "input.json"
    file.write_text(json.dumps(data))

    tasks, resources, _ = load_json(file)

    assert len(tasks) == 15
    assert len(resources) == 4
    id_map = {t.id: t for t in tasks}
    assert id_map["T2"].predecessors == ["T1"]
    assert id_map["T7"].predecessors == ["T4", "T5", "T6"]
