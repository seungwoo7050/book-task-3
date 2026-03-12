# 문제 정의

게임 플랫폼 구매 흐름에서 optimistic locking, idempotency key, CockroachDB transaction retry를 구현한다.

## 성공 기준

- `players`, `inventory`, `idempotency_keys`, `audit_log` 중심 스키마를 구성한다.
- 잔액 차감이 optimistic locking으로 동작한다.
- idempotency key가 이전 응답을 재사용한다.
- SQLSTATE `40001` 재시도 helper를 제공한다.
- `POST /api/purchase` API로 흐름을 노출한다.

## 제공 자료와 출처

- legacy `03-platform-engineering/06-cockroach-tx` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 세부 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem build`
- `make -C problem test`
- `cd solution/go && make repro`

## 제외 범위

- 복잡한 인증/인가
- 분산 트레이싱
