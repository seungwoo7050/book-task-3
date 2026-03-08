# BOJ 14891 — Gear

| Item | Detail |
| :--- | :--- |
| Track | `Core-05-Simulation` |
| Legacy Source | `legacy/core/05-simulation/silver-14891` |
| Tier | Silver |
| CLRS | Implementation discipline |
| Problem URL | https://www.acmicpc.net/problem/14891 |

## Summary

There are 4 gears, each with 8 teeth arranged in a circle. Each tooth is either N-pole (0) or S-pole (1). The teeth are numbered 0–7 clockwise starting from the 12 o'clock position. The right contact point of a gear is tooth index 2, and the left contact point is tooth index 6.

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
