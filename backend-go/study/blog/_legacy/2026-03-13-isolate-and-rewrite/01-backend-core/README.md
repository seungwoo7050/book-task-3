# 01 Backend Core blog

`01-backend-core`는 - 브리지 과제를 추가해 HTTP -> auth -> SQL 저장소 -> cache/observability -> concurrency 순서로 난도를 올렸다.

## 프로젝트 인덱스

| 프로젝트 | 시리즈 맵 | evidence ledger | structure | final blog | 대표 검증 |
| --- | --- | --- | --- | --- | --- |
| 04 SQL And Data Modeling | [00-series-map](04-sql-and-data-modeling/00-series-map.md) | [01-evidence-ledger](04-sql-and-data-modeling/01-evidence-ledger.md) | [_structure-outline](04-sql-and-data-modeling/_structure-outline.md) | [10-reconstructed](04-sql-and-data-modeling/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go run ./cmd/schemawalk` |
| 05 HTTP REST Basics | [00-series-map](05-http-rest-basics/00-series-map.md) | [01-evidence-ledger](05-http-rest-basics/01-evidence-ledger.md) | [_structure-outline](05-http-rest-basics/_structure-outline.md) | [10-reconstructed](05-http-rest-basics/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./internal/api` |
| 06 Go API Standard | [00-series-map](06-go-api-standard/00-series-map.md) | [01-evidence-ledger](06-go-api-standard/01-evidence-ledger.md) | [_structure-outline](06-go-api-standard/_structure-outline.md) | [10-reconstructed](06-go-api-standard/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./cmd/api` |
| 07 Auth Session JWT | [00-series-map](07-auth-session-jwt/00-series-map.md) | [01-evidence-ledger](07-auth-session-jwt/01-evidence-ledger.md) | [_structure-outline](07-auth-session-jwt/_structure-outline.md) | [10-reconstructed](07-auth-session-jwt/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./internal/auth` |
| 08 SQL Store API | [00-series-map](08-sql-store-api/00-series-map.md) | [01-evidence-ledger](08-sql-store-api/01-evidence-ledger.md) | [_structure-outline](08-sql-store-api/_structure-outline.md) | [10-reconstructed](08-sql-store-api/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./internal/store` |
| 09 Cache Migrations Observability | [00-series-map](09-cache-migrations-observability/00-series-map.md) | [01-evidence-ledger](09-cache-migrations-observability/01-evidence-ledger.md) | [_structure-outline](09-cache-migrations-observability/_structure-outline.md) | [10-reconstructed](09-cache-migrations-observability/10-2026-03-13-reconstructed-development-log.md) | `cd solution/go && go test -v ./internal/app` |
| 10 Concurrency Patterns | [00-series-map](10-concurrency-patterns/00-series-map.md) | [01-evidence-ledger](10-concurrency-patterns/01-evidence-ledger.md) | [_structure-outline](10-concurrency-patterns/_structure-outline.md) | [10-reconstructed](10-concurrency-patterns/10-2026-03-13-reconstructed-development-log.md) | `make -C problem run-workerpool` |
| 11 Rate Limiter | [00-series-map](11-rate-limiter/00-series-map.md) | [01-evidence-ledger](11-rate-limiter/01-evidence-ledger.md) | [_structure-outline](11-rate-limiter/_structure-outline.md) | [10-reconstructed](11-rate-limiter/10-2026-03-13-reconstructed-development-log.md) | `make -C problem test` |
