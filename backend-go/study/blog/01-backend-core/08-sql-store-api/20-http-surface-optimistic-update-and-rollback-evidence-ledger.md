# 08 SQL Store API Evidence Ledger

## 20 http-surface-optimistic-update-and-rollback

- 시간 표지: 7단계: 에러 정의 -> 8단계: App 구조체와 라우트 -> 9단계: 핸들러 구현 -> 10단계: main.go 작성 -> 11단계: 테스트 작성 (store_test.go) -> 12단계: 실행 및 API 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `solution/go/internal/store/store_test.go`, `solution/go/internal/store/store.go`
- 처음 가설: optimistic update와 rollback을 같은 과제에 묶어 이후 정합성 과제의 발판으로 삼았다.
- 실제 조치: 각 핸들러의 패턴: JSON 디코딩 → 입력 검증 → Repository 호출 → 에러 매핑 → JSON 응답 에러 매핑: `ErrNotFound` → 404 `ErrConflict` → 409 검증 실패 → 422 포트 4040 사용. 테스트 목록: `TestMigrationUpDown` — up 후 down하면 테이블 없음 확인 `TestRepositoryCRUD` — Create → Get → Update → List `TestReserveStockRollback` — 재고 초과 시 rollback, 원래 수량 유지 `TestCreateProductValidation` — name="" → 422

CLI:

```bash
go test ./internal/store/...

go run ./cmd/server
```

- 검증 신호:
- 2026-03-07 기준 `go test ./...`가 통과했다.
- 테스트는 migration up/down, CRUD, optimistic update, rollback 성격의 재고 예약을 포함한다.
- 남은 선택 검증: 외부 DB 연결과 connection pool 조정은 다루지 않았다.
- 핵심 코드 앵커: `solution/go/internal/store/store_test.go`
- 새로 배운 것: repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.
- 다음: 외부 DB 연결과 connection pool 조정은 다루지 않았다.
