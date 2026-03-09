# 10-shippable-backend-service — 읽기 가이드

## 이 폴더의 구성

| 파일 | 설명 | 추천 독자 |
|------|------|-----------|
| **essay.md** | SQLite→Postgres, Redis 캐시/쓰로틀링, Docker Compose, 마이그레이션, Swagger까지 포트폴리오 수준의 백엔드로 올리는 과정을 서사적으로 풀어낸 에세이 | 09 캡스톤과의 차이, 인프라 선택의 근거를 이해하고 싶은 독자 |
| **timeline.md** | Docker Compose 설정, Postgres 마이그레이션, Redis 연결, 환경변수 관리, Seed 스크립트까지의 개발 과정 | 직접 따라 실행하거나, 소스 코드에 보이지 않는 인프라 작업을 알고 싶은 독자 |

## 추천 읽기 순서

1. **essay.md** — 왜 SQLite에서 Postgres로, 왜 Redis를 도입하는지, 마이그레이션이 `synchronize: true`를 대체하는 이유를 먼저 파악한다.
2. **timeline.md** — Docker Compose 기동, 환경변수 설정, 마이그레이션/시드 실행, Swagger 확인 등 코드 밖 과정을 확인한다.
3. **소스 코드** — `database/`, `runtime/`, `auth/auth-rate-limit.service.ts`, `books/books.service.ts`(캐시 로직) 순으로 읽는다.

## 관련 프로젝트

- **09-platform-capstone**: 이 프로젝트의 기반, SQLite + 단일 프로세스 버전
- **06-persistence-and-repositories**: SQLite raw SQL / TypeORM 비교의 원점
- **08-production-readiness**: Health check, config, logging의 기초 버전
