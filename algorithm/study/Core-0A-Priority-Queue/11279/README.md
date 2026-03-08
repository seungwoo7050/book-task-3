# BOJ 11279 — Max Heap

| Item | Detail |
| :--- | :--- |
| Track | `Core-0A-Priority-Queue` |
| Legacy Source | `legacy/core/0A-priority-queue/bronze-11279` |
| Tier | Bronze |
| CLRS | Ch 6, 19 |
| Problem URL | https://www.acmicpc.net/problem/11279 |

## Summary

Implement a max-heap supporting two operations: **Insert** a natural number $x$. **Extract** and print the maximum value (print 0 if the heap is empty).

문제 원문과 starter 자료는 `problem/`에만 두고, 사용자 구현은 `python/`로 분리했다.

## Structure

- `problem/`: 원문 문제 설명, starter code, fixture, 실행 스크립트
- `python/`: 기본 해설 구현과 실행 메모
- `docs/`: 공개 학습 노트와 검증 참조
- `notion/`: 로컬 전용 기술 노트

## Verify

- `make -C problem test`로 Python fixture 테스트를 실행한다.
- `make -C problem run-py`로 대표 입력을 수동 실행한다.
- C++ 구현은 이 프로젝트 범위에서 유지하지 않는다.

## Status

- Python: verified against migrated fixtures on 2026-03-07
- C++: not retained by repository policy
- Legacy tree: preserved read-only under `legacy/`
