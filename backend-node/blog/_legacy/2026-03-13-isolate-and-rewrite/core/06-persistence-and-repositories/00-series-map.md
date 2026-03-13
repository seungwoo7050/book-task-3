# 06-persistence-and-repositories series map

`06-persistence-and-repositories`는 이 트랙에서 처음으로 저장 계층을 메모리 밖으로 밀어내는 단계다. 그래서 이 시리즈는 "API 표면은 유지한 채 저장 전략만 어떻게 교체했는가"라는 질문으로 읽어야 한다.

## 복원 원칙

- chronology는 Express raw SQL repository를 먼저 만들고, NestJS TypeORM repository로 같은 계약을 다시 묶는 순서로 복원한다.
- 근거는 `database/init.ts`, `book.repository.ts`, `BooksService`, 두 레인의 e2e 테스트와 실제 검증 출력이다.

## 대표 검증

```bash
$ cd express && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
$ cd ../nestjs && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   SQLite schema, raw SQL/ORM repository, API+DB 검증이 어떤 순서로 이어졌는지 따라간다.
