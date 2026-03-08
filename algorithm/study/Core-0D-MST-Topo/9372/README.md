# BOJ 9372 — 상근이의 여행

| Item | Detail |
| :--- | :--- |
| Track | `Core-0D-MST-Topo` |
| Legacy Source | `legacy/core/0D-mst-topo/bronze-9372` |
| Tier | Bronze |
| CLRS | Ch 23, 22.4 |
| Problem URL | https://www.acmicpc.net/problem/9372 |

## Summary

$N$개 국가, $M$개 비행기 노선(양방향). 모든 국가를 여행하기 위해 탑승해야 하는 최소 비행기 수를 구하라.

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
