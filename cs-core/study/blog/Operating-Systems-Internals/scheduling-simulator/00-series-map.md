# Scheduling Simulator 시리즈 맵

`scheduling-simulator`는 단일 CPU 위에서 scheduling policy가 waiting time, response time, turnaround time을 어떻게 바꾸는지 replay와 지표로 보여 주는 실험이다. 이 시리즈는 결과만 정리해 둔 회고문이 아니라, workload fixture와 공통 시뮬레이션 루프를 먼저 세운 뒤, policy별 차이가 replay/metric으로 어떻게 보이는지 따라간다.를 끝까지 따라가게 만드는 입구다.

2026-03-13에 기존 초안을 `study/blog/_legacy/2026-03-13-isolate-and-rewrite/Operating-Systems-Internals/scheduling-simulator/`로 옮긴 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 시리즈를 다시 썼다. 그래서 이 문서는 '무엇을 만들었는가'보다 '어떤 순서로 읽어야 그 판단 이동이 보이는가'를 먼저 설명한다.

## 이 시리즈를 읽는 방법

가장 먼저 `01-evidence-ledger.md`에서 살아 있는 근거를 모아 본다. 그 다음 `_structure-outline.md`에서 왜 최종 글이 그 순서로 배치되는지 확인한다. 마지막으로 `10-2026-03-13-reconstructed-development-log.md`에서 그 근거가 실제 서사로 어떻게 이어지는지 읽는다.

## 이번 재작성에서 붙잡은 source-of-truth

- 문제 계약: [`README.md`](../../../Operating-Systems-Internals/scheduling-simulator/README.md), [`problem/README.md`](../../../Operating-Systems-Internals/scheduling-simulator/problem/README.md)
- 구현 표면: `python/src/os_scheduling/__init__.py`, `python/src/os_scheduling/__main__.py`, `python/src/os_scheduling/cli.py`, `python/src/os_scheduling/core.py`
- 검증 entrypoint: `make test && make run-demo` in `problem`
- 개념 축: `mlfq heuristics`, `policy tradeoffs`, `scheduler metrics`

## 읽는 순서

1. [`01-evidence-ledger.md`](01-evidence-ledger.md) — source-first 근거와 phase별 판단 전환점을 먼저 모아 둔 문서
2. [`_structure-outline.md`](_structure-outline.md) — 최종 글의 읽기 곡선과 장면 배치를 설명하는 편집 설계 메모
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md) — 구현 순서, 코드, CLI를 한 흐름으로 다시 쓴 최종 blog

## 이번에 따라간 질문

workload fixture와 공통 시뮬레이션 루프를 먼저 세운 뒤, policy별 차이가 replay/metric으로 어떻게 보이는지 따라간다.
