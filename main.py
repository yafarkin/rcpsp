from pathlib import Path
import argparse
import subprocess
import sys

from scheduler import load_json, Scheduler, write_schedule


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RCPSP scheduler")
    parser.add_argument("input", type=Path, nargs="?", help="Input JSON file")
    parser.add_argument("output", type=Path, nargs="?", help="Output JSON file")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if input_path is None and output_path is None:
        default_in = Path("input.json")
        if default_in.exists():
            input_path = default_in
            output_path = Path("output.json")
        else:
            parser.error("input file is required")
    elif input_path is None or output_path is None:
        parser.error("both input and output files must be specified")

    tasks, resources, _ = load_json(input_path)
    sched = Scheduler(tasks, resources)
    schedule = sched.solve()
    write_schedule(output_path, tasks, schedule, resources)

    visualize_script = Path(__file__).with_name("visualize.py")
    if visualize_script.exists():
        subprocess.run(
            [sys.executable, str(visualize_script), str(output_path)],
            check=False,
        )


if __name__ == "__main__":
    main()
