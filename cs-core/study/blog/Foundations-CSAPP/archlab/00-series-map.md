# Architecture Lab 시리즈 맵

`archlab`은 Y86-64 프로그램 작성, 제어 로직 구현, 파이프라인 성능 개선을 한 흐름으로 묶는 프로젝트다. 이 시리즈는 결과만 정리해 둔 회고문이 아니라, Y86 프로그램, `iaddq` 제어 로직, `ncopy` 성능 개선이 왜 세 개의 다른 문제처럼 느껴지는지 코드 순서로 복원한다.를 끝까지 따라가게 만드는 입구다.

2026-03-13에 기존 초안을 `study/blog/_legacy/2026-03-13-isolate-and-rewrite/Foundations-CSAPP/archlab/`로 옮긴 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 시리즈를 다시 썼다. 그래서 이 문서는 '무엇을 만들었는가'보다 '어떤 순서로 읽어야 그 판단 이동이 보이는가'를 먼저 설명한다.

## 이 시리즈를 읽는 방법

가장 먼저 `01-evidence-ledger.md`에서 살아 있는 근거를 모아 본다. 그 다음 `_structure-outline.md`에서 왜 최종 글이 그 순서로 배치되는지 확인한다. 마지막으로 `10-2026-03-13-reconstructed-development-log.md`에서 그 근거가 실제 서사로 어떻게 이어지는지 읽는다.

## 이번 재작성에서 붙잡은 source-of-truth

- 문제 계약: [`README.md`](../../../Foundations-CSAPP/archlab/README.md), [`problem/README.md`](../../../Foundations-CSAPP/archlab/problem/README.md)
- 구현 표면: `c/src/main.c`, `c/src/mini_archlab.c`, `cpp/src/main.cpp`, `cpp/src/mini_archlab.cpp`, `y86/src/copy.ys`, `y86/src/ncopy.ys`
- 검증 entrypoint: `make clean && make test` in `c`
- 개념 축: `iaddq and control signals`, `part split`, `pipeline cost model`

## 읽는 순서

1. [`01-evidence-ledger.md`](01-evidence-ledger.md) — source-first 근거와 phase별 판단 전환점을 먼저 모아 둔 문서
2. [`_structure-outline.md`](_structure-outline.md) — 최종 글의 읽기 곡선과 장면 배치를 설명하는 편집 설계 메모
3. [`10-2026-03-13-reconstructed-development-log.md`](10-2026-03-13-reconstructed-development-log.md) — 구현 순서, 코드, CLI를 한 흐름으로 다시 쓴 최종 blog

## 이번에 따라간 질문

Y86 프로그램, `iaddq` 제어 로직, `ncopy` 성능 개선이 왜 세 개의 다른 문제처럼 느껴지는지 코드 순서로 복원한다.
