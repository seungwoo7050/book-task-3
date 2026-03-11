from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable


POLICIES = ("fifo", "lru", "clock", "opt")


@dataclass(frozen=True)
class PageAccess:
    mode: str
    page: int


@dataclass
class Frame:
    page: int
    dirty: bool
    loaded_at: int
    last_used: int
    referenced: bool = True


@dataclass(frozen=True)
class ReplayStep:
    index: int
    access: PageAccess
    hit: bool
    evicted: int | None
    dirty_eviction: bool
    snapshot: tuple[str, ...]


@dataclass(frozen=True)
class PolicyResult:
    policy: str
    frames: int
    steps: tuple[ReplayStep, ...]

    @property
    def faults(self) -> int:
        return sum(1 for step in self.steps if not step.hit)

    @property
    def hits(self) -> int:
        return sum(1 for step in self.steps if step.hit)

    @property
    def dirty_evictions(self) -> int:
        return sum(1 for step in self.steps if step.dirty_eviction)


def load_trace(path: str | Path) -> list[PageAccess]:
    accesses: list[PageAccess] = []
    for raw_line in Path(path).read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        mode, page = line.split()
        accesses.append(PageAccess(mode=mode, page=int(page)))
    return accesses


def simulate_policy(
    policy: str,
    accesses: Iterable[PageAccess],
    frame_count: int,
) -> PolicyResult:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    trace = list(accesses)
    frames: list[Frame] = []
    steps: list[ReplayStep] = []
    clock_hand = 0

    for index, access in enumerate(trace):
        hit_index = next((i for i, frame in enumerate(frames) if frame.page == access.page), None)
        evicted: int | None = None
        dirty_eviction = False
        if hit_index is not None:
            frame = frames[hit_index]
            frame.last_used = index
            frame.referenced = True
            if access.mode == "W":
                frame.dirty = True
            hit = True
        else:
            hit = False
            new_frame = Frame(
                page=access.page,
                dirty=access.mode == "W",
                loaded_at=index,
                last_used=index,
                referenced=True,
            )
            if len(frames) < frame_count:
                frames.append(new_frame)
            else:
                if policy == "fifo":
                    victim_index = min(range(len(frames)), key=lambda i: frames[i].loaded_at)
                elif policy == "lru":
                    victim_index = min(range(len(frames)), key=lambda i: frames[i].last_used)
                elif policy == "clock":
                    victim_index, clock_hand = _clock_select(frames, clock_hand)
                else:
                    victim_index = _opt_select(frames, trace, index + 1)
                victim = frames[victim_index]
                evicted = victim.page
                dirty_eviction = victim.dirty
                frames[victim_index] = new_frame
            if policy == "clock" and len(frames) <= frame_count:
                clock_hand %= len(frames)
        snapshot = tuple(_render_frame(frame) for frame in _sorted_frames(frames))
        steps.append(
            ReplayStep(
                index=index,
                access=access,
                hit=hit,
                evicted=evicted,
                dirty_eviction=dirty_eviction,
                snapshot=snapshot,
            )
        )
    return PolicyResult(policy=policy, frames=frame_count, steps=tuple(steps))


def _clock_select(frames: list[Frame], hand: int) -> tuple[int, int]:
    while True:
        frame = frames[hand]
        if frame.referenced:
            frame.referenced = False
            hand = (hand + 1) % len(frames)
            continue
        victim = hand
        hand = (hand + 1) % len(frames)
        return victim, hand


def _opt_select(frames: list[Frame], trace: list[PageAccess], start: int) -> int:
    future_pages = [access.page for access in trace[start:]]
    distances: list[tuple[int, int]] = []
    for index, frame in enumerate(frames):
        if frame.page not in future_pages:
            return index
        distances.append((future_pages.index(frame.page), index))
    return max(distances)[1]


def _render_frame(frame: Frame) -> str:
    suffix = "*" if frame.dirty else ""
    return f"{frame.page}{suffix}"


def _sorted_frames(frames: list[Frame]) -> list[Frame]:
    ordered = [replace(frame) for frame in frames]
    ordered.sort(key=lambda frame: frame.page)
    return ordered


def render_replay(result: PolicyResult) -> str:
    lines = ["idx access hit evicted dirty snapshot"]
    for step in result.steps:
        access = f"{step.access.mode}{step.access.page}"
        snapshot = "[" + ", ".join(step.snapshot) + "]"
        evicted = "-" if step.evicted is None else str(step.evicted)
        dirty = "yes" if step.dirty_eviction else "no"
        hit = "hit" if step.hit else "fault"
        lines.append(
            f"{step.index:>3} {access:>5} {hit:>5} {evicted:>7} {dirty:>5} {snapshot}"
        )
    return "\n".join(lines)


def render_summary(results: Iterable[PolicyResult]) -> str:
    lines = ["policy frames faults hits dirty_evictions"]
    for result in results:
        lines.append(
            f"{result.policy:>5} {result.frames:>6} {result.faults:>6} {result.hits:>4} {result.dirty_evictions:>15}"
        )
    return "\n".join(lines)
