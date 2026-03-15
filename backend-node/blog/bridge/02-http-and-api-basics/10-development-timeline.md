# 02-http-and-api-basics 개발 타임라인

`02-http-and-api-basics`를 읽고 나면 "프레임워크 없이도 서버를 만들 수 있다"보다 "프레임워크가 대신하던 일이 생각보다 많다"가 더 먼저 남는다. request body를 모으고, JSON을 파싱하고, route를 나누고, 헤더를 확인하고, status code를 결정하는 모든 장면이 그대로 드러나기 때문이다.

## 1. 출발점은 CRUD보다 HTTP 반복 작업을 눈앞에 꺼내는 일이었다

문제 정의는 최소 Books CRUD를 구현하며 HTTP 기본기를 익히라고 하지만, 실제 소스의 핵심은 CRUD 항목 수보다 반복 작업의 노출이다. `app.ts`는 서버 생성부터 route 분기까지 직접 수행한다. 이 프로젝트가 bridge의 끝점인 이유는, 다음 단계에서 프레임워크가 추상화할 대상이 바로 여기 다 보이기 때문이다.

## 2. `readJsonBody`와 `sendJson`이 프레임워크의 그림자를 드러낸다

가장 먼저 눈에 들어오는 건 body parsing과 응답 직렬화다.

```ts
async function readJsonBody(request: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];

  for await (const chunk of request) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }

  const body = Buffer.concat(chunks).toString("utf8");
  if (body.trim().length === 0) {
    return {};
  }

  return JSON.parse(body);
}
```

이 함수는 frameworkless HTTP의 현실을 그대로 보여 준다. JSON body는 자동으로 파싱되지 않는다. 스트림을 읽고, 버퍼를 합치고, 문자열을 만들고, 비어 있으면 `{}`로 처리하고, 그 뒤에야 `JSON.parse()`가 온다.

응답도 마찬가지다.

```ts
function sendJson(response: ServerResponse, statusCode: number, payload: JsonResponse): void {
  response.statusCode = statusCode;
  response.setHeader("content-type", "application/json; charset=utf-8");
  response.end(JSON.stringify(payload));
}
```

이 작은 함수 하나가 나중에 controller helper, response object, interceptor가 무엇을 대신하는지 이해하는 기준점이 된다.

## 3. route matching과 path parameter 추출도 결국 직접 해야 한다

`matchBookId()`와 `createApp()`의 조건문 분기를 보면, router라는 추상화 이전의 상태가 그대로 보인다.

```ts
function matchBookId(url: string): string | null {
  const match = /^\/books\/([^/]+)$/.exec(url);

  return match?.[1] ?? null;
}
```

즉 `GET /books/1`이라는 표면은 실제로는 "method가 GET인가", "url이 정확히 `/books`인가", "regex에 걸리는 id가 있는가"의 조합일 뿐이다. 이걸 한 번 직접 보고 나면, 이후 프레임워크 router가 왜 중요한지 훨씬 선명해진다.

## 4. `BookStore`와 validator를 뺀 순간 최소 계층 경계가 생긴다

작은 예제라도 `app.ts` 안에서 `Map` 조작과 payload 검증까지 다 하게 두면 금방 지저분해진다. 그래서 두 번째 전환점은 `BookStore`와 `validateCreateBookPayload()`를 분리한 데서 나온다.

`BookStore`는 숫자 auto-increment와 in-memory persistence를 담당하고, validator는 title/author/publishedYear 규칙만 담당한다. 이 덕분에 HTTP 계층은 "무슨 규칙이 틀렸는가"보다 "그 규칙 위반을 어떤 status code로 바꿀 것인가"에 집중할 수 있다.

## 5. 이 프로젝트의 진짜 중심은 성공 CRUD보다 실패 status code 분기다

`POST /books` 처리부를 보면 가장 중요한 분기가 어디 있는지 보인다.

```ts
if (!contentType?.startsWith("application/json")) {
  sendJson(response, 415, { message: "content-type must be application/json" });
  return;
}
```

wrong media type은 `415`로 닫힌다. 그다음 catch 블록에서는 malformed JSON인 `SyntaxError`를 `400 Request body must be valid JSON`으로 바꾸고, validator가 던진 일반 `Error`도 `400`으로 돌린다. 없는 책과 없는 route는 각각 `404`다.

이건 아주 작은 서버지만, 바로 이 분기 덕분에 "실패를 어디서 거부했는가"가 HTTP code에 반영된다. 그래서 이 프로젝트는 toy server보다 작은 API 계약 실습에 더 가깝다.

## 6. 테스트는 모든 분기를 덮지는 않지만 어떤 계약을 이미 고정했는지 알려 준다

`node/tests/app.test.ts`는 네 가지를 직접 보증한다.
- `GET /health`의 200 JSON
- `POST /books` 후 `GET /books`, `GET /books/1`
- invalid payload의 400
- wrong content-type의 415

즉 health, create/fetch, validation error, media type error는 테스트로 닫혀 있다. 반면 malformed JSON과 missing book/route는 소스에 구현돼 있지만 이번 테스트에서는 직접 assert 하지 않는다. 문서가 이 차이를 같이 적어 주는 편이 품질이 높다.

## 7. 이번 재실행은 in-memory 서버의 순서 의존성까지 보여 줬다

이번 턴에서 실제로 확인한 흐름은 아래와 같았다.

```bash
COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
COREPACK_ENABLE_AUTO_PIN=0 pnpm start
curl -i http://localhost:3000/health
curl -i http://localhost:3000/books
curl -i -X POST http://localhost:3000/books -H 'content-type: application/json' -d '{"title":"Node for Backend Engineers","author":"Alice","publishedYear":2026}'
curl -i http://localhost:3000/books
curl -i http://localhost:3000/books/1
curl -i -X POST http://localhost:3000/books -H 'content-type: text/plain' -d 'plain text'
```

결과는 다음과 같았다.
- `build` 통과
- `test` 통과, `4` tests passed
- 서버 기동 후 `/health`는 `200`
- 초기 `/books`는 빈 배열
- `POST /books`는 `201`
- 같은 프로세스 안에서 이어진 `/books`, `/books/1`은 `200`
- wrong content-type은 `415`

여기서 중요한 건 이 서버가 in-memory store를 쓰기 때문에 요청 순서가 실제 의미를 가진다는 점이다. `GET /books/1`은 반드시 같은 프로세스 안에서 앞선 `POST /books` 뒤에 읽어야 한다. 이것도 이후 persistence 레이어가 왜 필요한지 미리 보여 주는 단서다.

## 정리

이 프로젝트는 bridge의 마지막 장면답게, HTTP 서버의 가장 작은 골격을 전부 손으로 드러낸다. body parsing, response serialization, route matching, validator 분리, status code 분기, in-memory state라는 요소가 한 번 다 눈에 들어와야, 다음 장에서 Express와 NestJS가 무엇을 진짜로 덜어 주는지 비교할 수 있다.
