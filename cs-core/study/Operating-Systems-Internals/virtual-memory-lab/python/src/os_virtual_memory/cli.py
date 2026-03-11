from __future__ import annotations

import argparse

from .core import POLICIES, load_trace, render_replay, render_summary, simulate_policy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replay page replacement policies.")
    parser.add_argument("--trace", required=True, help="Path to the trace file.")
    parser.add_argument("--frames", required=True, type=int, help="Number of frames.")
    parser.add_argument(
        "--policy",
        default="all",
        choices=[*POLICIES, "all"],
        help="Policy to simulate.",
    )
    parser.add_argument("--replay", action="store_true", help="Print step-by-step replay.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    trace = load_trace(args.trace)
    policies = POLICIES if args.policy == "all" else (args.policy,)
    results = [simulate_policy(policy, trace, args.frames) for policy in policies]
    if args.replay:
        for result in results:
            print(f"[{result.policy}]")
            print(render_replay(result))
    print(render_summary(results))
    return 0
