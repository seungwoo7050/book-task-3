# 02-http-and-api-basics development timeline

이 프로젝트는 backend-node 트랙에서 처음으로 HTTP를 프레임워크 없이 직접 다룬다. 그래서 코드를 읽는 가장 좋은 방법도 "어떤 route를 만들었는가"보다 "도메인 규칙을 어디까지 HTTP 바깥에 남겨 두었는가"를 먼저 보는 것이다. 실제 구현 순서는 `book-store.ts`에서 payload와 저장소를 세우고, `app.ts`에서 request adapter를 붙인 뒤, 테스트로 status code 경계를 고정하는 흐름으로 남아 있다.

## 구현 순서 요약

- `BookStore`와 payload validator로 도메인 규칙을 먼저 만든다.
- `http.createServer()` 위에서 route, body parsing, JSON response를 직접 처리한다.
- CRUD 성공 path와 `400/404/415` 실패 path를 테스트로 닫는다.

## Phase 1

- 당시 목표: HTTP adapter가 없어도 동작하는 작은 Books 도메인을 만든다.
- 변경 단위: `node/src/book-store.ts`
- 처음 가설: route 안에서 곧바로 payload를 만지면 이후 Express/NestJS 비교가 어려워진다. 저장소와 validator를 먼저 분리해야 한다.
- 실제 진행: `BookStore`가 `Map`과 `nextId`를 관리하고, `validateCreateBookPayload()`가 title/author/year를 검사한다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/app.test.ts (4 tests)
Tests 4 passed (4)
```

검증 신호:

- 생성 성공 시 ID가 `"1"`부터 붙는다.
- 빈 title이나 정수가 아닌 `publishedYear`는 도메인 레벨에서 거부된다.

핵심 코드:

```ts
if (typeof title !== "string" || title.trim().length === 0) {
  throw new Error("title is required");
}
```

왜 이 코드가 중요했는가:

HTTP 프로젝트인데도 가장 먼저 고정한 규칙이 route가 아니라 payload validation이라는 점이 중요하다. 이 경계 덕분에 다음 프로젝트에서 Express controller나 Nest DTO가 들어와도 핵심 판단은 그대로 유지된다.

새로 배운 것:

- API 입문은 URL보다도 "언제부터 payload를 유효한 데이터로 취급할 것인가"를 정하는 일이다.

## Phase 2

- 당시 목표: 프레임워크 없는 서버에서 route와 body parsing을 직접 묶는다.
- 변경 단위: `node/src/app.ts`
- 처음 가설: `GET /health`, `GET/POST /books`, `GET /books/:id` 정도만 직접 구현해도 HTTP의 핵심 기계부품은 대부분 다 만져 볼 수 있다.
- 실제 진행: `readJsonBody()`가 request stream을 모아 JSON으로 파싱하고, `sendJson()`이 header와 body를 쓰며, `matchBookId()`가 path parameter를 정규식으로 뽑는다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/app.test.ts (4 tests)
Tests 4 passed (4)
```

검증 신호:

- `GET /health`는 `200 { status: "ok" }`로 닫힌다.
- `POST /books` 후 `GET /books`, `GET /books/1`이 같은 메모리 저장소를 공유한다.

핵심 코드:

```ts
if (method === "POST" && url === "/books") {
  const contentType = request.headers["content-type"];
  if (!contentType?.startsWith("application/json")) {
    sendJson(response, 415, { message: "content-type must be application/json" });
    return;
  }
```

왜 이 코드가 중요했는가:

프레임워크를 쓰면 흔히 안 보이는 `content-type` 검사와 route 분기가 여기선 노출된다. 이 프로젝트의 목적은 바로 그 숨겨진 기본값을 손으로 보는 데 있다.

새로 배운 것:

- body parsing은 도메인 로직이 아니라 transport adapter 책임이다. 그래서 `BookStore`가 아니라 `app.ts`에 남아 있어야 한다.

## Phase 3

- 당시 목표: 성공 CRUD뿐 아니라 실패 status code의 이유를 테스트로 고정한다.
- 변경 단위: `node/src/app.ts`, `node/tests/app.test.ts`
- 처음 가설: 입문 프로젝트일수록 "무엇이 실패하는가"를 명확히 나눠야 이후 request pipeline, auth, exception filter가 자연스럽게 이어진다.
- 실제 진행: 잘못된 JSON은 `400`, 잘못된 content-type은 `415`, 없는 route나 book id는 `404`로 응답하게 했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/app.test.ts (4 tests)
Tests 4 passed (4)
```

검증 신호:

- invalid payload test는 `title is required`를 포함한 `400`을 검증한다.
- text/plain 요청은 `415`로 거절된다.
- 책이 없으면 `404 Book not found`가 나온다.

핵심 코드:

```ts
if (error instanceof SyntaxError) {
  sendJson(response, 400, { message: "Request body must be valid JSON" });
  return;
}
```

왜 이 코드가 중요했는가:

여기서부터 HTTP 실패는 하나의 큰 에러가 아니라 "파싱 실패", "검증 실패", "라우팅 실패"처럼 다른 원인으로 분기된다. 다음 `request-pipeline` 프로젝트가 바로 이 차이를 공통 규약으로 끌어올린다.

새로 배운 것:

- CRUD를 만든다는 건 결국 성공 path보다 실패 path를 더 잘 설명할 수 있게 되는 일이다.

다음:

- [`../../core/03-rest-api-foundations/00-series-map.md`](../../core/03-rest-api-foundations/00-series-map.md)에서 같은 문제를 Express와 NestJS 두 레인으로 다시 푼다.
