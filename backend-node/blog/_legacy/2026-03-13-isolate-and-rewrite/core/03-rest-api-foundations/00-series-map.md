# 03-rest-api-foundations series map

`03-rest-api-foundations`는 backend-node 트랙에서 처음으로 같은 문제를 Express와 NestJS 두 번 푼다. 그래서 이 시리즈는 "Books CRUD는 같지만 의존성 연결 방식은 어떻게 달라지는가"라는 질문으로 읽어야 한다.

## 복원 원칙

- chronology는 Express에서 composition root를 먼저 세우고, NestJS에서 container DI로 같은 계약을 다시 만드는 순서로 복원한다.
- 근거는 [`express/src/app.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/express/src/app.ts), [`express/src/services/book.service.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/express/src/services/book.service.ts), [`nestjs/src/books/books.controller.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.controller.ts), [`nestjs/src/books/books.service.ts`](../../../study/Node-Backend-Architecture/core/03-rest-api-foundations/nestjs/src/books/books.service.ts)와 테스트 출력이다.

## 대표 검증

```bash
$ cd express && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ cd ../nestjs && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   Express 수동 DI, NestJS container DI, 공통 CRUD 검증이 어떤 순서로 이어지는지 따라간다.
