# 09-platform-capstone evidence ledger

이 경로의 git history는 여전히 `2026-03-12` 이관 커밋 한 번만 보여 준다. 그래서 chronology는 commit log 대신 실제 소스, 테스트, 수동 HTTP 재실행을 기준으로 다시 세웠다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 이전 장의 조각을 단일 NestJS 앱으로 묶는다 | `nestjs/src/app.module.ts`, `nestjs/src/main.ts` | capstone이면 기능이 크게 늘어났을 것 같았다 | TypeORM SQLite, EventEmitter, Auth, Books, Events를 한 앱에 올리고 전역 `ValidationPipe`, `HttpExceptionFilter`, `LoggingInterceptor`, `TransformInterceptor`를 설치했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build` | build 통과 | `TypeOrmModule.forRoot(...)`, `app.useGlobalInterceptors(...)` | 이 프로젝트의 첫 과제는 기능 확장이 아니라 통합 껍질 복구다 | 개별 feature 책임이 통합 뒤에도 유지되는지 봐야 한다 |
| 2 | Phase 2 | auth가 실제로 어떤 계약을 돌려주는지 확인한다 | `nestjs/src/auth/auth.service.ts`, `auth.controller.ts`, `auth/strategies/jwt.strategy.ts`, `auth/guards/roles.guard.ts` | JWT capstone이면 더 복잡한 권한 모델이 있을 것 같았다 | `register -> hash -> save -> user.registered`, `login -> compare -> sign`, `token + user` 반환, `ADMIN`만 write 가능한 단순 RBAC를 확인했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` | unit 10개 통과 | `return { token, user: ... }`, `requiredRoles.includes(user.role)` | access token rotation 같은 확장보다 단순 역할 분리가 현재 scope다 | books write 경계와 DTO validation을 닫아야 한다 |
| 3 | Phase 3 | public read와 admin write 경계를 실제 HTTP 표면으로 확인한다 | `nestjs/src/books/books.controller.ts`, `books.service.ts`, `common/filters/http-exception.filter.ts`, `common/interceptors/transform.interceptor.ts` | e2e만 통과하면 응답 형식도 충분히 설명될 것 같았다 | 수동 `curl`로 `GET /books` 성공 envelope, unauthenticated `POST /books`의 `401`, regular user `403`, invalid body `400`, missing book `404`를 다시 확인했다 | `curl -s http://localhost:3123/books`; `curl -s -X POST ... /books`; `curl -s -X GET ... /books/nonexistent` | `{"success":true,"data":[]}`, `{"success":false,"error":{"status":401,"message":"Unauthorized"}}`, `{"success":false,"error":{"status":403,"message":"Insufficient permissions"}}` | `response.status(status).json({ success: false, error: ... })` | capstone의 실제 품질은 기능 수보다 response contract 재현 여부에서 더 잘 보인다 | 이벤트와 로그가 같은 통합도에 올라왔는지 봐야 한다 |
| 4 | Phase 4 | 이벤트와 로그가 통합 단계에서 어떻게 남는지 확인한다 | `nestjs/src/events/app-event.listener.ts`, `nestjs/src/events/events.ts`, `common/interceptors/logging.interceptor.ts`, `test/e2e/capstone.e2e.test.ts` | 이벤트와 request 로그도 e2e가 같이 고정할 것 같았다 | e2e stdout과 수동 서버 실행을 비교해 `user.registered`, `book.created/updated/deleted` 로그는 남지만 request log는 성공 요청 위주로만 찍히고, e2e는 `LoggingInterceptor`를 재설치하지 않는다는 점을 기록했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`; `DB_PATH=:memory: JWT_SECRET=capstone-secret PORT=3123 node dist/main.js` | e2e 12개 통과, stdout에 event log 출력, 수동 요청에서는 `POST /auth/login — 71ms` 같은 성공 로그만 확인 | `tap(() => console.log(...))` | 이벤트 seam은 살아 있지만 운영 로그 계약은 아직 느슨하다 | 다음 장에서 shippable surface로 올라갈 때 이 약점이 더 중요해진다 |

## 근거 파일

- `applied/09-platform-capstone/README.md`
- `applied/09-platform-capstone/problem/README.md`
- `applied/09-platform-capstone/nestjs/README.md`
- `backend-node/docs/native-sqlite-recovery.md`
- `applied/09-platform-capstone/nestjs/src/app.module.ts`
- `applied/09-platform-capstone/nestjs/src/main.ts`
- `applied/09-platform-capstone/nestjs/src/auth/auth.controller.ts`
- `applied/09-platform-capstone/nestjs/src/auth/auth.service.ts`
- `applied/09-platform-capstone/nestjs/src/auth/guards/jwt-auth.guard.ts`
- `applied/09-platform-capstone/nestjs/src/auth/guards/roles.guard.ts`
- `applied/09-platform-capstone/nestjs/src/auth/strategies/jwt.strategy.ts`
- `applied/09-platform-capstone/nestjs/src/books/books.controller.ts`
- `applied/09-platform-capstone/nestjs/src/books/books.service.ts`
- `applied/09-platform-capstone/nestjs/src/common/filters/http-exception.filter.ts`
- `applied/09-platform-capstone/nestjs/src/common/interceptors/logging.interceptor.ts`
- `applied/09-platform-capstone/nestjs/src/common/interceptors/transform.interceptor.ts`
- `applied/09-platform-capstone/nestjs/src/events/app-event.listener.ts`
- `applied/09-platform-capstone/nestjs/src/events/events.ts`
- `applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`
- `applied/09-platform-capstone/nestjs/test/unit/books.service.test.ts`
- `applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`

## 후속 품질 메모

- `nestjs/README.md`는 `pnpm approve-builds && pnpm rebuild better-sqlite3`를 canonical install에 포함한다. 즉 native SQLite bootstrap은 여전히 이 capstone의 실제 전제다.
- 반대로 e2e는 `DB_PATH=:memory:`를 먼저 강제하므로, 문제 정의에 있는 native SQLite recovery 절차 자체를 자동으로 잠그지는 않는다.
- 또 e2e는 `beforeAll` single-app/shared-DB 흐름이어서, 각 테스트를 완전히 분리된 상태에서 다시 부팅하며 검증하는 구조는 아니다.
- 그래서 이 문서에서는 "통합 capstone 검증 완료"와 "file-backed native SQLite recovery 검증 완료"를 같은 말처럼 쓰지 않았다.
