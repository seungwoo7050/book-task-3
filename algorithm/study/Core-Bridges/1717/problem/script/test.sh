#!/bin/bash
set -euo pipefail

PYTHON=python3
SOLUTION_PY="../../python/src/solution.py"
DATA_DIR="../data"

pass=0
fail=0
total=0

for input_file in "$DATA_DIR"/input*.txt; do
    test_num=$(basename "$input_file" | grep -o '[0-9]\+')
    expected_file="$DATA_DIR/output${test_num}.txt"

    if [ ! -f "$expected_file" ]; then
        continue
    fi

    total=$((total + 1))
    actual=$($PYTHON "$SOLUTION_PY" < "$input_file" | tr -d '\r')
    expected=$(cat "$expected_file" | tr -d '\r')

    if [ "$actual" = "$expected" ]; then
        echo "Test $test_num: PASS"
        pass=$((pass + 1))
    else
        echo "Test $test_num: FAIL"
        echo "  Expected: $expected"
        echo "  Actual:   $actual"
        fail=$((fail + 1))
    fi
done

echo ""
echo "Results: $pass/$total passed, $fail failed"
[ "$fail" -eq 0 ] && exit 0 || exit 1
