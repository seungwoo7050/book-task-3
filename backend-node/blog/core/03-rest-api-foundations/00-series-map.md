# 03-rest-api-foundations series map

이 lab은 `core` 구간의 첫 비교 실험이다. 문제는 단순한 Books CRUD지만, 목적은 CRUD를 하나 더 만드는 데 있지 않다. 같은 계약을 Express와 NestJS가 어디에서 다르게 감싸는지, 그리고 그 차이가 실제 코드와 테스트 표면에서 어떻게 보이는지를 직접 확인하는 데 있다.

이번에 다시 읽어 보니 중심 질문은 세 가지였다.

- Express는 의존성 연결과 HTTP 경계를 어디까지 손으로 드러내는가
- NestJS는 같은 경계를 어떤 decorator와 DI container 안으로 흡수하는가
- 둘 다 테스트는 통과하지만, 런타임 payload validation은 실제로 어디까지 빠져 있는가

그래서 읽는 순서도 Express를 먼저 보는 편이 자연스럽다. `createApp()`에서 `BookService -> BookController -> Router`를 직접 엮는 장면을 먼저 보면, NestJS 쪽 `AppModule -> BooksModule -> BooksController`가 무엇을 숨기고 무엇을 자동화하는지 비교 기준이 생긴다.

## 이 글에서 볼 것

- Express lane의 수동 composition root와 `asyncHandler` 기반 request flow
- NestJS lane의 decorator 기반 controller와 `NotFoundException` 전파
- 두 레인이 같은 CRUD 계약을 통과하지만 둘 다 런타임 validation은 아직 넣지 않았다는 현재 상태

## source of truth

- `core/03-rest-api-foundations/problem/README.md`
- `core/03-rest-api-foundations/README.md`
- `core/03-rest-api-foundations/express/src/app.ts`
- `core/03-rest-api-foundations/express/src/controllers/book.controller.ts`
- `core/03-rest-api-foundations/express/src/routes/book.router.ts`
- `core/03-rest-api-foundations/express/src/services/book.service.ts`
- `core/03-rest-api-foundations/nestjs/src/app.module.ts`
- `core/03-rest-api-foundations/nestjs/src/books/books.controller.ts`
- `core/03-rest-api-foundations/nestjs/src/books/books.service.ts`
- `core/03-rest-api-foundations/nestjs/src/books/dto/create-book.dto.ts`
- `core/03-rest-api-foundations/express/test/e2e/books.e2e.test.ts`
- `core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 service를 HTTP 바깥으로 분리하고, controller/router를 수동으로 연결한다.
2. NestJS에서 같은 CRUD를 module, decorator, DI container 위로 옮긴다.
3. 두 lane 모두 CRUD happy path와 404 계약은 테스트로 고정하지만, 잘못된 payload를 막는 runtime validation은 아직 비어 있음을 확인한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  2 passed (2)
Tests       18 passed (18)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Tests       8 passed (8)
```

```bash
$ node -e "const request=require('supertest'); const {createApp}=require('./dist/app.js'); request(createApp()).post('/books').send({title:''}).end((_,res)=>console.log(res.status,res.body))"
201 { id: '...', title: '' }
```

```bash
$ node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/books').send({title:''}) ..."
201 { id: '...', title: '' }
```

마지막 두 실행은 문서에서 특히 중요하다. DTO 이름은 있지만 Express 쪽은 타입 수준에만 머물고, NestJS 쪽도 `ValidationPipe`와 `class-validator`가 연결돼 있지 않아 둘 다 빈 제목 payload를 받아들인다.

## 다음 프로젝트와의 연결

다음 `04-request-pipeline`은 CRUD 기능보다 그 앞단 규약을 다룬다. validation, error handling, response envelope, logging을 먼저 세워 두어야 이후 auth, persistence, async job 같은 주제가 덜 흔들린다.
