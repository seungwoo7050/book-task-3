# 06-persistence-and-repositories series map

이 프로젝트의 질문은 기능 추가가 아니다. 이미 있던 Books API를 그대로 둔 채, 저장 계층만 in-memory에서 SQLite 기반 영속 계층으로 바꿨을 때 어디까지 경계를 유지할 수 있는지가 핵심이다.

처음 읽을 때는 Express 쪽 `createDatabase`와 `BookRepository`를 먼저 보는 편이 좋다. raw SQL과 DB 초기화가 어떤 책임을 갖는지 잡힌 뒤 NestJS `Repository<Book>`로 넘어가면, 같은 문제를 두 다른 persistence 도구가 어떻게 감싸는지 자연스럽게 비교된다.

## 이 글에서 볼 것

- WAL과 schema 초기화 같은 persistence concern이 어디에 머무는지
- raw SQL repository와 ORM repository가 service 표면을 어떻게 비슷하게 유지하는지
- 저장 전략이 바뀐 뒤에도 CRUD와 validation 계약이 그대로 통과하는지

## source of truth

- `core/06-persistence-and-repositories/README.md`
- `core/06-persistence-and-repositories/problem/README.md`
- `core/06-persistence-and-repositories/express/src/database/init.ts`
- `core/06-persistence-and-repositories/express/src/repositories/book.repository.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`
- `core/06-persistence-and-repositories/express/test/unit/book.repository.test.ts`
- `core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 SQLite 초기화와 raw SQL repository를 만든다.
2. NestJS에서는 `Repository<Book>` 주입으로 같은 CRUD를 persistence에 연결한다.
3. repository unit test와 e2e를 돌려 저장 방식만 바뀌었는지 확인한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       7 passed (7)
test:e2e    6 passed (6)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       5 passed (5)
test:e2e    6 passed (6)
```

## 다음 프로젝트와의 연결

다음 장 `07-domain-events`에서는 저장이 성공한 뒤에만 side effect를 흘려보내기 위해 domain event 계층을 얹는다.
