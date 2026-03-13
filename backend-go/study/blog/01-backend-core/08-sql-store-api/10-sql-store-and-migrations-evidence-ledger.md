# 08 SQL Store API Evidence Ledger

## 10 sql-store-and-migrations

- 시간 표지: 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: 스키마 정의 (store.go) -> 5단계: DB 연결 및 마이그레이션 함수 -> 6단계: Product 구조체 및 Repository
- 당시 목표: `database/sql` 기반 CRUD API를 구현해야 한다.
- 변경 단위: `require modernc.org/sqlite v1.38.2`
- 처음 가설: DB 접근은 `database/sql`과 repository 계층으로 감싸 ORM 없이 경계를 드러냈다.
- 실제 조치: `go.mod`에 `require modernc.org/sqlite v1.38.2`와 간접 의존성들이 추가된다. Repository 메서드 순서: `Create` — INSERT, LastInsertId로 ID 취득 `Get` — SELECT + Scan, sql.ErrNoRows 처리 `List` — QueryContext + rows.Next 순회 `Update` — WHERE version = ? 조건으로 optimistic update `ReserveStock` — BeginTx + 재고 확인 + UPDATE + Commit/Rollback

CLI:

```bash
cd study/01-backend-core/08-sql-store-api/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/08-sql-store-api

go get modernc.org/sqlite
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/internal/store/store.go`
- 새로 배운 것: migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.
- 다음: 다음 글에서는 `20-http-surface-optimistic-update-and-rollback.md`에서 이어지는 경계를 다룬다.
