# 문제 정의

게임 상점 구매 흐름에서 트랜잭션, 멱등성, outbox, 운영 기본 요소를 통합한 단일 백엔드를 만든다.

## 성공 기준

- `GET /v1/healthcheck`, `POST /v1/purchases`, 구매 조회, 인벤토리 조회 API를 제공한다.
- `Idempotency-Key` 기반 중복 요청 안전 처리와 낙관적 잠금을 구현한다.
- purchase 성공 시 outbox row를 기록하고 relay가 발행을 이어받는다.
- 구조화 로그, rate limiting, graceful shutdown을 포함한다.
- README 기준으로 build/test/repro가 가능해야 한다.

## 제공 자료와 출처

- legacy `04-platform-capstone/09-game-store-capstone` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 세부 요구사항은 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && mkdir -p ./bin && go build -o ./bin/api ./cmd/api`
- `cd solution/go && go test ./...`
- `cd solution/go && make repro`

## 제외 범위

- 마이크로서비스 분리
- 복잡한 외부 인증
