import pytest

pytest.importorskip("ortools")

from scheduler import Task, Resource, Scheduler


def test_schedule_respects_precedence_and_resources():
    tasks = [
        Task(id="T1", duration=2, demands={"res": 1}),
        Task(id="T2", duration=2, demands={"res": 1}, predecessors=["T1"]),
    ]
    resources = [Resource(id="res", capacity=1)]

    sched = Scheduler(tasks, resources)
    schedule = sched.solve()

    assert schedule["T2"]["start"] >= schedule["T1"]["end"]
    assert schedule["T1"]["end"] - schedule["T1"]["start"] == 2
    assert schedule["T2"]["end"] - schedule["T2"]["start"] == 2
