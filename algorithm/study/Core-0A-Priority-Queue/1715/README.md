# BOJ 1715 — Card Sorting (카드 정렬하기)

| Item | Detail |
| :--- | :--- |
| Track | `Core-0A-Priority-Queue` |
| Legacy Source | `legacy/core/0A-priority-queue/gold-1715` |
| Tier | Gold |
| CLRS | Ch 6, 19 |
| Problem URL | https://www.acmicpc.net/problem/1715 |

## Summary

$N$ 개의 카드 묶음이 있다. 두 묶음을 합칠 때 비교 횟수는 두 묶음 크기의 합이다. 모든 묶음을 하나로 합칠 때 필요한 최소 비교 횟수를 구하라.

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
