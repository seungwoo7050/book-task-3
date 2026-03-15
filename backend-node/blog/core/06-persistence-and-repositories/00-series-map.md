# 06-persistence-and-repositories series map

이 lab의 핵심은 "SQLite를 붙였다"가 아니다. 이미 존재하던 Books API의 바깥 계약을 유지한 채, 안쪽 저장 전략만 in-memory에서 database-backed persistence로 교체할 수 있는지를 보는 데 있다. 그래서 중요한 건 기능 추가보다 boundary discipline이다.

이번에 다시 추적하면서 눈에 띈 사실은 두 레인이 같은 "SQLite 기반 영속 계층"을 말하면서도 기본 실행 성격이 완전히 같지는 않다는 점이었다. Express는 `main.ts` 기본값이 `bookstore.db` 파일이고, NestJS는 `AppModule`에서 `DB_PATH`가 없으면 `:memory:`를 쓴다. 즉 둘 다 SQLite를 쓰지만, 기본 재시작 지속성은 동일하지 않다.

## 이 글에서 볼 것

- Express가 raw SQL repository와 row mapping으로 persistence concern을 어떻게 격리하는지
- NestJS가 `Repository<Book>`와 entity metadata로 같은 CRUD 계약을 어떻게 유지하는지
- native `better-sqlite3` 준비, 테스트 격리, 기본 DB 경로 차이까지 포함해 "정말 같은 persistence 전환인지"를 어디까지 말할 수 있는지

## source of truth

- `core/06-persistence-and-repositories/problem/README.md`
- `core/06-persistence-and-repositories/README.md`
- `docs/native-sqlite-recovery.md`
- `core/06-persistence-and-repositories/express/src/database/init.ts`
- `core/06-persistence-and-repositories/express/src/main.ts`
- `core/06-persistence-and-repositories/express/src/repositories/book.repository.ts`
- `core/06-persistence-and-repositories/express/src/routes/book.router.ts`
- `core/06-persistence-and-repositories/express/test/unit/book.repository.test.ts`
- `core/06-persistence-and-repositories/express/test/e2e/database.e2e.test.ts`
- `core/06-persistence-and-repositories/nestjs/src/app.module.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/books.module.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/entities/book.entity.ts`
- `core/06-persistence-and-repositories/nestjs/test/unit/books.service.test.ts`
- `core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 DB bootstrap과 raw SQL repository를 따로 세워 SQL과 row mapping을 안쪽에 가둔다.
2. NestJS에서는 TypeORM entity와 framework repository를 주입해 같은 CRUD 언어를 유지한다.
3. 두 레인 모두 unit/e2e는 `:memory:` DB를 써서 테스트를 격리하고, native `better-sqlite3`가 준비된 상태에서 build/test/e2e가 통과하는지 확인한다.
4. 다만 런타임 기본값은 Express가 파일 DB, NestJS가 in-memory라서 "기본 persistence behavior"까지 완전히 같다고 말할 수는 없다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       13 passed (13)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       11 passed (11)
```

```bash
$ pnpm install
$ pnpm approve-builds
$ pnpm rebuild better-sqlite3
```

현재 환경에서는 위 복구 단계 없이도 build/test/e2e가 모두 통과했지만, README와 공통 recovery 문서는 native binding 문제가 생길 때 이 순서를 기준으로 복구하도록 안내한다.

## 다음 프로젝트와의 연결

다음 `07-domain-events`는 저장이 성공한 이후에만 side effect를 흘리는 구조를 올린다. 그래서 이 lab은 SQLite 실습이라기보다, 이후 event/outbox 논의가 기대는 저장 경계를 먼저 단단히 만드는 단계로 읽는 편이 자연스럽다.
