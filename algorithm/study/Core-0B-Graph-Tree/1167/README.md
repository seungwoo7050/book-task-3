# BOJ 1167 — 트리의 지름

| Item | Detail |
| :--- | :--- |
| Track | `Core-0B-Graph-Tree` |
| Legacy Source | `legacy/core/0B-graph-tree/gold-1167` |
| Tier | Gold |
| CLRS | Ch 22-24 |
| Problem URL | https://www.acmicpc.net/problem/1167 |

## Summary

트리의 지름이란, 트리에서 임의의 두 정점 사이의 거리 중 가장 긴 것을 말한다. 트리의 지름을 구하라.

문제 원문과 starter 자료는 `problem/`에만 두고, 사용자 구현은 `python/`, `cpp/`로 분리했다.

## Structure

- `problem/`: 원문 문제 설명, starter code, fixture, 실행 스크립트
- `python/`: 기본 해설 구현과 실행 메모
- `cpp/`: 비교용 구현과 빌드 메모
- `docs/`: 공개 학습 노트와 검증 참조
- `notion/`: 로컬 전용 기술 노트

## Verify

- `make -C problem test`로 Python fixture 테스트를 실행한다.
- `make -C problem run-py`로 대표 입력을 수동 실행한다.
- `make -C problem run-cpp`로 C++ 비교 구현을 실행한다.

## Status

- Python: verified against migrated fixtures on 2026-03-07
- C++: verified comparison implementation retained
- Legacy tree: preserved read-only under `legacy/`
