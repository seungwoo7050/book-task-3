# 0x13 — Meldable Heap Bridge

| Item | Detail |
| :--- | :--- |
| Track | `Advanced-CLRS` |
| Slot | `0x13` |
| Type | Advanced study project |
| CLRS | Ch 19 |
| Legacy Source | `legacy/README.md` Advanced Track roadmap |
| Project Focus | Pairing heap meld and extract-min as a practical bridge to Fibonacci-heap ideas |

## Summary

Fibonacci heap의 핵심 감각인 meld 중심 사고를 pairing heap으로 먼저 익힌다.

이 프로젝트는 BOJ 문제가 아니라 CLRS 주제를 직접 재현 가능한 입력/출력 문제로 바꾼 study project다.

## Curriculum Note

pure Fibonacci heap은 구현 부담이 커서, 이 프로젝트는 pairing heap으로 meld 중심 인터페이스를 먼저 안정화한다. docs에서 Fibonacci heap으로 다시 연결한다.

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
