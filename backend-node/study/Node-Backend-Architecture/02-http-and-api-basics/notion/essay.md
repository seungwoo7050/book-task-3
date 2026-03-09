# 프레임워크 없이 HTTP 서버를 만들어 보면 보이는 것들

## Express 전에 이걸 하는 이유

대부분의 백엔드 학습 경로는 Express나 NestJS로 바로 들어간다. `app.get('/books', handler)` 한 줄로 라우트가 등록되고, `req.body`에 JSON이 자동으로 들어와 있고, 에러가 나면 프레임워크가 알아서 500을 반환한다. 편리하지만, 이 편리함이 무엇을 대신해 주는지 모르면 나중에 문제가 생겼을 때 디버깅할 수가 없다.

그래서 이 과제는 `node:http` 모듈만으로 HTTP 서버를 만든다. 라우팅을 직접 분기하고, JSON body를 스트림에서 직접 읽어서 파싱하고, 상태 코드를 직접 설정한다. 이걸 한 번 해보면 Express의 `app.use(express.json())`이 무엇을 대신하는지, NestJS의 `@Body()` 데코레이터가 어디까지 추상화하는지 체감할 수 있다.

## 만든 것: Books CRUD + Health Check

이 서버는 네 개의 엔드포인트를 제공한다:

- `GET /health` — 서버 상태 확인 (`{ status: "ok" }`)
- `GET /books` — 저장된 모든 책 목록 조회
- `GET /books/:id` — 특정 책 조회 (없으면 404)
- `POST /books` — 새 책 등록 (title, author, publishedYear 필수)

도메인은 이전 과제의 도서 카탈로그를 이어받았다. 같은 도메인 위에서 "타입 변환"에서 "HTTP API"로 단계가 올라가는 구조다.

## JSON Body 파싱을 직접 하면 알게 되는 것

프레임워크에서는 `req.body`에 파싱된 객체가 들어와 있다. 하지만 날것의 `IncomingMessage`에는 body가 없다. 요청 본문은 **스트림**으로 들어오기 때문에 직접 모아야 한다:

1. `for await (const chunk of request)`로 청크를 수집한다
2. `Buffer.concat(chunks).toString("utf8")`로 문자열로 합친다
3. `JSON.parse(body)`로 파싱한다

이 과정에서 비어 있는 body, 깨진 JSON, 아예 `content-type`이 `application/json`이 아닌 요청을 구분해야 한다. 바로 이 지점에서 **상태 코드의 분화**가 일어난다:

- `content-type`이 `application/json`이 아니면 → `415 Unsupported Media Type`
- JSON 파싱이 실패하면 → `400 Bad Request` ("Request body must be valid JSON")
- 파싱은 됐지만 필수 필드가 누락되면 → `400 Bad Request` ("title is required")

프레임워크를 쓰면 이런 분기가 미들웨어 뒤에 숨는다. 직접 해보면 "400과 415는 실패 시점이 다르다"는 걸 몸으로 느끼게 된다.

## 라우팅을 직접 분기하기

프레임워크의 라우터는 `app.get('/books/:id', handler)` 같은 선언적 API를 제공한다. 프레임워크 없이 하면 `if/else`와 정규식으로 직접 분기해야 한다:

```typescript
if (method === "GET" && url === "/books") { ... }
if (method === "GET") {
  const bookId = matchBookId(url);  // /books/:id 패턴 매칭
  if (bookId) { ... }
}
if (method === "POST" && url === "/books") { ... }
```

이렇게 직접 해보면 라우팅이 결국 "메서드 + URL 패턴 매칭 → 핸들러 디스패치"라는 걸 알게 된다. Express의 `Router()`나 NestJS의 `@Controller()` + `@Get()` 데코레이터가 이 패턴 매칭을 추상화한 것이다.

## in-memory 저장소라는 선택

`BookStore` 클래스는 `Map<string, BookRecord>`으로 책을 저장한다. 서버가 종료되면 데이터는 사라진다.

이 선택은 의도적이다. 이 과제의 목표는 HTTP 계층이고, 영속 계층은 `06-persistence-and-repositories`에서 다룬다. in-memory 저장소를 먼저 만들어 두면, 나중에 SQLite나 Postgres로 교체할 때 **API 계약은 그대로 유지하면서 저장소만 바꾸는** 경험을 할 수 있다.

`BookStore`를 별도 파일(`book-store.ts`)로 분리한 것도 같은 이유다. HTTP 핸들러와 저장소를 섞지 않으면, 나중에 저장소 구현을 교체할 때 HTTP 계층을 건드릴 필요가 없다.

## 검증 로직: validateCreateBookPayload

입력 검증도 직접 함수로 만들었다. `validateCreateBookPayload`는 `unknown` 타입을 받아서:

1. 객체인지 확인한다 (아니면 "Request body must be a JSON object")
2. `title`이 비어 있지 않은 문자열인지 확인한다
3. `author`가 비어 있지 않은 문자열인지 확인한다
4. `publishedYear`가 정수인지 확인한다

통과하면 `CreateBookPayload` 타입을 반환하고, 실패하면 `Error`를 던진다. 이 패턴은 이후 과제에서 `class-validator` DTO로 대체되지만, 원형을 직접 만들어 보면 "검증이란 결국 무엇인가"가 명확해진다.

## 테스트: supertest로 서버 전체를 테스트하기

이 과제에서 처음으로 `supertest`를 사용한다. `supertest`는 HTTP 서버 인스턴스를 받아서 실제 HTTP 요청을 보내고 응답을 검증하는 도구다.

```typescript
await request(createApp())
  .post("/books")
  .set("content-type", "application/json")
  .send({ title: "Node for Backend Engineers", author: "Alice", publishedYear: 2026 })
  .expect(201);
```

`createApp()`이 `http.Server`를 반환하기 때문에, 테스트마다 새로운 서버 인스턴스를 만들 수 있다. in-memory 저장소 덕분에 테스트 간 상태 격리도 자동으로 된다.

테스트에서 커버하는 시나리오:
- health check 응답
- 책 생성 후 목록 조회와 단건 조회
- 빈 title로 생성 시도 → 400
- 잘못된 content-type → 415

## curl로 수동 검증하기

자동 테스트 외에, curl로도 직접 확인할 수 있도록 예시 스크립트를 제공했다:

```bash
# 서버 실행
pnpm start

# 다른 터미널에서
curl http://localhost:3000/health
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": "Bob", "publishedYear": 2026}'
curl http://localhost:3000/books
```

이 습관은 이후의 모든 API 과제에서 유지된다. 자동 테스트가 있더라도, curl로 한 번 직접 쏴보면 API의 실제 동작감이 다르다.

## 이 과제의 위치와 다음 단계

이 과제를 마치면 HTTP 요청/응답 모델, JSON body 파싱, 라우팅, 상태 코드, 입력 검증을 모두 프레임워크 없이 해본 상태가 된다. 다음 과제인 `03-rest-api-foundations`에서 같은 기능을 Express와 NestJS로 다시 만드는데, 그때 프레임워크가 "어디를 대신하는지"가 바로 보인다.

여기서 만든 in-memory `BookStore`의 인터페이스는 이후 `06-persistence-and-repositories`에서 SQLite로 교체할 때까지 동일한 형태로 유지된다. 그리고 `validateCreateBookPayload`의 패턴은 `04-request-pipeline`에서 validation pipe로 발전한다.
