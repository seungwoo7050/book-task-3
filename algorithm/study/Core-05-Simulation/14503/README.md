# BOJ 14503 — Robot Vacuum Cleaner

| Item | Detail |
| :--- | :--- |
| Track | `Core-05-Simulation` |
| Legacy Source | `legacy/core/05-simulation/gold-14503` |
| Tier | Gold |
| CLRS | Implementation discipline |
| Problem URL | https://www.acmicpc.net/problem/14503 |

## Summary

A room is an $N \times M$ grid. Each cell is either empty (0) or a wall (1). A robot starts at position $(r, c)$ facing direction $d$ (0=North, 1=East, 2=South, 3=West).

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
