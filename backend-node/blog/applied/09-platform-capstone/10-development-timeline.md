# 09-platform-capstone development timeline

이 capstone을 따라가다 보면 "챕터 1부터 8까지 다 들어갔다"는 말보다, 서로 다른 계약을 한 앱에 붙였을 때 어디가 유지되고 어디가 비는지가 더 중요해진다. 실제 소스도 그 방향으로 배치되어 있다. `AppModule`이 모듈을 조합하고, `main.ts`가 전역 HTTP 계약을 다시 설치하고, 그 위에서 auth와 books가 각자 자기 책임을 유지한 채 동작한다.

## 1. 단일 앱 껍질을 먼저 세운다

처음 기준선은 `AppModule`이다. 여기서 TypeORM이 `better-sqlite3`와 `DB_PATH || ":memory:"`를 물고 올라오고, 동시에 `EventEmitterModule.forRoot()`, `AuthModule`, `BooksModule`, `EventsModule`이 같은 Nest 앱에 실린다. capstone의 첫 결정은 기능을 새로 만드는 게 아니라, 이전 장의 조각들을 한 런타임에 같이 태우는 것이다.

`main.ts`도 같은 맥락이다. 이 파일은 controller를 늘리는 대신 앱 전체에 `ValidationPipe`, `HttpExceptionFilter`, `LoggingInterceptor`, `TransformInterceptor`를 깐다. 그래서 이후 개별 route를 볼 때는 "무슨 기능이 있나?"보다 "이 route가 어떤 전역 계약 아래서 실행되나?"를 먼저 묻게 된다.

여기서 하나 더 남길 점이 있다. canonical problem statement는 native SQLite recovery까지 이 capstone의 범위로 언급하지만, 기본 검증 흐름은 그 전체를 한 번에 자동화하지 않는다. `nestjs/README.md`가 `pnpm approve-builds && pnpm rebuild better-sqlite3`를 설치 절차에 따로 적는 이유도, 이 프로젝트가 TS 코드만 통과하면 끝나는 단계가 아니라 native binding bootstrap을 실제 전제로 두기 때문이다.

## 2. auth는 사용자 생성보다 계약 복구에 가깝다

다음으로 눈에 들어오는 건 `AuthService`다. register는 `findOneBy(username)`로 중복을 막고, `bcrypt.hash`로 비밀번호를 해시한 뒤, `save` 성공 후에만 `user.registered` 이벤트를 발행한다. login은 저장된 hash와 `bcrypt.compare`를 거쳐 JWT를 서명한다.

여기서 중요한 포인트는 "JWT가 있다"가 아니라, 반환 shape와 역할 정보가 아주 단순하다는 점이다. login 결과는 `accessToken`이 아니라 `token` 하나와 최소한의 `user` 정보만 돌려준다. `JwtStrategy.validate()`도 `{ sub, username, role }`를 그대로 request user로 넘기고, `RolesGuard`는 이 중 `role`만 읽어 `ADMIN` 여부를 확인한다. 즉, 이 앱의 인가 모델은 세밀한 permission system이 아니라 "공개 read + 관리자 write"로 고정된 단순 RBAC이다.

## 3. books는 CRUD보다 공개 읽기와 관리자 쓰기 경계를 고정한다

`BooksController`를 보면 이 분리가 더 선명해진다. `GET /books`, `GET /books/:id`는 guard가 없고, `POST/PUT/DELETE /books`만 `JwtAuthGuard -> RolesGuard -> @Roles(Role.ADMIN)` 체인을 탄다. write route에는 route-level `ValidationPipe`가 다시 붙어 있어서 DTO 스키마를 벗어난 payload를 막는다.

서비스 레벨에서도 흐름은 간단하다. `create`는 UUID를 만들고 저장한 뒤 `book.created`, `update`는 바뀐 필드 목록을 계산해서 `book.updated`, `remove`는 삭제 성공 뒤 `book.deleted`를 발행한다. 이 프로젝트에서 이벤트는 비동기 인프라를 붙이는 단계가 아니라, "상태 변경이 성공한 뒤에만 부수효과 seam을 남긴다"는 규칙을 capstone 안에 다시 심는 역할을 한다.

## 4. 공통 HTTP 표면은 응답은 잘 맞추지만 로그는 비대칭이다

통합 단계에서 가장 조심해서 봐야 하는 건 cross-cutting contract다. `TransformInterceptor`는 성공 응답을 항상 `{ success: true, data }`로 감싸고, `HttpExceptionFilter`는 실패 응답을 `{ success: false, error: { status, message, details? } }`로 맞춘다. 수동 재실행에서도 이 규약은 그대로 확인됐다.

```bash
$ curl -s http://localhost:3123/books
{"success":true,"data":[]}

$ curl -s -o - -w '\n%{http_code}\n' -X POST http://localhost:3123/books ...
{"success":false,"error":{"status":401,"message":"Unauthorized"}}
401
```

다만 로그는 덜 단단하다. `LoggingInterceptor`는 `tap(() => ...)`만 사용하므로 성공 요청에서는 `POST /auth/login — 71ms` 같은 줄이 남지만, 실제 재실행 기준 `401`, `403`, `400`, `404` 응답은 같은 형식의 request log가 남지 않았다. e2e도 `HttpExceptionFilter`와 `TransformInterceptor`는 다시 설치하지만 `LoggingInterceptor`는 재설치하지 않아서, 이 비대칭은 테스트로 고정돼 있지 않다. 이 프로젝트를 "통합은 됐지만 운영 표면은 아직 거칠다"라고 읽게 만드는 핵심 근거다.

## 5. e2e는 모듈 설명 대신 사용자 시나리오로 마무리한다

마지막 전환점은 `capstone.e2e.test.ts`다. 이 파일은 모듈을 하나씩 설명하지 않고 `admin register -> login -> token bootstrap -> protected write`, 그리고 `regular user -> 403`, `unauthenticated write -> 401`, `invalid body -> 400`, `missing book -> 404`를 한 흐름으로 묶는다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ test/unit/auth.service.test.ts (5 tests)
✓ test/unit/books.service.test.ts (5 tests)
✓ test/e2e/capstone.e2e.test.ts (12 tests)
```

이 결과 덕분에 "auth/books/events를 한 앱에 넣었다"는 사실보다, 이전 장의 계약이 실제 사용자 흐름에서도 충돌 없이 이어진다는 점이 더 설득력 있게 남는다. 동시에 refresh token, ownership, pagination, structured logging verification 같은 운영 레벨 문제는 아직 다음 단계로 남아 있다는 것도 분명해진다.

다만 이 자동 검증이 잠그는 건 HTTP 계약과 in-memory SQLite 경로까지다. 테스트가 `process.env.DB_PATH = ":memory:"`를 먼저 박아 두기 때문에, 문제 정의가 말하는 native SQLite recovery는 README와 recovery guide가 설명하는 별도 운영 절차로 남아 있다. 그리고 이 e2e suite는 `beforeAll`에서 앱을 한 번만 띄워 관리자 등록과 토큰 bootstrap을 해 둔 뒤, 같은 shared DB 위에 케이스들을 순차적으로 쌓는다. 즉 이 capstone의 canonical suite는 통합 계약을 강하게 확인하지만, file-backed DB 손상/복구나 완전한 per-test isolation까지 같이 증명하는 것은 아니다.
