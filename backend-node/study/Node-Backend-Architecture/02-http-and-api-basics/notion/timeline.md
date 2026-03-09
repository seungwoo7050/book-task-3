# 02-http-and-api-basics — 개발 타임라인

이 문서는 프로젝트의 전체 개발 과정을 순서대로 기록한다.
소스 코드만으로는 알 수 없는 설치 과정, curl 명령, 테스트 도구 선택 등을 담는다.

---

## 1단계: 프로젝트 초기화

### 디렉토리 생성

```bash
mkdir -p 02-http-and-api-basics/node/src
mkdir -p 02-http-and-api-basics/node/tests
mkdir -p 02-http-and-api-basics/problem/code
mkdir -p 02-http-and-api-basics/problem/data
mkdir -p 02-http-and-api-basics/problem/script
mkdir -p 02-http-and-api-basics/docs/concepts
mkdir -p 02-http-and-api-basics/docs/references
```

### 패키지 초기화 및 의존성 설치

```bash
cd node
pnpm init
pnpm add -D typescript @types/node vitest
pnpm add -D supertest @types/supertest
```

이 과제에서 처음으로 `supertest`가 추가된다. HTTP 서버에 실제 요청을 보내서 응답을 검증하는 테스트 도구다. `@types/supertest`도 함께 설치한다.

### TypeScript, Vitest 설정

이전 과제와 동일한 패턴:
- `tsconfig.json`: 루트 `tsconfig.base.json` extends
- `vitest.config.ts`: `environment: "node"`, `globals: true`

### npm 스크립트

```json
{
  "build": "tsc",
  "start": "node dist/main.js",
  "test": "vitest run"
}
```

진입점이 `dist/cli.js`에서 `dist/main.js`로 바뀌었다. 이 프로젝트는 CLI가 아니라 HTTP 서버이기 때문이다.

---

## 2단계: 문제 정의 (problem/)

### 스타터 코드

`problem/code/starter.ts` — `BookRecord`, `CreateBookPayload` 타입과 라우트 규약을 제공했다.

### 샘플 데이터

`problem/data/book-payload.json` — POST 요청 본문 예시를 제공했다.

### curl 예시 스크립트

`problem/script/curl-examples.sh` — health check, 책 생성, 목록 조회에 대한 curl 명령을 제공했다.

### 과제 지침서

`problem/README.md` — 4개의 엔드포인트 구현, JSON body 수동 파싱, 상태 코드 세분화, 테스트 구성을 요구했다.

---

## 3단계: 저장소 구현 (node/src/book-store.ts)

### 구현 내용

1. **타입 정의**: `BookRecord` (id, title, author, publishedYear), `CreateBookPayload` (title, author, publishedYear)
2. **`BookStore` 클래스**: `Map<string, BookRecord>` 기반 in-memory 저장소
   - `list()`: 모든 책 반환
   - `getById(id)`: ID로 조회, 없으면 `undefined`
   - `create(payload)`: 순차 ID 부여 후 저장, 생성된 레코드 반환
3. **`validateCreateBookPayload`**: `unknown` → `CreateBookPayload` 변환, 실패 시 설명적 에러 메시지

---

## 4단계: HTTP 서버 구현 (node/src/app.ts)

### 구현 순서

1. **`readJsonBody` 헬퍼**: `IncomingMessage` 스트림에서 청크를 모아 Buffer로 합치고 JSON 파싱
2. **`sendJson` 헬퍼**: 상태 코드, Content-Type 헤더, JSON body를 한 번에 설정하는 응답 유틸리티
3. **`matchBookId` 헬퍼**: `/books/:id` URL 패턴을 정규식으로 매칭
4. **`createApp` 팩토리**: `http.createServer`로 서버 생성, 라우팅 분기:
   - `GET /health` → 200 + `{ status: "ok" }`
   - `GET /books` → 200 + 전체 목록
   - `GET /books/:id` → 200 또는 404
   - `POST /books` → content-type 검사 → body 파싱 → 검증 → 201 또는 에러
   - 기타 → 404
