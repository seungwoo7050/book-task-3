# BOJ 1167 — 트리의 지름

> `Core-0B-Graph-Tree` 트랙의 Gold 프로젝트.

## 이 시리즈가 다루는 질문

- 문제: `트리의 지름`
- 트랙: `Core-0B-Graph-Tree`
- 한 줄 답: `임의 정점에서 최원점 탐색 후 한 번 더 탐색하는 two-pass`

## Source-of-truth

- 프로젝트 README: [../../../Core-0B-Graph-Tree/1167/README.md](../../../Core-0B-Graph-Tree/1167/README.md)
- 접근 근거: [../../../Core-0B-Graph-Tree/1167/docs/references/approach.md](../../../Core-0B-Graph-Tree/1167/docs/references/approach.md)
- Python 구현: [../../../Core-0B-Graph-Tree/1167/python/src/solution.py](../../../Core-0B-Graph-Tree/1167/python/src/solution.py)
- C++ 비교 구현: [../../../Core-0B-Graph-Tree/1167/cpp/src/solution.cpp](../../../Core-0B-Graph-Tree/1167/cpp/src/solution.cpp)

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md) — 문제 이해부터 첫 구현까지
2. [20-development-timeline.md](20-development-timeline.md) — 검증, edge case, 정리까지

## 고정 검증 명령

```bash
$ make -C study/Core-0B-Graph-Tree/1167/problem run-py
$ make -C study/Core-0B-Graph-Tree/1167/problem run-cpp
$ make -C study/Core-0B-Graph-Tree/1167/problem test
```
