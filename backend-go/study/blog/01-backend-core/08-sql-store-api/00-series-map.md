# 08 SQL Store API Series Map

`01-backend-core/08-sql-store-api`는 SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다.

## 이 시리즈가 복원하는 것

- 시작점: `database/sql` 기반 CRUD API를 구현해야 한다.
- 구현 축: 상품 CRUD API와 SQLite 저장소를 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `go test ./...`가 통과했다.
- 글 수: 2편

## 읽는 순서

- [10-sql-store-and-migrations.md](10-sql-store-and-migrations.md)
- [20-http-surface-optimistic-update-and-rollback.md](20-http-surface-optimistic-update-and-rollback.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
