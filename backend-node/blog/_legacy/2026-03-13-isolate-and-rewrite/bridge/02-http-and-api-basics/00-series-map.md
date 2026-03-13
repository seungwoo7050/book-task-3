# 02-http-and-api-basics series map

`02-http-and-api-basics`는 backend-node 트랙에서 처음으로 실제 HTTP request/response를 직접 잡는 프로젝트다. 그래서 이 시리즈는 "도메인 규칙을 어디까지 HTTP 바깥에 두고, 어떤 실패 status code를 직접 나눴는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 [`node/src/book-store.ts`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/book-store.ts)에서 도메인 규칙을 먼저 세우고, [`node/src/app.ts`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/src/app.ts)에서 HTTP adapter를 씌우는 순서로 복원한다.
- 검증은 [`node/tests/app.test.ts`](../../../study/Node-Backend-Architecture/bridge/02-http-and-api-basics/node/tests/app.test.ts)와 실제 `pnpm run test` 출력으로 닫는다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   in-memory store, manual route handling, status code 분리가 어떤 순서로 붙었는지 따라간다.
