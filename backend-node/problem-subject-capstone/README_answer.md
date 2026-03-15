# backend-node 서버 캡스톤 답안지

이 문서는 Node 트랙의 capstone 두 개를 실제 NestJS 통합 소스 기준으로 정리한 답안지다. 현재 `vanilla` 쪽은 공식 구현 표면이 비어 있고, 실제 해답은 NestJS 프로젝트에 모여 있다. 첫 capstone은 bridge와 core에서 배운 규약을 단일 서비스로 다시 묶는 기준선이고, 두 번째 capstone은 그 기준선을 Postgres, Redis, migration, Swagger, CI까지 갖춘 제출형 서비스 표면으로 확장한다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [09-platform-capstone-nestjs](09-platform-capstone-nestjs_answer.md) | 시작 위치의 구현을 완성해 auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것, native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것, 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 AuthController, AuthModule 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/nestjs && npm run test -- --run` |
| [10-shippable-backend-service-nestjs](10-shippable-backend-service-nestjs_answer.md) | 시작 위치의 구현을 완성해 Postgres migration과 Redis 의존성을 포함한 로컬 실행 흐름을 제공할 것, Swagger, health endpoint, auth/books API를 한 서비스 표면으로 설명할 것, 학습용 capstone과 제출용 서비스의 차이를 문서화할 것을 한 흐름으로 설명하고 검증한다. 핵심은 configureApp와 AppModule, AuthRateLimitService 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/nestjs && npm run test -- --run` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
