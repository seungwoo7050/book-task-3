# 06-persistence-and-repositories evidence ledger

이 lab의 path history도 `2026-03-12` 이관 커밋 한 번으로 압축돼 있어, chronology는 DB bootstrap, repository/service, 테스트, native dependency 복구 문서를 기준으로 다시 복원했다. 기존 blog 본문은 사실 근거로 사용하지 않았다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | Express에서 raw SQL repository 경계를 세운다 | `express/src/database/init.ts`, `express/src/main.ts`, `express/src/repositories/book.repository.ts`, `express/src/services/book.service.ts` | DB를 붙이면 controller/service까지 꽤 크게 바뀔 것 같았다 | DB bootstrap, PRAGMA, schema init, raw SQL, row mapping을 repository 안쪽으로 밀어 넣고 service는 여전히 `Book` 중심 계약만 보게 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`express/`) | unit 7개 + e2e 6개 통과 | `const DB_PATH = process.env.DB_PATH || "bookstore.db"`, `return row ? this.toBook(row) : null` | Express는 기본 실행이 파일 DB이고, repository mapping 덕분에 SQL column naming이 상위 계층으로 새지 않는다 | 같은 교체를 Nest ORM으로 본다 |
| 2 | Phase 2 | NestJS에서 ORM 기반 persistence로 같은 CRUD를 유지한다 | `nestjs/src/app.module.ts`, `nestjs/src/books/books.module.ts`, `nestjs/src/books/books.service.ts`, `nestjs/src/books/entities/book.entity.ts` | ORM을 붙이면 raw SQL이 사라지는 대신 서비스 언어도 달라질 것 같았다 | `TypeOrmModule.forRoot`와 `@InjectRepository(Book)`로 persistence를 프레임워크에 위임하고, service는 `find/create/update/remove` 언어를 유지했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` (`nestjs/`) | unit 5개 + e2e 6개 통과 | `database: process.env.DB_PATH || ":memory:"`, `this.bookRepository.save(book)` | NestJS는 기본 실행이 `:memory:`라서, "기본 persistence behavior"는 Express와 다르다 | 테스트 격리와 native dependency 범위를 분리해 본다 |
| 3 | Phase 3 | persistence 교체 이후에도 바깥 계약이 유지되는지 확인한다 | `express/test/unit/book.repository.test.ts`, `express/test/e2e/database.e2e.test.ts`, `nestjs/test/unit/books.service.test.ts`, `nestjs/test/e2e/database.e2e.test.ts` | CRUD가 통과하면 저장 전략 차이는 이미 충분히 설명된 것 같았다 | Express는 DB row 직접 조회와 repository unit test로 내부 mapping까지 확인했고, NestJS는 unit + e2e로 service/HTTP 계약을 고정했다 | 위 명령 재실행 | Express 13개, Nest 11개 테스트 통과 | Express e2e의 직접 `SELECT`, Nest e2e의 재조회 흐름 | "저장 계층만 바뀌었다"는 말이 맞으려면 내부 mapping 증거와 바깥 HTTP 계약 증거가 함께 있어야 한다 | native sqlite 준비 상태를 본다 |
| 4 | Phase 4 | native `better-sqlite3` 준비와 검증 범위를 정리한다 | `docs/native-sqlite-recovery.md`, 각 레인 `README.md`, Express/Nest test bootstrap 코드 | recovery 문서는 현재 실패가 날 때만 필요한 보조 자료라고 생각하기 쉽다 | 현재 환경에선 복구 없이도 build/test/e2e가 모두 통과했지만, `pnpm install -> approve-builds -> rebuild better-sqlite3` 순서를 공식 recovery path로 함께 남겼다 | 위 build/test/e2e 재실행 + recovery 문서 점검 | binding 오류 없이 양쪽 명령 모두 통과 | recovery 문서의 고정 순서와 테스트가 모두 `:memory:`를 쓰는 점 | native dependency는 현재 blocker는 아니지만, 이 lab의 재현 가능성을 설명하는 중요한 근거다 | `07-domain-events`에서 저장 성공 뒤 event를 흘린다 |

## 근거 파일

- `core/06-persistence-and-repositories/problem/README.md`
- `core/06-persistence-and-repositories/README.md`
- `docs/native-sqlite-recovery.md`
- `core/06-persistence-and-repositories/express/src/database/init.ts`
- `core/06-persistence-and-repositories/express/src/main.ts`
- `core/06-persistence-and-repositories/express/src/repositories/book.repository.ts`
- `core/06-persistence-and-repositories/express/src/services/book.service.ts`
- `core/06-persistence-and-repositories/express/src/routes/book.router.ts`
- `core/06-persistence-and-repositories/express/test/unit/book.repository.test.ts`
- `core/06-persistence-and-repositories/express/test/e2e/database.e2e.test.ts`
- `core/06-persistence-and-repositories/nestjs/src/app.module.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/books.module.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/books.service.ts`
- `core/06-persistence-and-repositories/nestjs/src/books/entities/book.entity.ts`
- `core/06-persistence-and-repositories/nestjs/src/main.ts`
- `core/06-persistence-and-repositories/nestjs/test/unit/books.service.test.ts`
- `core/06-persistence-and-repositories/nestjs/test/e2e/database.e2e.test.ts`
