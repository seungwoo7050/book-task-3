# Node-Backend-Architecture

이 트랙은 완전 초보를 Node.js 백엔드 주니어 준비 수준까지 끌어올리고, 운영과 아키텍처 트레이드오프를 설명할 수 있는 applied 단계까지 이어지는 학습 경로다.

## 이 트랙을 읽는 기준

- `bridge`는 언어, 런타임, HTTP 기본기를 먼저 고정하는 단계다.
- `core`는 Express와 NestJS를 나란히 두고 비교 학습하는 단계다.
- `applied`는 운영성, capstone, recruiter-facing 서비스로 이어지는 적용 단계다.
- 각 프로젝트 README는 `한 줄 문제 -> 내가 만든 답 -> 실행/검증` 순서로 읽히게 유지한다.

## 그룹별 카탈로그

| 그룹 | 프로젝트 | 한 줄 문제 | 답 형태 | 대표 검증 | 상태 |
| --- | --- | --- | --- | --- | --- |
| Bridge | [00-language-and-typescript](bridge/00-language-and-typescript/README.md) | Express와 NestJS로 넘어가기 전에 TypeScript, 비동기 흐름, 타입 모델링이 병목이 되지 않게 만드는 언어 브리지 문제다. | `ts/` | `pnpm run build && pnpm run test` | `verified` |
| Bridge | [01-node-runtime-and-tooling](bridge/01-node-runtime-and-tooling/README.md) | Node.js 런타임에서 파일, env, stream, scripts를 직접 다루며 작은 운영성 감각을 익히는 런타임 브리지 문제다. | `node/` | `pnpm run build && pnpm run test` | `verified` |
| Bridge | [02-http-and-api-basics](bridge/02-http-and-api-basics/README.md) | 프레임워크를 쓰기 전에 HTTP 요청/응답, status code, JSON 직렬화를 직접 구현하며 API의 최소 단위를 익히는 문제다. | `node/` | `pnpm run build && pnpm run test` | `verified` |
| Core | [03-rest-api-foundations](core/03-rest-api-foundations/README.md) | 같은 Books CRUD 문제를 Express와 NestJS로 각각 풀며 계층 분리, DI, 테스트 기본을 비교하는 첫 비교 학습 문제다. | `express/`, `nestjs/` | `pnpm run build && pnpm run test` / `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [04-request-pipeline](core/04-request-pipeline/README.md) | validation, error handling, logging, response shaping을 요청 파이프라인 규약으로 묶어 이후 모든 API의 공통 기반을 만드는 문제다. | `express/`, `nestjs/` | `pnpm run build && pnpm run test && pnpm run test:e2e` / `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [05-auth-and-authorization](core/05-auth-and-authorization/README.md) | JWT 인증과 RBAC 인가를 Express middleware chain과 NestJS guard chain으로 비교하는 보안 기초 문제다. | `express/`, `nestjs/` | `pnpm run build && pnpm run test` / `pnpm run build && pnpm run test` | `verified` |
| Core | [06-persistence-and-repositories](core/06-persistence-and-repositories/README.md) | in-memory 저장소를 SQLite 기반 영속 계층으로 교체하면서 raw SQL과 ORM, repository 패턴의 차이를 비교하는 문제다. | `express/`, `nestjs/` | `pnpm run build && pnpm run test && pnpm run test:e2e` / `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [07-domain-events](core/07-domain-events/README.md) | 도메인 이벤트로 side effect를 서비스 본문에서 분리하고 성공/실패 경계를 테스트로 고정하는 이벤트 설계 문제다. | `express/`, `nestjs/` | `pnpm run build && pnpm run test && pnpm run test:e2e` / `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Applied | [08-production-readiness](applied/08-production-readiness/README.md) | 애플리케이션 코드 바깥의 Docker, config, health, logging, CI, cache, queue, rate limiting을 학습용 서비스에 붙이는 운영성 문제다. | `nestjs/` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Applied | [09-platform-capstone](applied/09-platform-capstone/README.md) | REST, pipeline, auth, persistence, events, 운영성 규약을 단일 NestJS 서비스로 통합해 구조 일관성을 검증하는 capstone 문제다. | `nestjs/` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Applied | [10-shippable-backend-service](applied/10-shippable-backend-service/README.md) | 학습용 capstone을 Postgres, Redis, Docker Compose, Swagger까지 포함한 채용 제출용 NestJS 서비스 표면으로 다시 패키징하는 문제다. | `nestjs/` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |

## 추천 읽기 순서

1. `bridge/00-language-and-typescript`
2. `bridge/01-node-runtime-and-tooling`
3. `bridge/02-http-and-api-basics`
4. `core/03-rest-api-foundations`
5. `core/04-request-pipeline`
6. `core/05-auth-and-authorization`
7. `core/06-persistence-and-repositories`
8. `core/07-domain-events`
9. `applied/08-production-readiness`
10. `applied/09-platform-capstone`
11. `applied/10-shippable-backend-service`

## 함께 보는 문서

- [../../docs/project-catalog.md](../../docs/project-catalog.md)
- [../../docs/verification-matrix.md](../../docs/verification-matrix.md)
- [docs/README.md](docs/README.md)
