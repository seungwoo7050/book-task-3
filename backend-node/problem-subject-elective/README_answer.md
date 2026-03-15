# backend-node 서버 개발 비필수 답안지

이 문서는 Node 트랙의 bridge와 core 과제들을 실제 TypeScript, Node, Express, NestJS 소스 기준으로 다시 정리한 답안지다. bridge 구간은 런타임과 HTTP 입문을 다루고, core 구간은 같은 Books API를 프레임워크별로 비교하면서 요청 파이프라인, 인증, 영속성, 이벤트 설계를 어떻게 코드에 고정하는지 보여 준다.

## Bridge

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [00-language-and-typescript](00-language-and-typescript_answer.md) | 시작 위치의 구현을 완성해 입력 데이터를 타입으로 모델링하고 기본 검증을 수행할 것, 비동기 유틸리티와 에러 처리를 테스트로 검증할 것, CLI 실행 예시를 README만 보고 바로 재현할 수 있을 것을 한 흐름으로 설명하고 검증한다. 핵심은 toSlugPart와 normalizeTags, toNormalizedBook 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/ts && npm run test -- --run` |
| [01-node-runtime-and-tooling](01-node-runtime-and-tooling_answer.md) | 시작 위치의 구현을 완성해 NDJSON 로그를 줄 단위로 읽고 집계 결과를 출력할 것, 출력 포맷과 파일 경로 오류를 테스트로 검증할 것, README의 단일 명령으로 실행 흐름을 다시 재현할 수 있을 것을 한 흐름으로 설명하고 검증한다. 핵심은 runCli와 readRequestLog, summarizeRequests 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/node && npm run test -- --run` |
| [02-http-and-api-basics](02-http-and-api-basics_answer.md) | 시작 위치의 구현을 완성해 JSON body parsing과 route dispatch를 직접 구현할 것, GET /books, GET /books/:id, POST /books 중심 계약을 검증할 것, status code와 헤더 오류를 테스트로 확인할 것을 한 흐름으로 설명하고 검증한다. 핵심은 readJsonBody와 sendJson, matchBookId 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node && npm run test -- --run` |
| [03-rest-api-foundations-nestjs](03-rest-api-foundations-nestjs_answer.md) | 시작 위치의 구현을 완성해 두 레인 모두 GET/POST/PUT/DELETE /books 계약을 구현할 것, service가 HTTP 세부사항에 의존하지 않게 분리할 것, 두 레인의 테스트와 실행 명령이 README에 명시될 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 BooksController, BooksModule 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs && npm run test -- --run` |
| [04-request-pipeline-nestjs](04-request-pipeline-nestjs_answer.md) | 시작 위치의 구현을 완성해 성공 응답 형식과 실패 응답 형식을 일관되게 유지할 것, Express와 NestJS 각각에서 파이프라인 지점을 명확히 나눌 것, unit/e2e 테스트로 규약을 다시 확인할 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 BooksController, BooksModule 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/04-request-pipeline/nestjs && npm run test -- --run` |
| [05-auth-and-authorization-nestjs](05-auth-and-authorization-nestjs_answer.md) | 시작 위치의 구현을 완성해 로그인과 보호된 쓰기 경로를 구현할 것, 과 403을 테스트에서 구분할 것, Express와 NestJS 각각의 인증 훅 포인트를 설명할 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 AuthController, AuthModule 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/05-auth-and-authorization/nestjs && npm run test -- --run` |
| [06-persistence-and-repositories-nestjs](06-persistence-and-repositories-nestjs_answer.md) | 시작 위치의 구현을 완성해 두 레인 모두 CRUD 계약을 유지한 채 저장 계층을 바꿀 것, better-sqlite3 설치와 복구 절차를 문서화할 것, unit/e2e 테스트로 저장 전략 교체 이후 동작을 검증할 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 BooksController, BooksModule 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/nestjs && npm run test -- --run` |
| [07-domain-events-nestjs](07-domain-events-nestjs_answer.md) | 시작 위치의 구현을 완성해 도메인 이벤트와 리스너를 명시적으로 분리할 것, 성공/실패 경로의 이벤트 발행 여부를 테스트할 것, native SQLite 의존성을 포함한 재현 절차를 문서화할 것을 한 흐름으로 설명하고 검증한다. 핵심은 AppModule와 BooksController, BooksModule 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/core/07-domain-events/nestjs && npm run test -- --run` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
