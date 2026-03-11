from __future__ import annotations

from pathlib import Path

from os_scheduling import load_fixture, simulate_policy


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = PROJECT_ROOT / "problem" / "data"


def test_convoy_golden_timelines() -> None:
    specs = load_fixture(FIXTURE_DIR / "convoy.json")
    assert simulate_policy("fcfs", specs).timeline == (
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P2",
        "P2",
        "P2",
        "P2",
        "P3",
        "P3",
    )
    assert simulate_policy("sjf", specs).timeline == (
        "P3",
        "P3",
        "P2",
        "P2",
        "P2",
        "P2",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
        "P1",
    )
    assert simulate_policy("rr", specs).timeline == (
        "P1",
        "P1",
        "P2",
        "P2",
        "P3",
        "P3",
        "P1",
        "P1",
        "P2",
        "P2",
        "P1",
        "P1",
        "P1",
        "P1",
    )
    assert simulate_policy("mlfq", specs).timeline == (
        "P1",
        "P2",
        "P3",
        "P1",
        "P1",
        "P2",
        "P2",
        "P3",
        "P1",
        "P1",
        "P1",
        "P1",
        "P2",
        "P1",
    )


def test_sjf_reduces_waiting_time_on_convoy_fixture() -> None:
    specs = load_fixture(FIXTURE_DIR / "convoy.json")
    fcfs = simulate_policy("fcfs", specs)
    sjf = simulate_policy("sjf", specs)
    assert sjf.averages["waiting"] < fcfs.averages["waiting"]


def test_rr_improves_response_time_on_convoy_fixture() -> None:
    specs = load_fixture(FIXTURE_DIR / "convoy.json")
    fcfs = simulate_policy("fcfs", specs)
    rr = simulate_policy("rr", specs)
    assert rr.averages["response"] < fcfs.averages["response"]


def test_mlfq_handles_interactive_mix() -> None:
    specs = load_fixture(FIXTURE_DIR / "interactive-mix.json")
    fcfs = simulate_policy("fcfs", specs)
    mlfq = simulate_policy("mlfq", specs)
    assert mlfq.averages["response"] < fcfs.averages["response"]
