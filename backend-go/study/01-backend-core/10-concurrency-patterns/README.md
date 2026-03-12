# 10 Concurrency Patterns

## 한 줄 요약

worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다.

## 이 프로젝트가 푸는 문제

- worker pool과 pipeline을 각각 구현해야 한다.
- goroutine leak 없이 graceful shutdown과 context cancellation을 지원해야 한다.
- benchmark로 throughput 차이를 관찰해야 한다.

## 내가 만든 답

- worker pool과 three-stage pipeline을 `solution/go`에 구현했다.
- context cancellation과 channel close 규칙을 테스트로 고정했다.
- 문제 실행은 `problem/Makefile`, 구현 진입점은 `solution/go`로 분리했다.

## 핵심 설계 선택

- 분산 큐 같은 외부 시스템을 제거하고 순수 Go 동시성 패턴에만 집중하게 했다.
- goroutine leak 방지를 핵심 검증 기준으로 잡아 단순 병렬 처리 예제와 구분했다.

## 검증

- `make -C problem run-workerpool`
- `make -C problem run-pipeline`
- `make -C problem test`
- `make -C problem bench`

## 제외 범위

- 분산 큐 연동
- 실서비스 backpressure 정책

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: legacy/01-foundation/02-concurrency-patterns (`legacy/01-foundation/02-concurrency-patterns/README.md`, public repo에는 미포함)
