# 17 Game Store Capstone Evidence Ledger

## 40 repro-and-e2e-hardening

- 시간 표지: 12단계: E2E 테스트 -> 13단계: 전체 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/e2e/purchase_flow_test.go`, `solution/go/Makefile`
- 처음 가설: OAuth나 마이크로서비스는 제외하고 거래 일관성과 재현성에 집중했다.
- 실제 조치: 

CLI:

```bash
make e2e
# 구매 → 조회 → 멱등성 → 인벤토리 확인

make build
make test
go test -race ./...
```

- 검증 신호:
- 2026-03-08 기준 `mkdir -p ./bin && go build -o ./bin/api ./cmd/api`가 통과했다.
- 2026-03-08 기준 `go test ./...`가 통과했다.
- 2026-03-08 기준 `make repro`가 통과했다.
- 핵심 코드 앵커: `solution/go/e2e/purchase_flow_test.go`
- 새로 배운 것: e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.
- 다음: 선택 검증이나 운영 환경에서만 가능한 경계를 짧게 남긴다.
