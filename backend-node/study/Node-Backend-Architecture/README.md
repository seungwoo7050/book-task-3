# Node-Backend-Architecture

이 트랙은 완전 초보를 Node.js 백엔드 주니어 준비 수준까지 끌어올리고,
실무에서 자주 마주치는 운영과 아키텍처 트레이드오프를 미드 초입 수준으로 소개하는 학습 경로다.

## 트랙 운영 원칙

- Express는 원리 학습 레인으로 본다.
- NestJS는 실무 적용 레인으로 본다.
- `verified`는 이 디렉터리에서 실제로 다시 실행한 검증만 의미한다.
- legacy 코드를 옮겨온 프로젝트라도 검증을 다시 하기 전까지는 `reference-only` 또는 `in-progress`다.
- 공통 환경 복구 문서는 `docs/` 아래에 둔다.

## 프로젝트 목록

| ID | 프로젝트 | 상태 | 구현 레인 |
|---|---|---|---|
| `00` | `00-language-and-typescript` | `verified` | `ts/` |
| `01` | `01-node-runtime-and-tooling` | `verified` | `node/` |
| `02` | `02-http-and-api-basics` | `verified` | `node/` |
| `03` | `03-rest-api-foundations` | `verified` | `express/`, `nestjs/` |
| `04` | `04-request-pipeline` | `verified` | `express/`, `nestjs/` |
| `05` | `05-auth-and-authorization` | `verified` | `express/`, `nestjs/` |
| `06` | `06-persistence-and-repositories` | `verified` | `express/`, `nestjs/` |
| `07` | `07-domain-events` | `verified` | `express/`, `nestjs/` |
| `08` | `08-production-readiness` | `verified` | `nestjs/` |
| `09` | `09-platform-capstone` | `verified` | `nestjs/` |
| `10` | `10-shippable-backend-service` | `verified` | `nestjs/` |

## 추천 학습 순서

1. `00-language-and-typescript`
2. `01-node-runtime-and-tooling`
3. `02-http-and-api-basics`
4. `03-rest-api-foundations`
5. `04-request-pipeline`
6. `05-auth-and-authorization`
7. `06-persistence-and-repositories`
8. `07-domain-events`
9. `08-production-readiness`
10. `09-platform-capstone`
11. `10-shippable-backend-service`

## 공개 상태 요약

- 바로 학습 가능한 프로젝트: `00`, `01`, `02`, `03`, `04`, `05`, `08`
- native dependency 준비 후 바로 학습 가능한 프로젝트: `06`, `07`, `09`
- 포트폴리오 제출용으로 바로 읽히는 프로젝트: `10`
- 전체 프로젝트는 새 경로 기준 build/test 재검증을 마쳤다.

`06`, `07`, `09`는 `better-sqlite3`를 사용하므로 설치 뒤 `pnpm approve-builds`와
`pnpm rebuild better-sqlite3`가 필요할 수 있다.
처음 설치하거나 sqlite binding 오류가 나면 [native-sqlite-recovery.md](docs/native-sqlite-recovery.md)를 먼저 확인한다.

`10-shippable-backend-service`는 sqlite가 아니라 `Postgres + Redis + Docker Compose`를 사용한다.
이 프로젝트는 `09`를 대체하지 않고, 주니어 웹 백엔드 지원용 보강 과제로 추가된 포트폴리오 단계다.
