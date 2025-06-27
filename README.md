# RCPSP Solver

This repository contains a simple implementation of the Resource-Constrained Project Scheduling Problem (RCPSP) solver. The solver reads a project description from a JSON file, evaluates resource constraints and task precedence relations and then produces a feasible schedule.

## Installation

1. Clone this repository.
2. Ensure you have Python 3.8 or higher installed.
3. (Optional) Create a virtual environment.
4. Install the package and its dependencies using `pip`:
   ```bash
   pip install -e .
   ```

## Input format

The solver expects a JSON file describing available resources and the list of tasks. Each task specifies its duration, the resources it consumes and the list of predecessor tasks that must finish before it can start.

Example:

```json
{
  "resources": [
    {"id": "workers", "capacity": 2},
    {"id": "machine", "capacity": 1}
  ],
  "tasks": [
    {
      "id": "1",
      "duration": 1,
      "demands": {"workers": 1},
      "predecessors": []
    },
    {
      "id": "2",
      "duration": 2,
      "demands": {"workers": 1, "machine": 1},
      "predecessors": ["1"]
    },
    {
      "id": "3",
      "duration": 2,
      "demands": {"workers": 2},
      "predecessors": ["1"]
    },
    {
      "id": "4",
      "duration": 1,
      "demands": {"machine": 1},
      "predecessors": ["2", "3"]
    }
  ]
}
```

A copy of this example can be found at `examples/input.json`.

## Running the solver

To solve the example project and write the resulting schedule to `examples/output.json` run:

```bash
python main.py examples/input.json examples/output.json
```

After generating the schedule a simple HTML visualization will also be produced in the same directory.  The program prints the start and end time of each task, typically like:

```
Task 1 starts at t=0
Task 2 starts at t=1
Task 3 starts at t=1
Task 4 starts at t=3
```

This means tasks 1, 2 and 3 start as soon as resource constraints allow, and task 4 begins once its predecessors complete.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

