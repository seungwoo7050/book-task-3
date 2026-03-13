# 17 Game Store Capstone Evidence Ledger

## 10 bootstrap-and-schema

- 시간 표지: 1단계: 인프라 구성 -> 2단계: Go 모듈 초기화 -> 3단계: 스키마 설계 -> 4단계: 패키지 구조 설계
- 당시 목표: 잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 하나의 흐름으로 묶어야 한다.
- 변경 단위: `jackc/pgx/v5`, `google/uuid`
- 처음 가설: 필수 기술을 하나의 단일 백엔드 기준선으로 다시 묶어 capstone으로 삼았다.
- 실제 조치: CockroachDB 단일 노드 (프로젝트 14와 동일 패턴). Go 1.24.0. 의존성: `jackc/pgx/v5` v5.8.0 — CockroachDB 드라이버 `google/uuid` v1.6.0 — 애플리케이션 레벨 UUID 생성 테이블: `players` — balance BIGINT, version BIGINT, CHECK (balance >= 0) `catalog_items` — sku UNIQUE, price CHECK (price > 0) `purchases` — FK to players, catalog_items `inventories` — UNIQUE (player_id, item_id), qty CHECK (qty >= 0) `idempotency_keys` — key TEXT PK, request_hash, response_json JSONB `outbox` — aggregate_id, event_type, payload_json, published_at nullable

CLI:

```bash
cd 17-game-store-capstone/go
docker compose up -d
make wait-db

go mod init github.com/woopinbell/go-backend/study/04-capstone/17-game-store-capstone
go get github.com/jackc/pgx/v5
go get github.com/google/uuid
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/schema.sql`
- 새로 배운 것: 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.
- 다음: 다음 글에서는 `20-purchase-flow-and-tx-core.md`에서 이어지는 경계를 다룬다.
