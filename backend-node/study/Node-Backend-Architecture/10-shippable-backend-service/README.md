# 10-shippable-backend-service

- 상태: `verified`
- 구현 레인: `nestjs/`
- 프로젝트 성격: `09-platform-capstone`의 포트폴리오 강화판
- legacy 출처: `legacy/06-platform-capstone`을 직접 이식한 것이 아니라 `09-platform-capstone`을 기준으로 재패키징

## 프로젝트 한 줄 설명

JWT 인증, RBAC, Books CRUD, 이벤트 발행, Postgres migration, Redis 캐시와 로그인 throttling,
Swagger, Docker Compose를 한 번에 재현할 수 있는 채용 제출용 NestJS 백엔드 서비스다.

## 핵심 기능

- `POST /auth/register`, `POST /auth/login`
- `GET /books`, `GET /books/:id` 공개 조회
- `POST /books`, `PUT /books/:id`, `DELETE /books/:id` 관리자 전용 쓰기
- `GET /health/live`, `GET /health/ready`
- `GET /docs` Swagger UI
- 로그인 실패 횟수 기반 throttling
- public books 조회 캐시와 write 이후 invalidation

## 기술 스택

- NestJS + TypeScript
- TypeORM
- Postgres
- Redis
- Docker Compose
- Vitest
- GitHub Actions service containers

## 아키텍처 요약

- Auth, Books, Events를 feature module로 분리했다.
- Postgres는 checked-in migration과 seed script로 초기화한다.
- Redis는 `books:list`, `books:detail:*` 캐시와 `auth:login:*` throttling key만 담당한다.
- 응답 envelope, validation, HTTP error formatting, request id logging 규약은 기존 capstone과 동일하게 유지한다.

## 빠른 실행 방법

1. `docker compose up -d postgres redis`
2. `cd nestjs`
3. `pnpm install`
4. `cp .env.example .env`
5. `pnpm run db:migrate`
6. `pnpm run db:seed`
7. `pnpm run start`

Docker Compose로 앱까지 같이 올리려면 프로젝트 루트에서 `docker compose up -d app`을 실행한다.

## 테스트 방법

- unit: `pnpm run test`
- e2e: `docker compose up -d postgres redis && env $(cat .env.example | xargs) pnpm run test:e2e`

## API 문서 위치

- app 실행 후 [GET /docs](http://127.0.0.1:3000/docs)
- 발표 자료: [portfolio-presentation.md](docs/portfolio-presentation.md)

## 주요 트레이드오프

- `09`를 직접 바꾸지 않고 `10`을 별도 과제로 분리했다. 학습용 통합 capstone과 제출용 서비스의 목적이 다르기 때문이다.
- DB는 SQLite 대신 Postgres로 바꿨지만 ORM은 TypeORM을 유지했다. 저장소 전체의 개념 연속성을 유지하려는 선택이다.
- Redis는 cache와 throttling에만 쓴다. queue/worker는 다음 단계로 남겨 두었다.
- 클라우드 배포 대신 local reproducibility를 우선했다. 누구나 Docker Compose와 `.env.example`만으로 실행 가능한 상태를 목표로 삼았다.

## 실패 시 복구 루트

- `ECONNREFUSED`가 나면 `docker compose ps`로 Postgres와 Redis 상태를 먼저 확인한다.
- migration 실패 시 `DATABASE_URL`과 `public` schema 권한을 먼저 본다.
- `/docs`가 비어 있으면 `pnpm run build`를 다시 실행한 뒤 앱을 재시작한다.
- e2e 전에 `docker compose up -d postgres redis`를 빼먹으면 readiness와 login throttling 관련 테스트가 모두 실패한다.
