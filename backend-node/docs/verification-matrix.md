# Verification Matrix

마지막 구조 이관 기준 최신 기록일은 `2026-03-11`다.

| 그룹 | 프로젝트 | 레인 | 작업 디렉터리 | install | verify | 상태 |
| --- | --- | --- | --- | --- | --- | --- |
| Bridge | [00-language-and-typescript](study/Node-Backend-Architecture/bridge/00-language-and-typescript/README.md) | TypeScript 구현 | `study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts/` | `pnpm install` | `pnpm run build && pnpm run test` | `verified` |
| Bridge | [01-node-runtime-and-tooling](study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/README.md) | Node 구현 | `study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node/` | `pnpm install` | `pnpm run build && pnpm run test` | `verified` |
| Bridge | [02-http-and-api-basics](study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md) | Node HTTP 구현 | `study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/` | `pnpm install` | `pnpm run build && pnpm run test` | `verified` |
| Core | [03-rest-api-foundations](study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md) | Express 레인 | `study/Node-Backend-Architecture/core/03-rest-api-foundations/express/` | `pnpm install` | `pnpm run build && pnpm run test` | `verified` |
| Core | [03-rest-api-foundations](study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md) | NestJS 레인 | `study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [04-request-pipeline](study/Node-Backend-Architecture/core/04-request-pipeline/README.md) | Express 레인 | `study/Node-Backend-Architecture/core/04-request-pipeline/express/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [04-request-pipeline](study/Node-Backend-Architecture/core/04-request-pipeline/README.md) | NestJS 레인 | `study/Node-Backend-Architecture/core/04-request-pipeline/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [05-auth-and-authorization](study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md) | Express 레인 | `study/Node-Backend-Architecture/core/05-auth-and-authorization/express/` | `pnpm install` | `pnpm run build && pnpm run test` | `verified` |
| Core | [05-auth-and-authorization](study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md) | NestJS 레인 | `study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test` | `verified` |
| Core | [06-persistence-and-repositories](study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md) | Express 레인 | `study/Node-Backend-Architecture/core/06-persistence-and-repositories/express/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [06-persistence-and-repositories](study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md) | NestJS 레인 | `study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [07-domain-events](study/Node-Backend-Architecture/core/07-domain-events/README.md) | Express 레인 | `study/Node-Backend-Architecture/core/07-domain-events/express/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Core | [07-domain-events](study/Node-Backend-Architecture/core/07-domain-events/README.md) | NestJS 레인 | `study/Node-Backend-Architecture/core/07-domain-events/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Applied | [08-production-readiness](study/Node-Backend-Architecture/applied/08-production-readiness/README.md) | NestJS 운영성 레인 | `study/Node-Backend-Architecture/applied/08-production-readiness/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Applied | [09-platform-capstone](study/Node-Backend-Architecture/applied/09-platform-capstone/README.md) | NestJS capstone 레인 | `study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |
| Applied | [10-shippable-backend-service](study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md) | NestJS 포트폴리오 레인 | `study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs/` | `pnpm install` | `pnpm run build && pnpm run test && pnpm run test:e2e` | `verified` |

`better-sqlite3`가 로컬 환경에서 native rebuild를 요구하면 각 레인에서 `pnpm rebuild better-sqlite3`를 추가로 실행한다.
