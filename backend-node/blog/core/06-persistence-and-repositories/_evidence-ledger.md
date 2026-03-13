# 06-persistence-and-repositories evidence ledger

이 프로젝트의 git path history도 `2026-03-12` 이관 커밋 한 번으로 압축돼 있다. chronology는 DB 초기화 코드, repository/service, 테스트, 재검증 CLI를 중심으로 다시 세운 것이다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 메모리 저장소를 SQLite repository로 바꾼다 | `express/src/database/init.ts`, `express/src/repositories/book.repository.ts` | DB를 붙이면 service와 controller도 많이 흔들릴 것 같았다 | DB 초기화와 raw SQL을 repository에 가두고 상위 계층 표면은 거의 그대로 뒀다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`express/`) | `Tests 7 passed`, `test:e2e 6 passed` | `db.pragma("journal_mode = WAL")` | persistence 교체의 핵심은 SQL이 아니라 상위 계층 계약을 얼마나 유지하느냐에 있다 | 같은 교체를 Nest ORM으로도 해 본다 |
| 2 | Phase 2 | NestJS에서 ORM 기반 영속 계층을 붙인다 | `nestjs/src/books/books.service.ts` | ORM을 붙이면 service 책임도 꽤 달라질 것 같았다 | `Repository<Book>`를 주입해 CRUD 메서드 모양은 유지하고 저장 방식만 바꿨다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` (`nestjs/`) | `Tests 5 passed`, `test:e2e 6 passed` | `@InjectRepository(Book)` | raw SQL과 ORM의 차이는 controller보다 repository boundary에서 가장 또렷하게 드러난다 | 저장 성공 뒤에만 side effect를 흘리는 구조가 다음 문제다 |
| 3 | Phase 3 | 저장 방식이 바뀌어도 CRUD 계약이 유지되는지 본다 | `express/test/unit/book.repository.test.ts`, `nestjs/test/e2e/database.e2e.test.ts` | DB를 붙이면 404나 validation 같은 API 계약도 조금씩 흔들릴 수 있다고 보기 쉽다 | repository unit test와 e2e를 함께 돌려 persistence 내부와 HTTP 표면을 동시에 확인했다 | 위 명령 재실행 | Express 7/6, Nest 5/6 통과 | create/find/update/delete를 저장 계층 바깥 계약으로 다시 확인하는 테스트 | persistence migration은 API rewrite가 아니라 boundary discipline의 시험에 가깝다 | 다음엔 저장 성공 뒤에만 domain event를 발행한다 |

## 근거 파일

- `core/06-persistence-and-repositories/README.md`
- `core/06-persistence-and-repositories/problem/README.md`
- `core/06-persistence-and-repositories/express/src/database/init.ts`
- `core/06-persistence-and-repositories/express/src/repositories/book.repository.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`
- `core/06-persistence-and-repositories/express/test/unit/book.repository.test.ts`
- `core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`
