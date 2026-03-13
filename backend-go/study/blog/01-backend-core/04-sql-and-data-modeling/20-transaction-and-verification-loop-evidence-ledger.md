# 04 SQL And Data Modeling Evidence Ledger

## 20 transaction-and-verification-loop

- 시간 표지: Phase 4: CLI 바이너리 작성 -> Phase 5: 테스트 작성 -> Phase 6: 문서 작성 및 최종 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/cmd/schemawalk/main.go`, `problem/README.md`, `docs/README.md`, `docs/concepts/core-concepts.md`, `docs/references/README.md`, `docs/verification.md`
- 처음 가설: 실제 migration tool은 뒤로 미루고 데이터 모델과 transaction 경계를 먼저 학습하게 했다.
- 실제 조치: main.go 작성 (`solution/go/cmd/schemawalk/main.go`) DB 열기 → 스키마 적용 → 시드 → alice 인벤토리 조회 → 출력. `defer db.Close()`로 DB 정리. 테스트 헬퍼 (`newTestDB`) 매 테스트마다 새 in-memory DB를 만들고 스키마와 시드를 적용. `t.Helper()`로 에러 위치를 올바르게 표시.

CLI:

```bash
cd solution/go
go run ./cmd/schemawalk
# alice owns 2 x potion

cd solution/go
go test ./...
go test -v ./catalog/

# === RUN   TestListInventory
# --- PASS
# === RUN   TestPurchase
# --- PASS
# === RUN   TestPurchaseUnknownItem
# --- PASS
```

- 검증 신호:
- DB 열기 → 스키마 적용 → 시드 → alice 인벤토리 조회 → 출력. `defer db.Close()`로 DB 정리.
- --- PASS
- 2026-03-07 기준 `go run ./cmd/schemawalk`가 정상 실행됐다.
- 2026-03-07 기준 `go test ./...`가 통과했다.
- 남은 선택 검증: 실제 migration binary와 외부 RDBMS 연결은 다음 과제에서 다룬다.
- 핵심 코드 앵커: `solution/go/catalog/catalog_test.go`
- 새로 배운 것: `PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다.
- 다음: 실제 migration binary와 외부 RDBMS 연결은 다음 과제에서 다룬다.
