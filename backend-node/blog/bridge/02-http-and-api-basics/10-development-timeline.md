# 02-http-and-api-basics development timeline

이 프로젝트를 읽고 나면 "프레임워크 없이도 서버를 만들 수 있다"보다, "프레임워크가 원래 대신해 주던 일이 이렇게 많았구나"가 더 먼저 남는다. body parsing, route matching, `Content-Type`, status code를 모두 직접 적는 순간 HTTP의 기본기가 꽤 선명하게 드러난다.

## 흐름 먼저 보기

1. `app.ts`에서 HTTP 서버의 골격을 직접 세운다.
2. `BookStore`와 validator를 분리해 route handler를 가볍게 만든다.
3. 400/404/415를 나눠 실패 경로를 HTTP 계약으로 고정한다.

## 핸들러를 손으로 펼친 장면

`createApp`을 보면 이 프로젝트가 왜 필요한지 바로 드러난다. 프레임워크 없이 request와 response를 다룬다는 건, 결국 아래 같은 코드를 직접 쓰는 일이다.

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

이 함수가 중요한 이유는, 프레임워크를 쓰면 거의 보이지 않는 body parsing이 사실은 스트림을 읽고 문자열로 합치고 JSON으로 해석하는 별도 단계라는 걸 드러내기 때문이다.

응답도 직접 만든다.

```ts
function sendJson(response: ServerResponse, statusCode: number, payload: JsonResponse): void {
  response.statusCode = statusCode;
  response.setHeader("content-type", "application/json; charset=utf-8");
  response.end(JSON.stringify(payload));
}
```

route 분기도 아주 노골적이다.

```ts
if (method === "GET" && url === "/health") {
  sendJson(response, 200, { status: "ok" });
  return;
}
```

그래서 이 프로젝트는 단순한 HTTP 입문이라기보다, 프레임워크가 자동으로 해 주는 작업을 한 번 눈앞에 꺼내 보는 과정에 가깝다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
build: ok
```

## BookStore를 밖으로 뺀 장면

작은 예제라도 route handler 안에서 모든 규칙을 처리하기 시작하면 금방 복잡해진다. 그래서 두 번째 전환점은 `BookStore`와 validator를 별도 파일로 뺀 데서 나온다.

```ts
export class BookStore {
  private readonly books = new Map<string, BookRecord>();
  private nextId = 1;

  create(payload: CreateBookPayload): BookRecord {
    const book: BookRecord = {
      id: String(this.nextId),
      title: payload.title,
      author: payload.author,
      publishedYear: payload.publishedYear,
    };

    this.books.set(book.id, book);
    this.nextId += 1;
    return book;
  }
}
```

여기서 핵심은 저장 방식이 메모리라는 사실이 아니다. `app.ts`가 이제 직접 `Map`을 건드리지 않고 `store.create(payload)`라는 한 문장으로 도메인 작업을 위임할 수 있게 됐다는 점이 더 중요하다.

validator도 그 경계를 선명하게 만든다.

```ts
if (typeof publishedYear !== "number" || !Number.isInteger(publishedYear)) {
  throw new Error("publishedYear must be an integer");
}
```

이 함수는 status code를 정하지는 않지만, 적어도 "어떤 입력이 도메인 규칙을 벗어났는가"는 먼저 결정해 준다. 그래서 HTTP 계층은 나중에 code를 정하는 역할에 집중할 수 있다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       4 passed (4)
Duration    500ms
```

## 실패 status code를 나눈 장면

마지막 전환점은 성공 CRUD가 아니라 실패 경로를 나눌 때 생긴다. 여기서 이 프로젝트가 단순한 toy server를 넘어 HTTP 기본기 실습이 된다.

```ts
if (!contentType?.startsWith("application/json")) {
  sendJson(response, 415, { message: "content-type must be application/json" });
  return;
}
```

이 `415`는 payload가 틀린 경우와 media type이 틀린 경우를 같은 오류로 보지 않겠다는 선언이다.

JSON parse failure도 따로 다룬다.

```ts
if (error instanceof SyntaxError) {
  sendJson(response, 400, { message: "Request body must be valid JSON" });
  return;
}
```

즉 body가 JSON이 아니어서 파싱이 깨졌을 때와, JSON은 맞지만 필드가 잘못됐을 때를 다른 의미로 보는 것이다. 테스트도 이 경계를 그대로 고정한다.

```ts
await request(createApp())
  .post("/books")
  .set("content-type", "text/plain")
  .send("plain text")
  .expect(415);
```

이제 이 프로젝트는 단순히 책 한 권을 만들고 읽는 예제가 아니다. 어떤 실패를 어떤 HTTP code로 돌려줄지까지 포함한, 가장 작은 API 계약이 된다.

다음 프로젝트에서는 같은 CRUD를 Express와 NestJS로 나눠 구현하면서, 방금 손으로 적었던 이 작업들이 프레임워크 안에서 어떻게 흡수되는지를 비교하게 된다.
