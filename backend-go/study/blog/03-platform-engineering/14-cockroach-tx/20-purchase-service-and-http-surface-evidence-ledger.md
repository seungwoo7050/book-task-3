# 14 Cockroach TX Evidence Ledger

## 20 purchase-service-and-http-surface

- 시간 표지: 7단계: Service 구현 -> 8단계: HTTP Handler -> 9단계: cmd/server 진입점
- 당시 목표: balance version conflict와 idempotency cached response를 서비스 경계에서 구분한다.
- 변경 단위: `solution/go/service/purchase.go`, `solution/go/handler/purchase.go`
- 처음 가설: HTTP handler, service, repo를 나눠 정합성 로직이 어디에 있어야 하는지 드러냈다.
- 실제 조치: `PurchaseService.Purchase` — `RunInTx` 안에서 6단계 조율: 멱등성 키 확인 → 플레이어 조회 → 잔액 차감 → 인벤토리 upsert → 감사 로그 → 멱등성 키 저장 `PurchaseHandler.ServeHTTP` — `Idempotency-Key` 헤더 검증, JSON 디코딩, ErrConflict → 409 매핑 커넥션 풀: `MaxOpenConns=25`, `MaxIdleConns=10`, `ConnMaxLifetime=5m` Graceful shutdown: SIGTERM/SIGINT → 5초 타임아웃

CLI:

```bash
go test ./service/ -v

# 로컬 실행
make run
# 또는: DATABASE_URL="postgresql://root@localhost:26257/defaultdb?sslmode=disable" go run ./cmd/server
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/service/purchase.go`
- 새로 배운 것: optimistic locking은 `version` 컬럼으로 충돌을 감지한다.
- 다음: 다음 글에서는 `30-repro-and-e2e-proof.md`에서 이어지는 경계를 다룬다.
