from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Deque, Iterable


POLICIES = ("fcfs", "sjf", "rr", "mlfq")


@dataclass(frozen=True)
class ProcessSpec:
    pid: str
    arrival: int
    burst: int


@dataclass
class ProcessState:
    pid: str
    arrival: int
    burst: int
    remaining: int
    level: int = 0
    start: int | None = None
    completion: int | None = None

    @classmethod
    def from_spec(cls, spec: ProcessSpec) -> "ProcessState":
        return cls(
            pid=spec.pid,
            arrival=spec.arrival,
            burst=spec.burst,
            remaining=spec.burst,
        )


@dataclass(frozen=True)
class ProcessMetric:
    pid: str
    waiting_time: int
    response_time: int
    turnaround_time: int


@dataclass(frozen=True)
class PolicyResult:
    policy: str
    timeline: tuple[str, ...]
    metrics: tuple[ProcessMetric, ...]

    @property
    def averages(self) -> dict[str, float]:
        count = len(self.metrics)
        return {
            "waiting": round(sum(item.waiting_time for item in self.metrics) / count, 2),
            "response": round(sum(item.response_time for item in self.metrics) / count, 2),
            "turnaround": round(
                sum(item.turnaround_time for item in self.metrics) / count,
                2,
            ),
        }


def load_fixture(path: str | Path) -> list[ProcessSpec]:
    data = json.loads(Path(path).read_text())
    specs = [ProcessSpec(**item) for item in data]
    for spec in specs:
        if spec.arrival < 0 or spec.burst <= 0:
            raise ValueError("arrival must be >= 0 and burst must be > 0")
    return specs


def simulate_policy(policy: str, specs: Iterable[ProcessSpec]) -> PolicyResult:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    states = [ProcessState.from_spec(spec) for spec in specs]
    if policy == "fcfs":
        timeline = _simulate_fcfs(states)
    elif policy == "sjf":
        timeline = _simulate_sjf(states)
    elif policy == "rr":
        timeline = _simulate_rr(states, quantum=2)
    else:
        timeline = _simulate_mlfq(states, quanta=(1, 2, 4), boost_interval=10)
    metrics = tuple(_build_metrics(states))
    return PolicyResult(policy=policy, timeline=tuple(timeline), metrics=metrics)


def _simulate_fcfs(states: list[ProcessState]) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    ready: Deque[ProcessState] = deque()
    time = 0
    timeline: list[str] = []

    while pending or ready:
        time = _maybe_fill_idle(timeline, time, pending, ready)
        _enqueue_arrivals(pending, ready, time)
        current = ready.popleft()
        if current.start is None:
            current.start = time
        for _ in range(current.remaining):
            timeline.append(current.pid)
            time += 1
        current.remaining = 0
        current.completion = time
        _enqueue_arrivals(pending, ready, time)
    return timeline


def _simulate_sjf(states: list[ProcessState]) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    ready: list[ProcessState] = []
    time = 0
    timeline: list[str] = []

    while pending or ready:
        time = _maybe_fill_idle(timeline, time, pending, ready)
        _enqueue_arrivals_list(pending, ready, time)
        ready.sort(key=lambda item: (item.remaining, item.arrival, item.pid))
        current = ready.pop(0)
        if current.start is None:
            current.start = time
        for _ in range(current.remaining):
            timeline.append(current.pid)
            time += 1
        current.remaining = 0
        current.completion = time
        _enqueue_arrivals_list(pending, ready, time)
    return timeline


def _simulate_rr(states: list[ProcessState], quantum: int) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    ready: Deque[ProcessState] = deque()
    time = 0
    timeline: list[str] = []

    while pending or ready:
        time = _maybe_fill_idle(timeline, time, pending, ready)
        _enqueue_arrivals(pending, ready, time)
        current = ready.popleft()
        if current.start is None:
            current.start = time
        run_ticks = min(quantum, current.remaining)
        for _ in range(run_ticks):
            timeline.append(current.pid)
            time += 1
            current.remaining -= 1
            _enqueue_arrivals(pending, ready, time)
        if current.remaining == 0:
            current.completion = time
        else:
            ready.append(current)
    return timeline


