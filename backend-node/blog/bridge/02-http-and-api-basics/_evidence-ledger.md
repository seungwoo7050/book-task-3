# 02-http-and-api-basics Evidence Ledger

## 독립 Todo 판정
- 판정: `done`
- 이유: `problem/README.md`가 별도 성공 기준을 가진 독립 bridge 문제이고, `node/` 워크스페이스가 자체 build/test/server surface를 갖는다.
- 이번 Todo에서도 기존 blog 본문은 입력 근거로 사용하지 않았다.

## 이번 턴에 읽은 근거
- `backend-node/README.md`
- `backend-node/study/Node-Backend-Architecture/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/README.md`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/problem/script/curl-examples.sh`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/package.json`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/book-store.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/main.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tests/app.test.ts`
- `backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/docs/concepts/frameworkless-http.md`

## 소스에서 확인한 핵심 사실
- `createApp()`는 frameworkless HTTP 서버의 route dispatch를 직접 수행한다.
- JSON body parsing은 request stream을 모두 읽은 뒤 `JSON.parse()`를 호출하는 수동 단계다.
- response는 `sendJson()`이 `content-type`과 `JSON.stringify()`를 직접 책임진다.
- `matchBookId()`는 regex로 path parameter를 직접 뽑는다.
- `BookStore`는 in-memory `Map`과 auto-increment id를 사용한다.
- `validateCreateBookPayload()`는 empty title/author와 non-integer `publishedYear`를 `Error`로 거절한다.
- wrong content-type은 `415`, malformed JSON은 `400`, invalid payload도 `400`, missing book/route는 `404`다.
- 테스트는 health, create/fetch, invalid payload, wrong content-type만 직접 덮고, malformed JSON과 missing book/route는 source-only branch다.

## 검증 명령과 실제 결과

| 명령 | 결과 | 메모 |
| --- | --- | --- |
| `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build` | 통과 | `tsc` exit code `0` |
| `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` | 통과 | `1` file, `4` tests passed |
| `COREPACK_ENABLE_AUTO_PIN=0 pnpm start` | 통과 | `HTTP basics server listening on 3000` 출력 |
| `curl -i http://localhost:3000/health` | 통과 | `200 {"status":"ok"}` |
| `curl -i http://localhost:3000/books` | 통과 | 초기 상태 `200 []` |
| `curl -i -X POST http://localhost:3000/books -H 'content-type: application/json' -d '{"title":"Node for Backend Engineers","author":"Alice","publishedYear":2026}'` | 통과 | `201`과 생성된 book 반환 |
| 이후 `curl -i http://localhost:3000/books` | 통과 | `200`과 길이 1 배열 |
| 이후 `curl -i http://localhost:3000/books/1` | 통과 | `200`과 생성된 book 반환 |
| `curl -i -X POST http://localhost:3000/books -H 'content-type: text/plain' -d 'plain text'` | 통과 | `415 {"message":"content-type must be application/json"}` |

## 이번 문서가 기대는 중심 앵커
- HTTP skeleton 앵커: `node/src/app.ts`
- 도메인 경계 앵커: `node/src/book-store.ts`
- 테스트 앵커: `node/tests/app.test.ts`
- 개념 앵커: `docs/concepts/frameworkless-http.md`

## 이번 턴의 품질 메모
- success path만이 아니라 test가 아직 직접 덮지 않는 실패 branch까지 source-based로 구분했다.
- 병렬 요청이 아니라 같은 프로세스 안의 순차 요청으로 in-memory state를 검증했다.
- frameworkless HTTP의 의미를 "불편함"보다 "프레임워크가 무엇을 추상화하는지 보이는 상태"로 다시 썼다.
