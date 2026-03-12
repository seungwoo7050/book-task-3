# 01 Backend Core

## 이 트랙이 푸는 문제

- 실무 백엔드 핵심인 HTTP, SQL, 인증, 캐시, 관측성을 한 번에 배우면 각 경계가 왜 필요한지 설명하기 어렵다.

## 이 트랙의 답

- 브리지 과제를 추가해 HTTP -> auth -> SQL 저장소 -> cache/observability -> concurrency 순서로 난도를 올렸다.

## 프로젝트 순서

1. [04-sql-and-data-modeling](04-sql-and-data-modeling/README.md) : 스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다.
2. [05-http-rest-basics](05-http-rest-basics/README.md) : 작은 JSON API를 통해 상태 코드, validation, pagination, idempotency 기본 감각을 익히는 브리지 과제다.
3. [06-go-api-standard](06-go-api-standard/README.md) : 표준 라이브러리만으로 REST API, middleware, JSON envelope, graceful shutdown을 정리하는 본선 과제다.
4. [07-auth-session-jwt](07-auth-session-jwt/README.md) : session login과 JWT login을 함께 구현해 인증 방식과 인가 경계를 비교하는 브리지 과제다.
5. [08-sql-store-api](08-sql-store-api/README.md) : SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다.
6. [09-cache-migrations-observability](09-cache-migrations-observability/README.md) : cache-aside, cache invalidation, migration, metrics, trace header를 한 API로 묶어 운영 기본기를 붙이는 과제다.
7. [10-concurrency-patterns](10-concurrency-patterns/README.md) : worker pool과 pipeline을 통해 goroutine lifecycle, channel, cancellation을 직접 다루는 본선 과제다.
8. [11-rate-limiter](11-rate-limiter/README.md) : Token Bucket과 per-client limiter를 HTTP middleware까지 연결해 백엔드 보호 기초를 익히는 과제다.

## 졸업 기준

- 인증 포함 REST API를 직접 구성하고, 저장소 계층과 migration 흐름을 설명할 수 있어야 한다.
- cache, metrics, rate limiting 같은 운영 기본 요소를 어떤 경계에 둘지 스스로 결정할 수 있어야 한다.

## 대표 프로젝트

- [08-sql-store-api](08-sql-store-api/README.md) : 이 트랙에서 문제와 답이 가장 선명하게 만나는 중심 과제다.