5. **에러 핸들링**: `SyntaxError`(JSON 파싱 실패) → 400, 일반 `Error`(검증 실패) → 400, 그 외 → 500

### 설계 결정

- `createApp`이 `BookStore` 인스턴스를 주입받을 수 있게 해서, 테스트마다 새 저장소로 격리한다
- 기본값으로 `new BookStore()`를 사용해서, 프로덕션 코드에서는 인자 없이 호출 가능

---

## 5단계: 진입점 구현 (node/src/main.ts)

```typescript
const port = Number(process.env.PORT ?? "3000");
const server = createApp();
server.listen(port, () => {
  process.stdout.write(`HTTP basics server listening on ${port}\n`);
});
```

`PORT` 환경 변수로 포트를 바꿀 수 있고, 기본값은 3000이다.

---

## 6단계: 테스트 작성 (node/tests/app.test.ts)

### 테스트 항목

1. **Health check**: `GET /health` → 200 + `{ status: "ok" }`, Content-Type이 JSON인지 확인
2. **CRUD 흐름**: POST로 책 생성 → GET /books로 목록 확인 → GET /books/1로 단건 확인
3. **검증 실패**: 빈 title로 POST → 400 + "title is required" 메시지 확인
4. **Content-Type 검증**: `text/plain`으로 POST → 415 확인

### supertest 사용 패턴

```bash
# supertest는 http.Server 인스턴스를 직접 받는다
request(createApp()).get("/health").expect(200)
```

포트를 열지 않고도 HTTP 요청/응답을 검증할 수 있다.

---

## 7단계: 빌드와 검증

### 빌드

```bash
cd node
pnpm run build
```

### 테스트 실행

```bash
pnpm run test
```

4개 테스트 케이스 전체 통과.

### 서버 실행 및 curl 수동 검증

```bash
# 서버 실행
pnpm start

# 다른 터미널에서 Health check
curl http://localhost:3000/health

# 책 생성
curl -X POST http://localhost:3000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": "Bob", "publishedYear": 2026}'

# 목록 조회
curl http://localhost:3000/books

# 단건 조회
curl http://localhost:3000/books/1

# 잘못된 요청 — 415 확인
curl -X POST http://localhost:3000/books \
  -H "Content-Type: text/plain" \
  -d 'plain text'
```

---

## 8단계: 문서 작성 (docs/)

### 개념 문서

`docs/concepts/frameworkless-http.md` — 프레임워크 없이 HTTP를 다루면 보이는 것들: 라우팅, JSON body 파싱, 응답 코드 분화, 테스트 방식을 정리했다.

### 참조 자료

`docs/references/checked-sources.md` — Node.js `http` 모듈 API와 MDN HTTP 상태 코드 문서를 다시 확인하고 기록했다.

---

## 프로젝트 파일 구조 최종 상태

```
02-http-and-api-basics/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── frameworkless-http.md
│   └── references/
│       └── checked-sources.md
├── problem/
│   ├── README.md
│   ├── code/
│   │   └── starter.ts
│   ├── data/
│   │   └── book-payload.json
│   └── script/
│       └── curl-examples.sh
└── node/
    ├── package.json
    ├── pnpm-lock.yaml
    ├── tsconfig.json
    ├── vitest.config.ts
    ├── src/
    │   ├── app.ts
    │   ├── book-store.ts
    │   └── main.ts
    └── tests/
        └── app.test.ts
```

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| pnpm | 패키지 매니저 |
| TypeScript 5.6+ | 컴파일러 |
| Vitest 2.1+ | 테스트 러너 |
| supertest 7+ | HTTP 서버 통합 테스트 도구 |
| node:http | 프레임워크 없는 HTTP 서버 |
| curl | 수동 API 검증 |
