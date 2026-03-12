# 10-shippable-backend-service

- 그룹: `Applied`
- 상태: `verified`
- 공개 답안 레인: `nestjs/`
- 성격: 09 기반 포트폴리오 재패키징

## 한 줄 문제

학습용 capstone을 Postgres, Redis, Docker Compose, Swagger까지 포함한 채용 제출용 NestJS 서비스 표면으로 다시 패키징하는 문제다.

## 성공 기준

- JWT 인증, RBAC, Books CRUD, migration, cache, throttling을 한 서비스 표면으로 설명할 수 있다.
- Postgres와 Redis가 필요한 실행 흐름을 README만으로 재현할 수 있다.
- 학습용 통합 과제와 제출용 서비스의 차이를 문서로 설명할 수 있다.

## 내가 만든 답

- `09-platform-capstone`을 직접 덮어쓰지 않고 별도 프로젝트로 분리해 포트폴리오용 표면을 만들었다.
- Postgres migration, Redis cache/throttling, Docker Compose, Swagger, seed script를 한 묶음으로 구성했다.
- 루트 README에서 바로 대표 결과물로 읽히도록 채용 검토자 중심 문서를 배치했다.

## 제공 자료

- `problem/README.md`
- `nestjs/`
- `docker-compose.yml`
- `docs/`
- `notion/`

## 실행과 검증

### NestJS 포트폴리오 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `docker compose up -d postgres redis && cp .env.example .env && pnpm run db:migrate && pnpm run db:seed && pnpm run start`

## 왜 다음 단계로 이어지는가

- 이 트랙의 끝 단계다. 이후에는 배포, queue/worker, 외부 연동 같은 별도 포트폴리오 축으로 확장하면 된다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [nestjs/README.md](nestjs/README.md)에서 확인한다.
