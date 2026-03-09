# 하나로 합치기 — 캡스톤에서 드러나는 아키텍처의 진짜 가치

## 프롤로그: 부품과 기계의 차이

프로젝트 03에서 REST를 만들었다. 04에서 파이프라인을 정비했다. 05에서 인증을 붙였다. 06에서 영속 계층을 교체했다. 07에서 이벤트를 분리했다. 08에서 운영 기반을 깔았다.

각각은 잘 동작했다. 하지만 이 부품들이 하나의 서비스 안에서 함께 동작할 때, 예상치 못한 질문들이 등장한다. 인증 Guard가 Books 모듈에서 어떻게 접근되는가? 이벤트가 Auth와 Books 양쪽에서 발행될 때 리스너는 어떻게 구성하는가? 전역 파이프와 인터셉터가 인증 엔드포인트에도 적용되는가?

캡스톤 프로젝트는 이 질문들에 답하는 과정이다.

---

## 1. 모듈 의존성 그래프

`AppModule`은 다섯 개의 임포트를 가진다:

```typescript
imports: [
  TypeOrmModule.forRoot({ ... entities: [Book, User] ... }),
  EventEmitterModule.forRoot(),
  AuthModule,
  BooksModule,
  EventsModule,
]
```

이 한 줄씩이 프로젝트 03~08의 핵심을 대표한다:

- **TypeORM**: 06-persistence — Book과 User 두 엔티티를 하나의 SQLite에
- **EventEmitter**: 07-domain-events — 도메인 이벤트 인프라
- **AuthModule**: 05-auth — JWT + bcrypt + Passport + RBAC
- **BooksModule**: 03-rest + 04-pipeline — CRUD + 검증 + 에러 처리
- **EventsModule**: 07-domain-events — 이벤트 리스너들

NestJS의 모듈 시스템이 이 통합을 가능하게 한다. 각 모듈은 자기 의존성을 캡슐화하고 있으므로, `AppModule`에서 import만 하면 시작 시 자동으로 조립된다.

---

## 2. Auth + Books의 접점: Guard와 Decorator

개별 프로젝트에서는 Auth 모듈과 Books 모듈이 분리되어 있었다. 캡스톤에서 이 둘이 만나는 지점은 `BooksController`다.

```typescript
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(Role.ADMIN)
@Post()
create(@Body(...) dto: CreateBookDto) { ... }
```

`GET /books`와 `GET /books/:id`는 공개 — Guard가 없다. 누구나 조회 가능.
`POST`, `PUT`, `DELETE`는 `JwtAuthGuard`로 인증을 확인하고, `RolesGuard`로 `ADMIN` 역할을 확인한다.

이 구조는 프로젝트 05에서 만든 Guard를 Books 컨트롤러에 그대로 가져다 쓴 것이다. Auth와 Books의 결합은 데코레이터 수준에서만 발생한다. Service나 Repository는 서로 모른다.

---

## 3. 이벤트의 확장: User + Book

프로젝트 07에서는 Book 이벤트만 있었다. 캡스톤에서는 `UserRegisteredEvent`가 추가된다.

```typescript
export class UserRegisteredEvent {
  constructor(
    public readonly userId: string,
    public readonly username: string,
    public readonly role: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}
```

`AuthService.register()` 끝에 이 이벤트가 발행된다. `AppEventListener`에서는 `@OnEvent("user.registered")`로 이 이벤트를 처리한다.

이전에 `BookEventListener`였던 클래스가 `AppEventListener`로 이름이 바뀌었다. 더 이상 Book 전용이 아니라 애플리케이션 전체의 이벤트를 수신하기 때문이다. 이름 변경은 사소해 보이지만, 책임 범위가 확장되었음을 명시적으로 드러내는 신호다.

---

## 4. 두 엔티티, 하나의 데이터베이스

```typescript
TypeOrmModule.forRoot({
  type: "better-sqlite3",
  database: process.env.DB_PATH || ":memory:",
  entities: [Book, User],
  synchronize: true,
})
```

