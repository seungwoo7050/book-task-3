# 08 SQL Store API Structure

## 이 글이 답할 질문

- `database/sql` 기반 CRUD API를 구현해야 한다.
- DB 접근은 `database/sql`과 repository 계층으로 감싸 ORM 없이 경계를 드러냈다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `01-backend-core/08-sql-store-api` 안에서 `10-sql-store-and-migrations.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: 1단계: 프로젝트 초기화 -> 2단계: 외부 의존성 설치 -> 3단계: 디렉토리 구조 생성 -> 4단계: 스키마 정의 (store.go) -> 5단계: DB 연결 및 마이그레이션 함수 -> 6단계: Product 구조체 및 Repository
- 세션 본문: `require modernc.org/sqlite v1.38.2` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/internal/store/store.go`
- 코드 앵커 2: `solution/go/cmd/server/main.go`
- 코드 설명 초점: 이 코드는 상태를 저장하고 읽는 계약을 고정한 부분이다. 이후의 handler, service, runtime 설명은 이 저장 규칙이 닫혀 있어야만 설득력을 갖는다.
- 개념 설명: migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.
- 마지막 단락: 다음 글에서는 `20-http-surface-optimistic-update-and-rollback.md`에서 이어지는 경계를 다룬다.
