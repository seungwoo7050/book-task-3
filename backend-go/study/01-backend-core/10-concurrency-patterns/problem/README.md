# 문제 정의

Go의 핵심 동시성 패턴인 worker pool과 pipeline을 구현하고 goroutine lifecycle을 안전하게 관리한다.

## 성공 기준

- worker pool이 job 제출, 결과 수집, graceful shutdown을 지원한다.
- pipeline이 Generator -> Filter -> Sink 3단계로 동작한다.
- 모든 단계가 context cancellation을 존중한다.
- goroutine leak 없이 종료된다.
- benchmark로 throughput을 확인한다.

## 제공 자료와 출처

- legacy `01-foundation/02-concurrency-patterns` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 세부 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem test`
- `make -C problem bench`

## 제외 범위

- distributed queue
- production backpressure policy
