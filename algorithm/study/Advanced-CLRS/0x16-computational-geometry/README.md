# 0x16 — Computational Geometry Lab

| Item | Detail |
| :--- | :--- |
| Track | `Advanced-CLRS` |
| Slot | `0x16` |
| Type | Advanced study project |
| CLRS | Ch 33 |
| Legacy Source | `legacy/README.md` Advanced Track roadmap |
| Project Focus | Segment intersection and convex hull under a shared geometry toolkit |

## Summary

orientation test를 중심으로 선분 교차와 convex hull을 함께 다룬다.

이 프로젝트는 BOJ 문제가 아니라 CLRS 주제를 직접 재현 가능한 입력/출력 문제로 바꾼 study project다.

## Curriculum Note

두 주제를 한 프로젝트에 묶은 이유는 orientation/cross product toolkit이 공통 기반이기 때문이다.

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
