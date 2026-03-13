# 03-rest-api-foundations series map

이 프로젝트는 `core` 구간의 시작점이다. 여기서부터는 같은 Books CRUD를 두 프레임워크로 나란히 풀면서, service, controller, router, DI가 어디서 갈라지는지 직접 비교하게 된다.

처음 읽을 때는 Express와 NestJS를 번갈아 보기보다, 먼저 Express 한 번, 그다음 NestJS 한 번 순서로 읽는 편이 자연스럽다. Express 쪽에서 수동 DI와 router 경계를 본 뒤 NestJS로 넘어가면, 어떤 보일러플레이트가 사라지고 무엇이 프레임워크 안으로 흡수됐는지가 더 잘 보인다.

## 이 글에서 볼 것

- Express에서 `BookService`와 router를 왜 따로 세웠는지
- NestJS가 같은 CRUD를 어떤 decorator와 예외 처리 위로 옮겼는지
- 두 레인이 실제로 같은 CRUD 계약을 통과하는지

## source of truth

- `core/03-rest-api-foundations/README.md`
- `core/03-rest-api-foundations/problem/README.md`
- `core/03-rest-api-foundations/express/src/*`
- `core/03-rest-api-foundations/nestjs/src/*`
- `core/03-rest-api-foundations/express/test/unit/book.service.test.ts`
- `core/03-rest-api-foundations/nestjs/test/e2e/books.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 service와 router/controller 경계를 먼저 세운다.
2. NestJS에서 같은 CRUD를 container DI와 decorator 기반 controller로 다시 구성한다.
3. Express는 unit 중심, NestJS는 unit + e2e로 같은 CRUD 계약을 고정한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Test Files  2 passed (2)
Tests       18 passed (18)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       8 passed (8)
test:e2e    8 passed (8)
```

## 다음 프로젝트와의 연결

다음 장 `04-request-pipeline`은 CRUD 기능보다 앞에 오는 규약에 집중한다. validation, error handling, response envelope, logging이 따로 서야 이후 auth와 persistence도 덜 흔들린다.
