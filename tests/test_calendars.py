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

def test_parse_global_and_resource_calendars(tmp_path: Path):
    data = {
        "tasks": [],
        "resources": [],
        "calendars": [
            {"id": "global", "working_hours": 6},
            {"id": "machine", "working_hours": 10}
        ]
    }
    file = tmp_path / "input.json"
    file.write_text(json.dumps(data))

    _, _, calendars = load_json(file)

    assert len(calendars) == 2
    ids = {c.id for c in calendars}
    assert {"global", "machine"} == ids
    hours = {c.id: c.working_hours for c in calendars}
    assert hours["global"] == 6
    assert hours["machine"] == 10
