# 09 Cache Migrations Observability Series Map

`01-backend-core/09-cache-migrations-observability`는 cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다.

## 이 시리즈가 복원하는 것

- 시작점: cache-aside hit/miss와 invalidation을 같이 경험해야 한다.
- 구현 축: SQLite 저장소 위에 in-memory cache-aside 계층과 `/metrics` 노출을 `solution/go`에 구현했다.
- 검증 축: 2026-03-07 기준 `go test ./...`가 통과했다.
- 글 수: 3편

## 읽는 순서

- [10-runtime-and-migration-surface.md](10-runtime-and-migration-surface.md)
- [20-cache-invalidation-and-fallback.md](20-cache-invalidation-and-fallback.md)
- [30-metrics-tracing-and-verification.md](30-metrics-tracing-and-verification.md)

## 근거 기준

- 소스코드, README, docs, 테스트, CLI만 입력 근거로 사용했다.
- 기존 blog 초안과 `_legacy` 본문은 입력 근거로 사용하지 않았다.
