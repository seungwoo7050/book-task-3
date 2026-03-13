# 02-http-and-api-basics series map

이 프로젝트는 bridge의 마지막 단계에서 HTTP를 한 번 손으로 다뤄 보는 실험이다. Express와 NestJS로 넘어가기 전에, request body를 어떻게 읽는지, `Content-Type`을 어디서 검사하는지, 400과 415를 왜 다르게 돌려줘야 하는지를 몸으로 확인하는 구간이라고 보는 편이 더 정확하다.

처음 읽을 때는 `app.ts`를 먼저 보는 편이 좋다. 여기서 route 분기와 JSON 응답을 어떻게 직접 쓰는지 잡히면, `book-store.ts`가 왜 별도 파일로 빠졌는지도 자연스럽게 따라온다.

## 이 글에서 볼 것

- frameworkless HTTP 서버가 실제로 어떤 반복 작업을 들고 있는지
- payload validator와 in-memory store를 밖으로 빼면 무엇이 단순해지는지
- `400`, `404`, `415`가 각각 어느 실패를 가리키는지

## source of truth

- `bridge/02-http-and-api-basics/README.md`
- `bridge/02-http-and-api-basics/problem/README.md`
- `bridge/02-http-and-api-basics/node/src/app.ts`
- `bridge/02-http-and-api-basics/node/src/book-store.ts`
- `bridge/02-http-and-api-basics/node/tests/app.test.ts`

## 구현 흐름 한눈에 보기

1. `createApp`에서 health/books/books/:id/books POST를 직접 분기한다.
2. `BookStore`와 `validateCreateBookPayload`로 도메인 규칙을 route 바깥으로 뺀다.
3. malformed JSON, wrong `Content-Type`, invalid payload, missing book을 각기 다른 status code로 묶는다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
build: ok

$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       4 passed (4)
Duration    500ms
```

## 다음 프로젝트와의 연결

다음 장 `03-rest-api-foundations`에서는 같은 Books CRUD를 Express와 NestJS 두 레인으로 나눠 푼다. 지금 손으로 적었던 HTTP 작업을 프레임워크가 어떻게 흡수하는지가 그때부터 비교 대상으로 올라온다.
