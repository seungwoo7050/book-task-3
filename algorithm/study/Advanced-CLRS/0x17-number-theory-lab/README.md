# 0x17 — Number Theory Lab

| Item | Detail |
| :--- | :--- |
| Track | `Advanced-CLRS` |
| Slot | `0x17` |
| Type | Advanced study project |
| CLRS | Ch 31 |
| Legacy Source | `legacy/README.md` Advanced Track roadmap |
| Project Focus | Extended GCD, CRT, and toy RSA in one reproducible interface |

## Summary

Euclidean algorithm에서 CRT와 RSA toy demo까지 자연스럽게 올라가는 숫자론 브리지 프로젝트다.

이 프로젝트는 BOJ 문제가 아니라 CLRS 주제를 직접 재현 가능한 입력/출력 문제로 바꾼 study project다.

## Curriculum Note

암호학 전체를 다루지 않고, CLRS Ch 31의 algebraic primitives가 어떻게 연결되는지에 집중한다.

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
