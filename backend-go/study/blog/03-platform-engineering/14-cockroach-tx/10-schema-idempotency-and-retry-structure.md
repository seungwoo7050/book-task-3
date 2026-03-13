# 14 Cockroach TX Structure

## 이 글이 답할 질문

- 중복 요청, 동시 요청, CockroachDB retry를 한 purchase 흐름에서 다뤄야 한다.
- DB가 요구하는 retry와 애플리케이션이 요구하는 idempotency를 한 흐름에서 분리해 보여 준다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `03-platform-engineering/14-cockroach-tx` 안에서 `10-schema-idempotency-and-retry.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 인프라 구성 -> 2단계: 스키마 설계 및 마이그레이션 -> 3단계: Go 모듈 초기화 -> 4단계: 패키지 구조 설계 -> 5단계: Repository 구현 -> 6단계: 트랜잭션 재시도 헬퍼
- 세션 본문: `solution/go/schema.sql, solution/go/txn/retry.go` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/schema.sql`
- 코드 앵커 2: `solution/go/txn/retry.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다.
- 마지막 단락: 다음 글에서는 `20-purchase-service-and-http-surface.md`에서 이어지는 경계를 다룬다.
