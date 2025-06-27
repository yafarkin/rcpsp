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


def test_complex_project_smoke():
    resources = [
        Resource(id="BA", capacity=1),
        Resource(id="DEV_BE", capacity=3),
        Resource(id="DEV_FE", capacity=1),
        Resource(id="QA", capacity=1),
    ]

    tasks = [
        Task(id="T1", duration=2, demands={"BA": 1}),
        Task(id="T2", duration=3, demands={"DEV_BE": 1}, predecessors=["T1"]),
        Task(id="T3", duration=2, demands={"DEV_FE": 1}, predecessors=["T1"]),
        Task(id="T4", duration=4, demands={"DEV_BE": 1}, predecessors=["T2"]),
        Task(id="T5", duration=3, demands={"DEV_BE": 1}, predecessors=["T2"]),
        Task(id="T6", duration=3, demands={"DEV_FE": 1}, predecessors=["T3"]),
        Task(
            id="T7",
            duration=2,
            demands={"QA": 1},
            predecessors=["T4", "T5", "T6"],
        ),
        # Independent tasks
        Task(id="T8", duration=1, demands={"DEV_BE": 1}),
        Task(id="T9", duration=2, demands={"DEV_BE": 1}),
        Task(id="T10", duration=2, demands={"DEV_BE": 1}),
        Task(id="T11", duration=2, demands={"DEV_FE": 1}),
        Task(id="T12", duration=1, demands={"QA": 1}),
        Task(id="T13", duration=2, demands={"QA": 1}),
        Task(id="T14", duration=1, demands={"BA": 1}),
        Task(id="T15", duration=2, demands={"BA": 1}),
    ]

    sched = Scheduler(tasks, resources)
    schedule = sched.solve()

    assert set(schedule.keys()) == {t.id for t in tasks}

    task_map = {t.id: t for t in tasks}
    for tid, times in schedule.items():
        assert times["end"] - times["start"] == task_map[tid].duration
        assert times["start"] >= 0

    assert schedule["T2"]["start"] >= schedule["T1"]["end"]
    assert schedule["T3"]["start"] >= schedule["T1"]["end"]
    assert schedule["T4"]["start"] >= schedule["T2"]["end"]
    assert schedule["T5"]["start"] >= schedule["T2"]["end"]
    assert schedule["T6"]["start"] >= schedule["T3"]["end"]
    assert schedule["T7"]["start"] >= max(
        schedule["T4"]["end"], schedule["T5"]["end"], schedule["T6"]["end"]
    )

    # verify resource capacities are respected
    horizon = max(v["end"] for v in schedule.values())
    caps = {r.id: r.capacity for r in resources}
    for t in range(horizon):
        usage = {r.id: 0 for r in resources}
        for tid, times in schedule.items():
            if times["start"] <= t < times["end"]:
                for r_id, demand in task_map[tid].demands.items():
                    usage[r_id] += demand
        for r_id, used in usage.items():
            assert used <= caps[r_id]
