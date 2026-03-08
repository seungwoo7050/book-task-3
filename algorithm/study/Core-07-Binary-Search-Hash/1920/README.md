# BOJ 1920 — Find Number

| Item | Detail |
| :--- | :--- |
| Track | `Core-07-Binary-Search-Hash` |
| Legacy Source | `legacy/core/07-binary-search-hash/bronze-1920` |
| Tier | Bronze |
| CLRS | Ch 11, 12.3 |
| Problem URL | https://www.acmicpc.net/problem/1920 |

## Summary

Given $N$ integers and $M$ query integers, for each query determine whether the integer exists in the $N$ integers. Print 1 if found, 0 otherwise.

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
