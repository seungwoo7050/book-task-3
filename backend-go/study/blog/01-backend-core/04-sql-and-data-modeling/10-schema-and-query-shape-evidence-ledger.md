# 04 SQL And Data Modeling Evidence Ledger

## 10 schema-and-query-shape

- 시간 표지: Phase 1: 프로젝트 뼈대와 의존성 -> Phase 2: 스키마 설계 -> Phase 3: 쿼리 구현
- 당시 목표: 스키마 설계와 관계 모델링을 실제 도메인 예제로 익혀야 한다.
- 변경 단위: `modernc.org/sqlite`, `solution/go/catalog/catalog.go`
- 처음 가설: ORM 없이 SQL 구조를 먼저 보여 주기 위해 스키마와 쿼리 자체를 학습 표면에 올렸다.
- 실제 조치: 디렉터리 구조 생성 Go 모듈 초기화 및 의존성 설치 SQL 스키마 작성 (`solution/go/catalog/catalog.go`) 세 테이블의 DDL을 Go 상수로 작성했다: `players`: 플레이어 (id, name) `items`: 아이템 (id, name, price_cents) `inventory`: 인벤토리 (player_id, item_id, quantity) — composite PK

CLI:

```bash
mkdir -p 01-backend-core/04-sql-and-data-modeling/{solution/go/cmd/schemawalk,solution/go/catalog,docs/concepts,docs/references,problem}

cd 01-backend-core/04-sql-and-data-modeling/go
go mod init github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling
go get modernc.org/sqlite
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/go/catalog/catalog.go`
- 새로 배운 것: `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.
- 다음: 다음 글에서는 `20-transaction-and-verification-loop.md`에서 이어지는 경계를 다룬다.
