# Curriculum Map

## 목표 재정의

이 저장소의 목표는 `완전 초보 -> Node.js 백엔드 주니어 준비 완료 + 미드 초입 개념 이해`다.
이 목표는 세 층으로 나눈다.

1. 입문 브리지: 언어, 런타임, HTTP 기초
2. 주니어 코어: REST, 요청 파이프라인, 인증/인가, DB, 이벤트
3. 미드 입문: 운영, 배포, 관측성, 통합 아키텍처

## 왜 legacy 순서를 그대로 쓰지 않는가

legacy는 비교 학습 자료로는 유효하지만, 초보 학습 경로로 쓰기에는 다음 보강이 필요했다.

- 바로 Express/NestJS 테스트부터 시작해 언어와 Node 런타임 기초가 빠져 있었다.
- 인증보다 먼저 요청 검증과 에러 흐름을 이해하는 순서가 더 명확하다.
- 이벤트 이후 바로 capstone으로 넘어가 운영/배포/관측성 브리지가 부족했다.

## 새 프로젝트 순서

| 단계 | 프로젝트 | 목적 |
|---|---|---|
| Bridge | `00-language-and-typescript` | JS, TS, 비동기, 모듈, 에러 처리 기초 |
| Bridge | `01-node-runtime-and-tooling` | Node 런타임, 파일 시스템, env, 스크립트, 디버깅 |
| Bridge | `02-http-and-api-basics` | HTTP 요청/응답, JSON, REST, 간단한 서버 |
| Core | `03-rest-api-foundations` | 계층 분리, DI, Express vs NestJS 비교의 출발점 |
| Core | `04-request-pipeline` | validation, error, logging, response shaping |
| Core | `05-auth-and-authorization` | JWT, RBAC, middleware/guard chain |
| Core | `06-persistence-and-repositories` | SQLite, repository pattern, raw SQL vs ORM |
| Core | `07-domain-events` | side effect 분리, event bus, 발행/구독 경계 |
| Mid Intro | `08-production-readiness` | Docker, config, logging, health, CI, rate limit, cache, queue |
| Mid Intro | `09-platform-capstone` | 03~08을 단일 NestJS 서비스에 통합 |
| Mid Intro | `10-shippable-backend-service` | 09를 Postgres + Redis + Compose + Swagger 기반 포트폴리오 서비스로 강화 |

## 구현 레인 정책

- `express/`: 원리 학습 레인. 프레임워크가 가리는 경계를 직접 본다.
- `nestjs/`: 실무 적용 레인. 모듈, DI, 가드, 필터, 인터셉터를 실제 팀 코드 형태로 본다.
- `03`~`07`은 비교 학습을 위해 두 레인을 모두 유지한다.
- `08`~`10`은 실무 지향 주제를 집중하기 위해 NestJS 단일 레인으로 간다.

## 왜 10번 과제를 추가했는가

`09-platform-capstone`은 학습용 통합 과제로는 충분하지만, 채용 관점에서 바로 읽히는 산출물은 아니었다.
`10-shippable-backend-service`는 다음 공백을 메운다.

- SQLite 중심 예제를 Postgres migration 기반 서비스로 바꿔 실무 친화도를 높인다.
- Redis 캐시와 로그인 throttling을 추가해 운영 설계의 우선순위를 보여 준다.
- Docker Compose, Swagger, seed script, CI service container를 한 묶음으로 제공해 재현성과 온보딩 속도를 높인다.
- `09`는 학습용 capstone으로 유지하고, `10`은 제출용 포트폴리오 서비스로 분리해 두 목적을 섞지 않는다.
