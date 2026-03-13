# 02-http-and-api-basics evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md), [`node/src/app.ts`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts), [`node/src/book-store.ts`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/book-store.ts), [`node/tests/app.test.ts`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tests/app.test.ts), 실제 `pnpm run build`, `pnpm run test` 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: HTTP 전에 먼저 in-memory Books 도메인과 payload 검증을 만든다.
- 변경 단위: `node/src/book-store.ts`
- 처음 가설: route를 붙이기 전에 `BookStore`와 `validateCreateBookPayload()`를 분리해 두면 나중에 프레임워크를 바꿔도 도메인 규칙을 그대로 가져갈 수 있다.
- 실제 조치: `Map` 기반 저장소와 `title/author/publishedYear` 검증 함수를 만들었다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`
- 검증 신호: `tsc` 통과.
- 핵심 코드 앵커: `BookStore.create()`, `validateCreateBookPayload()`
- 새로 배운 것: HTTP 입문 프로젝트의 중심도 결국은 request보다 "검증된 payload를 어디서부터 신뢰할 것인가"였다.
- 다음: frameworkless `http.createServer()` 위에 route와 body parsing을 얹는다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: 프레임워크 없이 route, JSON body, status code를 직접 처리한다.
- 변경 단위: `node/src/app.ts`
- 처음 가설: `GET /health`, `GET/POST /books`, `GET /books/:id`만 직접 구현해도 이후 Express/NestJS가 가리는 핵심이 거의 드러난다.
- 실제 조치: `readJsonBody()`, `sendJson()`, `matchBookId()`를 만들고 `createApp()` 안에서 method/url로 직접 분기했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: `✓ tests/app.test.ts (4 tests)`, `Tests 4 passed (4)`
- 핵심 코드 앵커: `readJsonBody()`, `createApp()`
- 새로 배운 것: body parsing, route matching, content-type 검사 같은 일이 프레임워크의 마법이 아니라는 점이 여기서 처음 선명해진다.
- 다음: 실패 경로를 `400`, `404`, `415`로 나눠 테스트로 닫는다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: 성공 CRUD만이 아니라 잘못된 JSON/Content-Type/ID 경계까지 명시한다.
- 변경 단위: `node/src/app.ts`, `node/tests/app.test.ts`
- 처음 가설: 입문 단계일수록 실패 status code를 명시적으로 쪼개야 이후 request pipeline 프로젝트가 자연스럽게 연결된다.
- 실제 조치: `SyntaxError`는 `400`, 잘못된 content-type은 `415`, 존재하지 않는 route/id는 `404`로 분기했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: health 200, create/fetch 201/200, invalid payload 400, wrong content-type 415
- 핵심 코드 앵커: `sendJson()`의 실패 분기
- 새로 배운 것: HTTP 기본기는 CRUD를 만드는 것보다 "왜 이 실패가 400이고 저 실패가 415인가"를 설명하는 데 더 가깝다.
- 다음: [`../../core/03-rest-api-foundations/00-series-map.md`](../../core/03-rest-api-foundations/00-series-map.md)에서 같은 Books 문제를 Express와 NestJS 두 레인으로 다시 푼다.
