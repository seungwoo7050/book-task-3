# 03-rest-api-foundations structure plan

이 문서는 "Express와 NestJS로 CRUD를 만들었다"보다 "같은 CRUD를 두 프레임워크가 어디서 다르게 감싸는가, 그리고 둘 다 아직 무엇을 하지 않는가"가 먼저 읽혀야 한다. 서사의 중심은 `manual composition -> framework DI -> 테스트가 고정한 계약 -> validation 부재 확인`이다.

## 읽기 구조

1. 왜 이 lab이 `core`의 첫 비교 실험인지 먼저 짚는다.
2. Express lane에서 `createApp`, `BookService`, `createBookRouter`, `asyncHandler`를 묶어 manual composition을 보여 준다.
3. NestJS lane에서 `AppModule`, `BooksModule`, `BooksController`, `BooksService`로 같은 문제를 어떻게 프레임워크 안으로 넣는지 잇는다.
4. 테스트 통과 신호를 정리하되, 마지막에는 invalid payload 재실행으로 runtime validation 부재를 분명히 남긴다.

## 반드시 남길 근거

- Express `src/app.ts`
- Express `src/routes/book.router.ts`
- Express `src/services/book.service.ts`
- NestJS `src/app.module.ts`
- NestJS `src/books/books.controller.ts`
- NestJS `src/books/books.service.ts`
- NestJS `src/books/dto/create-book.dto.ts`
- NestJS `src/main.ts`
- Express `pnpm run build`, `pnpm run test`
- NestJS `pnpm run build`, `pnpm run test`, `pnpm run test:e2e`
- 두 lane의 invalid payload 직접 재실행 결과

## 리라이트 톤

- 프레임워크 우열 비교나 취향 평가로 쓰지 않는다.
- "같은 문제를 다른 표면으로 감싼다"는 느낌이 먼저 살아야 한다.
- 테스트가 통과해도 아직 validation이 비어 있다는 현재 한계를 숨기지 않는다.