`entities` 배열에 `Book`과 `User` 두 엔티티가 등록된다. TypeORM이 시작 시 `books`와 `users` 테이블을 자동 생성한다.

`User` 엔티티에는 `@Column({ unique: true })` 제약이 있다. 같은 username으로 두 번 등록하면 409 Conflict. 이 유니크 제약은 데이터베이스 수준에서 보장되므로 애플리케이션 레벨의 체크와 이중으로 보호된다.

`User.password`는 bcrypt 해시로 저장된다. 원문 비밀번호는 어디에도 보존되지 않는다. `AuthService.register()`에서 `bcrypt.hash(dto.password, 10)`을 호출하고, `login()`에서 `bcrypt.compare(password, user.password)`로 검증한다.

---

## 5. E2E 테스트: 전체 흐름의 증명

캡스톤 E2E 테스트(`capstone.e2e.test.ts`)는 이 프로젝트의 하이라이트다. 개별 기능을 확인하는 것을 넘어, 기능 간의 교차 동작을 검증한다.

### 테스트 시나리오의 흐름

1. **ADMIN 계정 생성**: `beforeAll`에서 admin 유저 등록 + 로그인 → JWT 토큰 획득
2. **인증 테스트**: 회원가입, 중복 거부, 로그인, 잘못된 비밀번호
3. **공개 API 검증**: `GET /books`는 토큰 없이도 200
4. **보호 API 검증**: `POST /books`는 토큰 없으면 401
5. **RBAC 검증**: ADMIN은 생성/수정/삭제 가능, USER는 403
6. **검증 파이프라인**: 잘못된 body는 400
7. **Not Found**: 존재하지 않는 책은 404

```typescript
it("POST /books — regular user should be forbidden", async () => {
  // 일반 유저 등록 → 로그인 → 토큰으로 책 생성 시도
  expect(res.status).toBe(403);
});
```

이 테스트가 성공한다는 것은 Auth Guard, Roles Guard, BookService, TypeORM, ValidationPipe가 모두 올바르게 연동된다는 증거다.

### `beforeAll` vs `beforeEach`

이전 프로젝트들은 `beforeEach`로 매 테스트마다 DB를 초기화했다. 캡스톤은 `beforeAll`을 사용한다. 한 번 앱을 띄우고 모든 테스트가 같은 데이터를 공유한다.

이 선택은 의도적이다. 실제 서비스에서는 데이터가 테스트 간에 누적된다. 이 E2E 테스트는 "독립적인 단위"가 아니라 "통합 시나리오"를 검증하므로, 데이터 누적이 오히려 현실적이다.

---

## 6. 캡스톤이 가르치는 것

### 모듈 경계의 비용

Auth와 Books가 만나는 지점(`@UseGuards`)은 의외로 단순하다. 이전 프로젝트들에서 모듈 경계를 명확히 했기 때문이다. Guard는 Auth에서 export하고, Controller에서 import한다. 양 모듈의 Service는 서로 의존하지 않는다.

만약 `BooksService`가 `AuthService`에 직접 의존했다면? 순환 의존이 발생하거나, 모듈 간 결합이 강해져서 독립 테스트가 어려워졌을 것이다.

### 이벤트 통합의 용이성

새로운 이벤트(`UserRegisteredEvent`)를 추가하는 과정은 놀라울 정도로 단순하다. 이벤트 클래스 정의, Service에서 emit, Listener에서 `@OnEvent` 핸들러 추가. 기존 코드를 수정하지 않는다.

이것이 프로젝트 07에서 만든 이벤트 아키텍처가 지닌 확장성이다.

---

## 에필로그: 다음은 현실 세계의 인프라

이 캡스톤은 아직 SQLite 기반이다. 단일 프로세스, 단일 파일. 프로젝트 10에서는 이 모든 것이 Postgres + Redis + Docker Compose 위로 올라간다. 마이그레이션 스크립트가 `synchronize: true`를 대체하고, 로그인 쓰로틀링이 Redis에 기반하며, Swagger가 API 문서를 자동 생성한다.

캡스톤에서 한 것은 설계의 통합이었다. 다음 프로젝트에서 할 것은 인프라의 통합이다.
