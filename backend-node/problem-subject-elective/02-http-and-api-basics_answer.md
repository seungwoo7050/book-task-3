# 02-http-and-api-basics 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 JSON body parsing과 route dispatch를 직접 구현할 것, GET /books, GET /books/:id, POST /books 중심 계약을 검증할 것, status code와 헤더 오류를 테스트로 확인할 것을 한 흐름으로 설명하고 검증한다. 핵심은 `readJsonBody`와 `sendJson`, `matchBookId` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- JSON body parsing과 route dispatch를 직접 구현할 것
- GET /books, GET /books/:id, POST /books 중심 계약을 검증할 것
- status code와 헤더 오류를 테스트로 확인할 것
- 첫 진입점은 `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts`이고, 여기서 `readJsonBody`와 `sendJson` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts`: `readJsonBody`, `sendJson`, `matchBookId`, `createApp`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/book-store.ts`: `BookStore`, `validateCreateBookPayload`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/main.ts`: `port`, `server`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/code/starter.ts`: `ROUTES`, `validateCreateBookPayload`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tests/app.test.ts`: `frameworkless http server`, `returns health information`, `creates and fetches a book`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/pnpm-lock.yaml`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tsconfig.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/data/book-payload.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/code/starter.ts`와 `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `frameworkless http server` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node && npm run test -- --run`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node && npm run test -- --run
```

- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/code/starter.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `frameworkless http server`와 `returns health information`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node && npm run test -- --run`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/book-store.ts`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/main.ts`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/code/starter.ts`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tests/app.test.ts`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/pnpm-lock.yaml`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tsconfig.json`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/data/book-payload.json`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/script/curl-examples.sh`
- `../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/package.json`
