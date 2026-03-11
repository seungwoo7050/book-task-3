from __future__ import annotations

import argparse

from .core import POLICIES, load_fixture, render_replay, render_summary, simulate_policy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare scheduling policies on a fixture.")
    parser.add_argument("--fixture", required=True, help="Path to the JSON workload fixture.")
    parser.add_argument(
        "--policy",
        default="all",
        choices=[*POLICIES, "all"],
        help="Policy to simulate.",
    )
    parser.add_argument("--replay", action="store_true", help="Print ASCII replay.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    specs = load_fixture(args.fixture)
    policies = POLICIES if args.policy == "all" else (args.policy,)
    results = [simulate_policy(policy, specs) for policy in policies]
    if args.replay:
        for result in results:
            print(f"[{result.policy}]")
            print(render_replay(result))
    print(render_summary(results))
    return 0
