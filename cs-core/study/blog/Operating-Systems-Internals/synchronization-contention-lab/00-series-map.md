# Synchronization Contention Lab 시리즈 맵

`synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다. 이 시리즈는 결과만 정리해 둔 회고문이 아니라, counter/gate/buffer 세 시나리오를 먼저 세우고, mutex/semaphore/condvar가 각 시나리오에서 무엇을 보장하는지 따라간다.를 끝까지 따라가게 만드는 입구다.

2026-03-13에 기존 초안을 `study/blog/_legacy/2026-03-13-isolate-and-rewrite/Operating-Systems-Internals/synchronization-contention-lab/`로 옮긴 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 시리즈를 다시 썼다. 그래서 이 문서는 '무엇을 만들었는가'보다 '어떤 순서로 읽어야 그 판단 이동이 보이는가'를 먼저 설명한다.

## 이 시리즈를 읽는 방법

가장 먼저 `01-evidence-ledger.md`에서 살아 있는 근거를 모아 본다. 그 다음 `_structure-outline.md`에서 왜 최종 글이 그 순서로 배치되는지 확인한다. 마지막으로 `10-2026-03-13-reconstructed-development-log.md`에서 그 근거가 실제 서사로 어떻게 이어지는지 읽는다.

## 이번 재작성에서 붙잡은 source-of-truth

- 문제 계약: [`README.md`](../../../Operating-Systems-Internals/synchronization-contention-lab/README.md), [`problem/README.md`](../../../Operating-Systems-Internals/synchronization-contention-lab/problem/README.md)
- 구현 표면: `c/src/contention_lab.c`, `c/src/main.c`
- 검증 entrypoint: `make test && make run-demo` in `problem`
- 개념 축: `correctness before timing`, `mutex semaphore condvar`, `scenario invariants`

## 읽는 순서

1. [`01-evidence-ledger.md`](01-evidence-ledger.md) — source-first 근거와 phase별 판단 전환점을 먼저 모아 둔 문서
2. [`_structure-outline.md`](_structure-outline.md) — 최종 글의 읽기 곡선과 장면 배치를 설명하는 편집 설계 메모
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md) — 구현 순서, 코드, CLI를 한 흐름으로 다시 쓴 최종 blog

## 이번에 따라간 질문

counter/gate/buffer 세 시나리오를 먼저 세우고, mutex/semaphore/condvar가 각 시나리오에서 무엇을 보장하는지 따라간다.
