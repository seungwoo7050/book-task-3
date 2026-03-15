# backend-node

이 저장소는 Node.js 백엔드 학습 결과물을 쌓아 두는 임시 폴더가 아니라, GitHub 첫 화면에서 바로 `무슨 문제를 풀었는지`, `내 답이 무엇인지`, `어떻게 다시 검증하는지`를 읽히게 만드는 study-first 아카이브다.

## 이 레포가 푸는 문제

- Node.js 백엔드 학습이 언어, 런타임, HTTP, API, auth, persistence, 운영성으로 나뉘어 있는데 이를 한 번에 설명하기 어렵다는 문제
- 학습 레포가 시간이 지나면 “그래서 어떤 문제를 풀었고 공개 답안이 어디 있나”가 흐려지는 문제
- Express와 NestJS를 둘 다 공부해도 비교 기준과 읽는 순서가 레포 표면에서 보이지 않는 문제

## 내가 만든 답

- 활성 트랙을 `study/Node-Backend-Architecture` 하나로 고정하고, 이를 `bridge -> core -> applied` 3그룹으로 재배치했다.
- 각 프로젝트는 `README -> problem -> 구현 레인 -> docs -> notion` 순서로 읽히는 공개 계약을 갖도록 정리했다.
- 루트 문서에서 대표 결과물, 전체 카탈로그, 검증 행렬, 경로 이관 맵을 바로 찾게 했다.

## 대표 결과물

| 프로젝트 | 해결한 문제 | 공개 답안 형태 | 대표 검증 |
| --- | --- | --- | --- |
| [08-production-readiness](study/Node-Backend-Architecture/applied/08-production-readiness/README.md) | 학습용 서비스에 운영 준비 항목을 어디까지 붙일지 정리 | NestJS 운영성 예제 | `pnpm run build && pnpm run test && pnpm run test:e2e` |
| [09-platform-capstone](study/Node-Backend-Architecture/applied/09-platform-capstone/README.md) | 03~08을 하나의 서비스로 통합해 규약 일관성 검증 | NestJS capstone | `pnpm run build && pnpm run test && pnpm run test:e2e` |
| [10-shippable-backend-service](study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md) | 학습용 capstone을 채용 제출용 서비스 표면으로 재패키징 | Postgres + Redis + Compose 기반 NestJS 서비스 | `pnpm run build && pnpm run test && pnpm run test:e2e` |

## 서버 문제지 빠른 진입

- [problem-subject-essential/README.md](problem-subject-essential/README.md): 서버 공통 필수 기준으로 다시 고른 문제지
- [problem-subject-elective/README.md](problem-subject-elective/README.md): essential에 포함되지 않은 나머지 문제지
- [problem-subject-capstone/README.md](problem-subject-capstone/README.md): 트랙 종합 과제만 따로 모은 문제지

## 전체 트랙 카탈로그

| 그룹 | 프로젝트 | 한 줄 문제 | 답 형태 | 상태 |
| --- | --- | --- | --- | --- |
| Bridge | [00-language-and-typescript](study/Node-Backend-Architecture/bridge/00-language-and-typescript/README.md) | Express와 NestJS로 넘어가기 전에 TypeScript, 비동기 흐름, 타입 모델링이 병목이 되지 않게 만드는 언어 브리지 문제다. | `ts/` | `verified` |
| Bridge | [01-node-runtime-and-tooling](study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/README.md) | Node.js 런타임에서 파일, env, stream, scripts를 직접 다루며 작은 운영성 감각을 익히는 런타임 브리지 문제다. | `node/` | `verified` |
| Bridge | [02-http-and-api-basics](study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md) | 프레임워크를 쓰기 전에 HTTP 요청/응답, status code, JSON 직렬화를 직접 구현하며 API의 최소 단위를 익히는 문제다. | `node/` | `verified` |
| Core | [03-rest-api-foundations](study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md) | 같은 Books CRUD 문제를 Express와 NestJS로 각각 풀며 계층 분리, DI, 테스트 기본을 비교하는 첫 비교 학습 문제다. | `express/`, `nestjs/` | `verified` |
| Core | [04-request-pipeline](study/Node-Backend-Architecture/core/04-request-pipeline/README.md) | validation, error handling, logging, response shaping을 요청 파이프라인 규약으로 묶어 이후 모든 API의 공통 기반을 만드는 문제다. | `express/`, `nestjs/` | `verified` |
| Core | [05-auth-and-authorization](study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md) | JWT 인증과 RBAC 인가를 Express middleware chain과 NestJS guard chain으로 비교하는 보안 기초 문제다. | `express/`, `nestjs/` | `verified` |
| Core | [06-persistence-and-repositories](study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md) | in-memory 저장소를 SQLite 기반 영속 계층으로 교체하면서 raw SQL과 ORM, repository 패턴의 차이를 비교하는 문제다. | `express/`, `nestjs/` | `verified` |
| Core | [07-domain-events](study/Node-Backend-Architecture/core/07-domain-events/README.md) | 도메인 이벤트로 side effect를 서비스 본문에서 분리하고 성공/실패 경계를 테스트로 고정하는 이벤트 설계 문제다. | `express/`, `nestjs/` | `verified` |
| Applied | [08-production-readiness](study/Node-Backend-Architecture/applied/08-production-readiness/README.md) | 애플리케이션 코드 바깥의 Docker, config, health, logging, CI, cache, queue, rate limiting을 학습용 서비스에 붙이는 운영성 문제다. | `nestjs/` | `verified` |
| Applied | [09-platform-capstone](study/Node-Backend-Architecture/applied/09-platform-capstone/README.md) | REST, pipeline, auth, persistence, events, 운영성 규약을 단일 NestJS 서비스로 통합해 구조 일관성을 검증하는 capstone 문제다. | `nestjs/` | `verified` |
| Applied | [10-shippable-backend-service](study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md) | 학습용 capstone을 Postgres, Redis, Docker Compose, Swagger까지 포함한 채용 제출용 NestJS 서비스 표면으로 다시 패키징하는 문제다. | `nestjs/` | `verified` |

## 최신 검증 상태

- 구조 이관 기준 최신 검증 기록일은 `2026-03-11`다.
- 전체 검증 행렬과 레인별 명령은 [docs/verification-matrix.md](docs/verification-matrix.md)에 정리했다.
- README 계약과 카탈로그 규칙은 [docs/readme-contract.md](docs/readme-contract.md), [docs/project-catalog.md](docs/project-catalog.md)에서 확인할 수 있다.
- 이전 경로에서 새 그룹 경로로 옮긴 표는 [docs/migration-map.md](docs/migration-map.md)에 정리했다.

## 읽는 순서

1. [docs/README.md](docs/README.md)에서 루트 문서 지도를 확인한다.
2. [study/README.md](study/README.md)에서 활성 학습 영역과 그룹 구성을 본다.
3. [study/Node-Backend-Architecture/README.md](study/Node-Backend-Architecture/README.md)에서 프로젝트 순서와 대표 검증 명령을 고른다.
4. 관심 있는 프로젝트의 `README.md`에서 `문제 / 답 / 검증`을 먼저 읽는다.
5. 필요하면 같은 프로젝트의 `problem/README.md`, 구현 레인 README, `docs/README.md`, `notion/README.md` 순서로 내려간다.
