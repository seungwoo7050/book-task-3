# 0x15 — Advanced String Matching

| Item | Detail |
| :--- | :--- |
| Track | `Advanced-CLRS` |
| Slot | `0x15` |
| Type | Advanced study project |
| CLRS | Ch 32 |
| Legacy Source | `legacy/README.md` Advanced Track roadmap |
| Project Focus | KMP prefix function and Rabin-Karp rolling hash under one interface |

## Summary

문자열 매칭을 failure function과 rolling hash라는 두 관점에서 비교한다.

이 프로젝트는 BOJ 문제가 아니라 CLRS 주제를 직접 재현 가능한 입력/출력 문제로 바꾼 study project다.

## Curriculum Note

한 문제 형식에서 두 알고리즘을 모두 실행할 수 있게 해서, correctness는 동일 출력으로 비교하고 내부 메커니즘은 docs에서 분리했다.

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
