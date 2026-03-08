# Skill Matrix

## 기대 수준 정의

- `기초`: 용어와 기본 문법을 이해하고 작은 예제를 스스로 수정할 수 있다.
- `주니어`: 구현, 테스트, 디버깅, 문서화까지 한 사이클을 스스로 끝낼 수 있다.
- `미드 입문`: 운영과 트레이드오프를 설명하고 설계 선택의 이유를 말할 수 있다.

## 프로젝트별 학습 성과

| 프로젝트 | 핵심 역량 | 기대 수준 |
|---|---|---|
| `00-language-and-typescript` | 타입, 함수, 객체, async/await, 에러 처리 | 기초 |
| `01-node-runtime-and-tooling` | env, fs, path, streams, scripts, debugging | 기초 |
| `02-http-and-api-basics` | HTTP, REST, status code, JSON, 간단한 서버 | 기초 |
| `03-rest-api-foundations` | Router/Controller/Service, DI, 모듈, 테스트 기본 | 주니어 초입 |
| `04-request-pipeline` | validation, 예외 계층, 로깅, 응답 규약 | 주니어 |
| `05-auth-and-authorization` | JWT, RBAC, 401/403 경계, 보안 테스트 | 주니어 |
| `06-persistence-and-repositories` | persistence, repository, migration 개념, transaction 기초 | 주니어 |
| `07-domain-events` | event-driven 분리, negative case 검증, side effect 격리 | 주니어 |
| `08-production-readiness` | Docker, health check, config, cache, queue, rate limit, CI | 미드 입문 |
| `09-platform-capstone` | 아키텍처 통합, 운영 규약 일치, 트레이드오프 설명 | 미드 입문 |
| `10-shippable-backend-service` | Postgres migration, Redis cache/throttle, Compose, Swagger, recruiter-facing 문서화 | 미드 입문 |

## 면접/실무 관점 체크

이 트랙을 마치면 다음 질문에 답할 수 있어야 한다.

- 왜 Express와 NestJS를 둘 다 배웠는가
- validation과 auth를 왜 분리해서 학습하는가
- raw SQL과 ORM은 무엇을 각각 잘하는가
- 이벤트는 언제 도입하고, 언제 과한가
- health check, rate limiting, cache, queue는 각각 어떤 문제를 해결하는가
- 왜 학습용 capstone과 제출용 shippable service를 분리했는가
