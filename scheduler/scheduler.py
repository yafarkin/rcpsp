from __future__ import annotations

from typing import Dict, List

from ortools.sat.python import cp_model

from .data import Task, Resource


class Scheduler:
    """Solve RCPSP using CP-SAT."""

    def __init__(self, tasks: List[Task], resources: List[Resource]):
        self.tasks = tasks
        self.resources = resources

    def solve(self) -> Dict[str, Dict[str, int]]:
        model = cp_model.CpModel()
        horizon = sum(t.duration for t in self.tasks)

        starts = {}
        ends = {}
        intervals = {}
        for task in self.tasks:
            start = model.NewIntVar(0, horizon, f"start_{task.id}")
            end = model.NewIntVar(0, horizon, f"end_{task.id}")
            interval = model.NewIntervalVar(start, task.duration, end, f"interval_{task.id}")
            starts[task.id] = start
            ends[task.id] = end
            intervals[task.id] = interval

        # Precedence constraints
        for task in self.tasks:
            for pred in task.predecessors:
                model.Add(starts[task.id] >= ends[pred])

        # Resource constraints
        for res in self.resources:
            demands = []
            ivs = []
            for task in self.tasks:
                if res.id in task.demands:
                    demands.append(task.demands[res.id])
                    ivs.append(intervals[task.id])
            if ivs:
                model.AddCumulative(ivs, demands, res.capacity)

        makespan = model.NewIntVar(0, horizon, "makespan")
        model.AddMaxEquality(makespan, [ends[t.id] for t in self.tasks])
        model.Minimize(makespan)

        solver = cp_model.CpSolver()
        result = solver.Solve(model)

        schedule = {}
        if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            for t in self.tasks:
                schedule[t.id] = {
                    "start": solver.Value(starts[t.id]),
                    "end": solver.Value(ends[t.id]),
                }
        return schedule
