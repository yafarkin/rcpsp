"""Generate an HTML visualization for a schedule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

_TEMPLATE_PATH = Path(__file__).with_name("visualize_template.html")


def _load_template() -> str:
    with open(_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def visualize(json_path: Path, html_path: Path | None = None) -> None:
    """Generate an HTML file from a schedule JSON."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    template = _load_template()
    html = template.replace("__DATA__", json.dumps(data))

    if html_path is None:
        html_path = json_path.with_suffix(".html")

    with open(html_path, "w", encoding="utf-8") as out:
        out.write(html)
    print(f"Wrote visualization to {html_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize RCPSP schedule")
    parser.add_argument("schedule", type=Path, help="Schedule JSON file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output HTML file"
    )
    args = parser.parse_args()
    visualize(args.schedule, args.output)


if __name__ == "__main__":
    main()
