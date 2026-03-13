# 14 Cockroach TX Evidence Ledger

## 10 schema-idempotency-and-retry

- 시간 표지: 1단계: 인프라 구성 -> 2단계: 스키마 설계 및 마이그레이션 -> 3단계: Go 모듈 초기화 -> 4단계: 패키지 구조 설계 -> 5단계: Repository 구현 -> 6단계: 트랜잭션 재시도 헬퍼
- 당시 목표: 중복 요청, 동시 요청, CockroachDB retry를 한 purchase 흐름에서 다뤄야 한다.
- 변경 단위: `solution/go/schema.sql`, `solution/go/txn/retry.go`
- 처음 가설: DB가 요구하는 retry와 애플리케이션이 요구하는 idempotency를 한 흐름에서 분리해 보여 준다.
- 실제 조치: 포트 매핑: `26257:26258` (SQL), `8081:8080` (Admin UI) 4개 테이블: `players`, `inventory`, `idempotency_keys`, `audit_log` 핵심 제약: `players.version` (낙관적 잠금), `UNIQUE(player_id, item_name)` (upsert), `REFERENCES players(id)` (FK) Go 1.24.0 사용. pgx v5.8.0 — CockroachDB/PostgreSQL 드라이버. 순서: player.go (GetPlayer, DeductBalance) → inventory.go (UpsertInventory) → audit.go (InsertAuditLog) → idempotency.go (Get/Insert/Exists)

CLI:

```bash
# Docker Compose로 CockroachDB 단일 노드 실행
cd 14-cockroach-tx/go
docker compose -p cockroach-tx up -d db

# DB 준비 대기
make wait-db
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/schema.sql`
- 새로 배운 것: idempotency key는 네트워크 재시도와 중복 요청을 구분하지 않고 같은 결과로 수렴시키는 장치다.
- 다음: 다음 글에서는 `20-purchase-service-and-http-surface.md`에서 이어지는 경계를 다룬다.
