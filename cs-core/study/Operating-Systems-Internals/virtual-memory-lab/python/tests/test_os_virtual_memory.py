from __future__ import annotations

from pathlib import Path

from os_virtual_memory import load_trace, simulate_policy


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRACE_DIR = PROJECT_ROOT / "problem" / "data"


def test_fifo_belady_anomaly() -> None:
    trace = load_trace(TRACE_DIR / "belady.trace")
    fifo_3 = simulate_policy("fifo", trace, 3)
    fifo_4 = simulate_policy("fifo", trace, 4)
    assert fifo_3.faults == 9
    assert fifo_4.faults == 10


def test_locality_trace_favors_lru_and_opt() -> None:
    trace = load_trace(TRACE_DIR / "locality.trace")
    fifo = simulate_policy("fifo", trace, 3)
    lru = simulate_policy("lru", trace, 3)
    opt = simulate_policy("opt", trace, 3)
    assert lru.faults <= fifo.faults
    assert opt.faults <= lru.faults


def test_dirty_evictions_counted() -> None:
    trace = load_trace(TRACE_DIR / "dirty.trace")
    fifo = simulate_policy("fifo", trace, 2)
    assert fifo.dirty_evictions == 1


def test_clock_replay_is_deterministic() -> None:
    trace = load_trace(TRACE_DIR / "belady.trace")
    clock = simulate_policy("clock", trace, 3)
    assert clock.steps[0].snapshot == ("1",)
    assert clock.steps[-1].snapshot
