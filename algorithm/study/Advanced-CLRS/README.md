# Advanced-CLRS

이 트랙은 CLRS 고급 챕터를 repo-authored study project로 재구성한 심화 학습 트랙이다. Core처럼 BOJ 문제를 옮기는 대신, 각 챕터의 핵심 알고리즘이나 proof workflow를 재현 가능한 입력/출력 프로젝트로 바꿨다.

## Why This Track Exists

- Core에서 다룬 구현형 문제를 넘어 CLRS의 이론-heavy 주제를 직접 다룬다.
- 증명, 불변식, 자료구조 인터페이스, verifier/approximation 같은 주제를 runnable artifact로 남긴다.
- 너무 넓은 원안 슬롯은 학습 가능한 프로젝트 단위로 좁혀서 track 전체를 완성했다.

## Project Set

| Slot | Project | CLRS | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 0x10 | [Strassen Matrix Multiplication](0x10-strassen-matrix/README.md) | Ch 4 | Verified | divide and conquer + padding |
| 0x11 | [Amortized Analysis Lab](0x11-amortized-analysis-lab/README.md) | Ch 17 | Verified | MULTIPOP + binary counter |
| 0x12 | [Red-Black Tree Insert and Validate](0x12-red-black-tree/README.md) | Ch 13, 18 | Verified | B-tree is kept as docs follow-up |
| 0x13 | [Meldable Heap Bridge](0x13-meldable-heap/README.md) | Ch 19 | Verified | pairing heap bridge before Fibonacci heap notes |
| 0x14 | [Network Flow with Edmonds-Karp](0x14-network-flow/README.md) | Ch 26 | Verified | deterministic augmenting-path variant |
| 0x15 | [Advanced String Matching](0x15-string-matching/README.md) | Ch 32 | Verified | KMP and Rabin-Karp under one CLI |
| 0x16 | [Computational Geometry Lab](0x16-computational-geometry/README.md) | Ch 33 | Verified | hull + segment intersection |
| 0x17 | [Number Theory Lab](0x17-number-theory-lab/README.md) | Ch 31 | Verified | extended GCD, CRT, toy RSA |
| 0x18 | [NP-Completeness Lab](0x18-np-completeness-lab/README.md) | Ch 34 | Verified | certificate verification, not fake exact solvers |
| 0x19 | [Approximation Algorithms Lab](0x19-approximation-lab/README.md) | Ch 35 | Verified | set cover + vertex cover approximation |

## Redesign Decisions

- `0x12`: 원안의 red-black tree와 B-tree를 한 프로젝트에 모두 구현하는 것은 범위가 과해서, 구현은 red-black tree insertion/validation에 집중하고 B-tree는 docs reading path로 남겼다.
- `0x13`: raw Fibonacci heap 구현 대신 pairing heap 기반 meld lab으로 바꿨다. 핵심 인터페이스를 먼저 잡고 docs에서 Fibonacci heap으로 연결하는 편이 학습 효율이 높다.
- `0x18`: NP-completeness는 solver보다 verifier와 reduction 사고가 우선이라서 certificate verification lab으로 바꿨다.

## Policy

- 모든 advanced 프로젝트는 Python 구현과 fixture 기반 검증을 제공한다.
- C++는 현재 유지하지 않는다. 이 트랙의 목표는 low-level optimization보다 개념적 정확성과 재현 가능한 reasoning이다.
- 각 프로젝트는 `problem/`, `python/`, `docs/`, `notion/` 구조를 사용한다.
