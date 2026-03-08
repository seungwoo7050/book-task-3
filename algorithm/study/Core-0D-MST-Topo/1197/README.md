# BOJ 1197 — 최소 스패닝 트리

| Item | Detail |
| :--- | :--- |
| Track | `Core-0D-MST-Topo` |
| Legacy Source | `legacy/core/0D-mst-topo/silver-1197` |
| Tier | Silver |
| CLRS | Ch 23, 22.4 |
| Problem URL | https://www.acmicpc.net/problem/1197 |

## Summary

무방향 가중 그래프가 주어졌을 때, 최소 스패닝 트리의 가중치 합을 구하라.

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
