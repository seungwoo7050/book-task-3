# 09-platform-capstone development timeline

이 프로젝트에 들어오면 이전 단계의 규약들이 한꺼번에 모이기 시작한다. 그래서 읽는 감각도 "새 기능이 뭐지?"보다 "기존에 세운 규약들이 서로 충돌하지 않게 어떻게 한 앱에 붙었지?"에 더 가깝다.

## 흐름 먼저 보기

1. auth/books/events/persistence를 한 앱 안에 조합한다.
2. 공통 filter/logging/event listener 규약을 다시 맞춘다.
3. 실제 사용자 흐름을 e2e로 묶어 통합 결과를 확인한다.

## 모듈을 다시 쓰지 않고 합친 장면

capstone이라고 하면 모든 걸 새로 설계해야 할 것처럼 보이지만, 이 프로젝트의 인상적인 부분은 오히려 그 반대다. `AuthService`와 `BooksService`는 이전 단계 책임을 꽤 많이 유지한 채 한 앱으로 들어온다.

```ts
const saved = await this.userRepository.save(user);

this.eventEmitter.emit(
  "user.registered",
  new UserRegisteredEvent(saved.id, saved.username, saved.role),
);
```

auth는 register/login과 event 발행 책임을 그대로 들고 들어온다. books도 마찬가지다.

```ts
const saved = await this.bookRepository.save(book);

this.eventEmitter.emit(
  "book.created",
  new BookCreatedEvent(saved.id, saved.title, saved.author),
);
```

이 두 장면이 중요한 이유는, capstone의 본질이 "더 큰 service 하나를 새로 만든다"가 아니라 "이전 단계에서 검증한 책임을 깨지 않고 한 앱 안에 배치한다"는 데 있기 때문이다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       10 passed (10)
test:e2e    12 passed (12)
```

## cross-cutting contract를 다시 맞춘 장면

모듈을 합친 뒤 더 쉽게 흔들리는 건 feature code보다 공통 규약이다. 그래서 capstone의 두 번째 전환점은 `HttpExceptionFilter`와 `LoggingInterceptor`, `AppEventListener`를 다시 정리하는 데서 나온다.

```ts
response.status(status).json({
  success: false,
  error: { status, message, ...(details ? { details } : {}) },
});
```

이 filter는 개별 모듈이 아무리 잘 돌아가도 응답 표면이 흐려지면 통합 서비스 품질이 떨어진다는 사실을 보여 준다.

```ts
return next.handle().pipe(
  tap(() => {
    const ms = Date.now() - start;
    console.log(`${method} ${url} — ${ms}ms`);
  }),
);
```

logging도 같은 맥락이다. 이제 각 controller가 알아서 로그를 남기는 게 아니라, 앱 전체가 같은 request-level contract를 공유한다.

## 실제 사용자 흐름으로 묶은 장면

마지막 장면은 e2e다. 이 파일이 중요한 이유는 모듈 목록을 다시 설명하지 않고, 실제 사용자 흐름으로 capstone의 통합도를 보여 주기 때문이다.

```ts
const loginRes = await request(app.getHttpServer())
  .post("/auth/login")
  .send({ username: "admin", password: "admin123" });

adminToken = loginRes.body.data.token;
```

이 admin token bootstrap 하나로 이후 모든 protected route 검증이 이어진다.

```ts
const res = await request(app.getHttpServer())
  .post("/books")
  .set("Authorization", `Bearer ${adminToken}`)
  .send(validBook);

expect(res.status).toBe(201);
```

같은 파일 안에는 regular user의 `403`, unauthenticated write의 `401`, public `GET /books`의 `200`, invalid body `400`, missing book `404`까지 함께 들어 있다. 그래서 이 프로젝트는 "기능이 많다"보다 "이전 단계에서 만든 규약들이 한 사용자 흐름 안에서도 동시에 살아 있다"는 쪽으로 읽히게 된다.

다음 프로젝트에서는 이 capstone이 다시 한 번 포장된다. 기능을 더 크게 바꾸기보다, Postgres, Redis, Swagger, Docker Compose를 붙여 실제 제출용 서비스 표면으로 변형하는 단계다.