def _simulate_mlfq(
    states: list[ProcessState],
    quanta: tuple[int, ...],
    boost_interval: int,
) -> list[str]:
    pending = sorted(states, key=lambda item: (item.arrival, item.pid))
    queues = [deque() for _ in quanta]
    time = 0
    next_boost = boost_interval
    timeline: list[str] = []

    while pending or any(queues):
        time = _maybe_fill_idle(timeline, time, pending, queues)
        _enqueue_arrivals_mlfq(pending, queues, time)
        if time >= next_boost and any(queues):
            _boost_queues(queues)
            while next_boost <= time:
                next_boost += boost_interval
        level = _pick_level(queues)
        current = queues[level].popleft()
        if current.start is None:
            current.start = time
        current.level = level
        run_ticks = min(quanta[level], current.remaining)
        for _ in range(run_ticks):
            timeline.append(current.pid)
            time += 1
            current.remaining -= 1
            _enqueue_arrivals_mlfq(pending, queues, time)
        if current.remaining == 0:
            current.completion = time
            continue
        current.level = min(level + 1, len(quanta) - 1)
        queues[current.level].append(current)
    return timeline


def _maybe_fill_idle(timeline: list[str], time: int, pending: list[ProcessState], ready) -> int:
    has_ready = bool(ready)
    if has_ready or not pending:
        return time
    next_arrival = pending[0].arrival
    while time < next_arrival:
        timeline.append(".")
        time += 1
    return time


def _enqueue_arrivals(
    pending: list[ProcessState],
    ready: Deque[ProcessState],
    time: int,
) -> None:
    while pending and pending[0].arrival <= time:
        ready.append(pending.pop(0))


def _enqueue_arrivals_list(
    pending: list[ProcessState],
    ready: list[ProcessState],
    time: int,
) -> None:
    while pending and pending[0].arrival <= time:
        ready.append(pending.pop(0))


def _enqueue_arrivals_mlfq(
    pending: list[ProcessState],
    queues: list[Deque[ProcessState]],
    time: int,
) -> None:
    while pending and pending[0].arrival <= time:
        proc = pending.pop(0)
        proc.level = 0
        queues[0].append(proc)


def _pick_level(queues: list[Deque[ProcessState]]) -> int:
    for index, queue in enumerate(queues):
        if queue:
            return index
    raise RuntimeError("no runnable process")


def _boost_queues(queues: list[Deque[ProcessState]]) -> None:
    boosted = deque()
    for queue in queues:
        while queue:
            proc = queue.popleft()
            proc.level = 0
            boosted.append(proc)
    queues[0] = boosted
    for index in range(1, len(queues)):
        queues[index] = deque()


def _build_metrics(states: list[ProcessState]) -> list[ProcessMetric]:
    metrics: list[ProcessMetric] = []
    for state in sorted(states, key=lambda item: item.pid):
        if state.start is None or state.completion is None:
            raise RuntimeError("process did not complete")
        turnaround = state.completion - state.arrival
        waiting = turnaround - state.burst
        response = state.start - state.arrival
        metrics.append(
            ProcessMetric(
                pid=state.pid,
                waiting_time=waiting,
                response_time=response,
                turnaround_time=turnaround,
            )
        )
    return metrics


def render_replay(result: PolicyResult) -> str:
    segments: list[str] = []
    if not result.timeline:
        return "(empty)"
    start = 0
    current = result.timeline[0]
    for index, item in enumerate(result.timeline[1:], start=1):
        if item != current:
            segments.append(f"{start:02d}-{index - 1:02d}:{current}")
            start = index
            current = item
    segments.append(f"{start:02d}-{len(result.timeline) - 1:02d}:{current}")
    return " | ".join(segments)


def render_summary(results: Iterable[PolicyResult]) -> str:
    lines = ["policy waiting response turnaround"]
    for result in results:
        averages = result.averages
        lines.append(
            f"{result.policy:>5} {averages['waiting']:>7} {averages['response']:>8} {averages['turnaround']:>10}"
        )
    return "\n".join(lines)
