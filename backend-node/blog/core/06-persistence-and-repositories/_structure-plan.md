# 06-persistence-and-repositories structure plan

이 문서는 SQLite 기능 소개보다 "저장 전략만 바꾸고 상위 계약은 어디까지 유지했는가"가 먼저 읽혀야 한다. 서사의 중심은 `Express raw SQL boundary -> Nest ORM boundary -> 기본 DB 경로 차이 -> 테스트/복구 범위`다.

## 읽기 구조

1. 왜 controller보다 DB bootstrap과 repository를 먼저 봐야 하는지부터 잡는다.
2. Express `createDatabase`, `main.ts`, `BookRepository`로 raw SQL 경계를 보여 준다.
3. NestJS `AppModule`, `BooksModule`, `BooksService`, `Book` entity로 ORM 위임 방식을 잇는다.
4. Express 기본 DB가 `bookstore.db`, Nest 기본 DB가 `:memory:`라는 비대칭을 분리해서 적는다.
5. 마지막에는 테스트 격리 방식과 `better-sqlite3` recovery 문서를 함께 연결한다.

## 반드시 남길 근거

- `docs/native-sqlite-recovery.md`
- Express `src/database/init.ts`
- Express `src/main.ts`
- Express `src/repositories/book.repository.ts`
- Express repository unit/e2e 결과
- NestJS `src/app.module.ts`
- NestJS `src/books/books.service.ts`
- NestJS `src/books/entities/book.entity.ts`
- NestJS unit/e2e 결과
- 두 레인의 build/test/e2e 재실행 결과

## 리라이트 톤

- SQL 튜토리얼처럼 쓰지 않는다.
- raw SQL과 ORM의 차이를 기능 비교보다 boundary 비교로 쓴다.
- 테스트가 덮는 것과 source만으로 확인한 초기화 세부를 섞지 않는다.
