# 0x18 — NP-Completeness Lab

| Item | Detail |
| :--- | :--- |
| Track | `Advanced-CLRS` |
| Slot | `0x18` |
| Type | Advanced study project |
| CLRS | Ch 34 |
| Legacy Source | `legacy/README.md` Advanced Track roadmap |
| Project Focus | Certificate verification for vertex cover and 3-SAT plus reduction-oriented notes |

## Summary

NP-hard 문제를 억지로 푸는 대신, certificate verification과 reduction reading을 runnable lab 형태로 만든다.

이 프로젝트는 BOJ 문제가 아니라 CLRS 주제를 직접 재현 가능한 입력/출력 문제로 바꾼 study project다.

## Curriculum Note

NP-completeness는 solver보다 verifier와 reduction 사고가 우선이라서 certificate verification lab으로 바꿨다.

## Structure

- `problem/`: repo-authored specification, starter code, fixtures, 실행 스크립트
- `python/`: 기본 해설 구현과 실행 메모
- `docs/`: 공개 학습 노트와 검증 참조
- `notion/`: 로컬 전용 기술 노트

## Verify

- `make -C problem test`로 Python fixture 테스트를 실행한다.
- `make -C problem run-py`로 대표 입력을 수동 실행한다.
- C++ 구현은 이 프로젝트 범위에서 유지하지 않는다.

## Status

- Python: verified against repo-authored fixtures on 2026-03-08
- C++: not retained by repository policy
- Legacy tree: advanced roadmap preserved in `legacy/README.md`
