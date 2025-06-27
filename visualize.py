import json
from pathlib import Path
import argparse


def visualize(path: Path) -> None:
    """Simple visualization of the schedule."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("schedule", []):
        print(f"Task {item['id']} : start={item['start']} end={item['end']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize RCPSP schedule")
    parser.add_argument("schedule", type=Path, help="Schedule JSON file")
    args = parser.parse_args()
    visualize(args.schedule)


if __name__ == "__main__":
    main()
