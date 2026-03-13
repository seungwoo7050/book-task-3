# BOJ 11657 — 타임머신

> `Core-0C-Shortest-Path` 트랙의 Gold 프로젝트.

## 이 시리즈가 다루는 질문

- 문제: `타임머신`
- 트랙: `Core-0C-Shortest-Path`
- 한 줄 답: `N-1회 완화 + 추가 1회 검사로 음수 사이클을 판정하는 Bellman-Ford`

## Source-of-truth

- 프로젝트 README: [../../../Core-0C-Shortest-Path/11657/README.md](../../../Core-0C-Shortest-Path/11657/README.md)
- 접근 근거: [../../../Core-0C-Shortest-Path/11657/docs/references/approach.md](../../../Core-0C-Shortest-Path/11657/docs/references/approach.md)
- Python 구현: [../../../Core-0C-Shortest-Path/11657/python/src/solution.py](../../../Core-0C-Shortest-Path/11657/python/src/solution.py)
- C++ 비교 구현: [../../../Core-0C-Shortest-Path/11657/cpp/src/solution.cpp](../../../Core-0C-Shortest-Path/11657/cpp/src/solution.cpp)

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md) — 문제 이해부터 첫 구현까지
2. [20-development-timeline.md](20-development-timeline.md) — 검증, edge case, 정리까지

## 고정 검증 명령

```bash
$ make -C study/Core-0C-Shortest-Path/11657/problem run-py
$ make -C study/Core-0C-Shortest-Path/11657/problem run-cpp
$ make -C study/Core-0C-Shortest-Path/11657/problem test
```
