# BOJ 1406 — Editor

| Item | Detail |
| :--- | :--- |
| Track | `Core-01-Array-List` |
| Legacy Source | `legacy/core/01-array-list/silver-1406` |
| Tier | Silver |
| CLRS | Ch 10.2 |
| Problem URL | https://www.acmicpc.net/problem/1406 |

## Summary

You have an initial string and a cursor positioned at the **end** of the string. Process $M$ commands:

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
