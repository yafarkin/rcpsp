# RCPSP Solver

This repository contains a simple implementation of the Resource-Constrained Project Scheduling Problem (RCPSP) solver. The solver reads a project description from a JSON file, evaluates resource constraints and activity precedence relations and then produces a feasible schedule.

## Installation

1. Clone this repository.
2. Ensure you have Python 3.8 or higher installed.
3. (Optional) Create a virtual environment.
4. Install any required packages:
   ```bash
   pip install -r requirements.txt
   ```
   The solver does not rely on heavy dependencies, so the requirements file may be minimal.

## Input format

The solver expects a JSON file describing available resources and the list of activities. Each activity specifies its duration, the resources it consumes and the list of successor activities that cannot start until the activity finishes.

Example:

```json
{
  "resources": [
    {"id": "workers", "capacity": 2},
    {"id": "machine", "capacity": 1}
  ],
  "activities": [
    {
      "id": 1,
      "duration": 1,
      "resources": {"workers": 1},
      "successors": [2, 3]
    },
    {
      "id": 2,
      "duration": 2,
      "resources": {"workers": 1, "machine": 1},
      "successors": [4]
    },
    {
      "id": 3,
      "duration": 2,
      "resources": {"workers": 2},
      "successors": [4]
    },
    {
      "id": 4,
      "duration": 1,
      "resources": {"machine": 1},
      "successors": []
    }
  ]
}
```

A copy of this example can be found at `examples/input.json`.

## Running the solver

Assuming the solver entry point is `solver.py`, run the following command:

```bash
python solver.py examples/input.json
```

The program will output a schedule listing the start time of each activity. The precise output format depends on the implementation, but typically it might look like:

```
Activity 1 starts at t=0
Activity 2 starts at t=1
Activity 3 starts at t=1
Activity 4 starts at t=3
```

This means activities 1, 2 and 3 start as soon as resource constraints allow, and activity 4 begins once its predecessors complete.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

