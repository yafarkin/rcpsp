from pathlib import Path
import argparse

from scheduler import load_json, Scheduler, write_schedule


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RCPSP scheduler")
    parser.add_argument("input", type=Path, help="Input JSON file")
    parser.add_argument("output", type=Path, help="Output JSON file")
    args = parser.parse_args()

    tasks, resources, _ = load_json(args.input)
    sched = Scheduler(tasks, resources)
    schedule = sched.solve()
    write_schedule(args.output, tasks, schedule)


if __name__ == "__main__":
    main()
