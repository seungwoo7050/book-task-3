# 17 Game Store Capstone Structure

## 이 글이 답할 질문

- 잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 하나의 흐름으로 묶어야 한다.
- 필수 기술을 하나의 단일 백엔드 기준선으로 다시 묶어 capstone으로 삼았다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `04-capstone/17-game-store-capstone` 안에서 `10-bootstrap-and-schema.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 인프라 구성 -> 2단계: Go 모듈 초기화 -> 3단계: 스키마 설계 -> 4단계: 패키지 구조 설계
- 세션 본문: `jackc/pgx/v5, google/uuid` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/schema.sql`
- 코드 앵커 2: `solution/go/internal/config/config.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.
- 마지막 단락: 다음 글에서는 `20-purchase-flow-and-tx-core.md`에서 이어지는 경계를 다룬다.
