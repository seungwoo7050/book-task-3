#!/usr/bin/env python3
"""driver.py - Simplified Performance Lab helper."""

import subprocess
import sys


def run_part_a():
    tests = [
        ("-s 1 -E 1 -b 1 -t data/traces/study.trace", "study"),
    ]
    print("=== Part A: Cache Simulator ===")
    for args, name in tests:
        cmd = f"./csim {args}"
        print(f"  Testing {name}: {cmd}")
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=10)
            print(f"    {result.stdout.strip()}")
        except FileNotFoundError:
            print("    csim not found. Run the active implementation in study/c or study/cpp.")


def run_part_b():
    print("\n=== Part B: Matrix Transpose ===")
    print("  Use the active implementation benchmarks in study/c or study/cpp.")


if __name__ == "__main__":
    if "-A" in sys.argv:
        run_part_a()
    elif "-B" in sys.argv:
        run_part_b()
    else:
        run_part_a()
        run_part_b()
