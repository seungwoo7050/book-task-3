# 09-platform-capstone evidence ledger

이 프로젝트의 git path history도 `2026-03-12` 한 번의 이관 커밋으로만 보인다. chronology는 auth/books services, 공통 filter/interceptor, event listener, unit/e2e tests, 재검증 CLI를 기준으로 다시 세운 것이다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 03~08의 규약을 한 앱 안에 조합한다 | `nestjs/src/auth/auth.service.ts`, `books/books.service.ts` | capstone이면 완전히 새 설계를 해야 할 것 같았다 | auth, books, events, TypeORM, JWT를 각 모듈 책임을 유지한 채 한 앱에 묶었다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` | `Tests 10 passed`, `test:e2e 12 passed` | `this.eventEmitter.emit("user.registered", ...)` | capstone의 핵심은 새 기능보다 기존 invariant를 깨지 않고 조합하는 데 있다 | cross-cutting contract도 다시 맞춰야 한다 |
| 2 | Phase 2 | 공통 응답/로그/event 규약을 통합 앱에 다시 세운다 | `common/filters/http-exception.filter.ts`, `logging.interceptor.ts`, `events/app-event.listener.ts` | 기능만 합치면 capstone도 저절로 정리될 것 같았다 | validation failure, 404, logging, event consumption을 공통 계층으로 다시 정리했다 | 같은 명령 재실행 | duplicate username, invalid credentials, 403, 400, 404가 모두 표준 envelope로 돌아온다 | `response.status(status).json({ success: false, error: ... })` | 통합 단계에서 가장 쉽게 흔들리는 건 feature보다 cross-cutting contract다 | 실제 사용자 흐름을 e2e로 묶어야 한다 |
| 3 | Phase 3 | 실제 관리자/일반 사용자 흐름을 한 e2e로 검증한다 | `nestjs/test/e2e/capstone.e2e.test.ts` | unit test가 충분하면 통합도 자연스럽게 설명될 것 같았다 | in-memory SQLite 위에서 register/login/admin CRUD/public read/regular user forbidden/invalid body/missing book을 한 흐름으로 묶었다 | 위 명령 재실행 | e2e 12개 전부 통과 | admin token을 만든 뒤 protected route를 검증하는 시나리오 | 통합 서비스는 모듈 목록보다 사용자 흐름이 이전 규약을 동시에 만족하는지에서 더 잘 드러난다 | 다음 프로젝트에서 이 capstone을 제출용 서비스 표면으로 다시 패키징한다 |

## 근거 파일

- `applied/09-platform-capstone/README.md`
- `applied/09-platform-capstone/problem/README.md`
- `applied/09-platform-capstone/nestjs/src/auth/auth.service.ts`
- `applied/09-platform-capstone/nestjs/src/books/books.service.ts`
- `applied/09-platform-capstone/nestjs/src/common/filters/http-exception.filter.ts`
- `applied/09-platform-capstone/nestjs/src/common/interceptors/logging.interceptor.ts`
- `applied/09-platform-capstone/nestjs/src/events/app-event.listener.ts`
- `applied/09-platform-capstone/nestjs/test/unit/auth.service.test.ts`
- `applied/09-platform-capstone/nestjs/test/e2e/capstone.e2e.test.ts`
