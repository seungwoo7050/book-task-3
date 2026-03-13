# 05-auth-and-authorization development timeline

이 프로젝트에 들어오면 파이프라인은 이미 서 있고, 이제 그 위에 누가 들어올 수 있는지와 누가 수정할 수 있는지가 올라온다. 그래서 읽는 순서도 protected route보다 auth service가 먼저다. 어떤 자격을 발급하는지가 먼저 정해져야, 그 자격을 어디서 막을지도 분명해지기 때문이다.

## 흐름 먼저 보기

1. register/login과 JWT 발급을 auth service에 모은다.
2. authentication과 authorization을 다른 request 단계로 나눈다.
3. public route와 protected route를 같은 e2e 흐름으로 묶는다.

## auth service를 먼저 세운 장면

보안 실습이라고 하면 middleware나 guard부터 떠올리기 쉽지만, 실제 출발점은 `AuthService`다.

```ts
const hashedPassword = await bcrypt.hash(dto.password, 10);
const payload: JwtPayload = {
  sub: user.id,
  username: user.username,
  role: user.role,
};
const token = jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
```

이 코드가 중요한 이유는, 이후 모든 protected route가 결국 이 payload를 믿고 움직이기 때문이다. 즉 인증은 route 앞단에서 시작되는 게 아니라, 어떤 claim을 token에 담기로 했는지 정하는 순간부터 시작된다.

NestJS 쪽도 같은 판단을 유지한다.

```ts
const payload = { sub: user.id, username: user.username, role: user.role };
const token = this.jwtService.sign(payload);
```

프레임워크가 달라도 auth service가 하는 일은 거의 같다. 이 공통점이 있어야 뒤에서 request boundary 차이가 더 선명해진다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Tests       9 passed (9)
```

## 401과 403을 갈라 둔 장면

다음 전환점은 token을 검사하는 것과 role을 검사하는 것을 같은 단계로 두지 않기로 한 데서 나온다. Express 쪽에서는 이 차이가 middleware 두 개로 아주 선명하게 보인다.

```ts
if (!authHeader || !authHeader.startsWith("Bearer ")) {
  res.status(401).json({ error: "Authentication required" });
  return;
}
```

여기서의 `401`은 "당신이 누군지 아직 모른다"는 뜻이다. 반면 role 검사는 다른 의미를 가진다.

```ts
if (!allowedRoles.includes(req.user.role)) {
  res.status(403).json({ error: "Insufficient permissions" });
  return;
}
```

이 `403`은 identity는 있지만 permission이 부족하다는 신호다. 둘을 같은 검사로 묶지 않은 덕분에 실패 이유가 훨씬 분명해진다.

NestJS에서도 같은 분리가 guard 쪽으로 옮겨 간다.

```ts
if (!user || !requiredRoles.includes(user.role)) {
  throw new ForbiddenException("Insufficient permissions");
}
```

즉 framework surface는 달라도, authentication과 authorization의 의미 차이는 그대로 유지된다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test
Tests       4 passed (4)
```

## 보호 route와 공개 route를 같이 본 장면

이 프로젝트가 설명으로 끝나지 않는 건 e2e가 public route와 protected route를 한 화면에 놓기 때문이다.

```ts
const res = await request(app)
  .post("/books")
  .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 });

expect(res.status).toBe(401);
```

token이 없으면 `POST /books`는 바로 멈춘다. 반면 regular user가 같은 route를 치면 결과는 달라진다.

```ts
const res = await request(app)
  .post("/books")
  .set("Authorization", `Bearer ${loginRes.body.token}`)
  .send({ title: "Test", author: "A", publishedYear: 2023, genre: "F", price: 10 });

expect(res.status).toBe(403);
```

그리고 `GET /books`는 여전히 공개로 남아 있다. 이 세 경로가 같은 테스트 흐름 안에 있기 때문에, "이 프로젝트가 무엇을 보호하고 무엇은 열어 두는가"가 훨씬 분명하게 남는다.

보안을 무겁게 설명하지 않아도, 여기까지 읽으면 이 프로젝트의 요점은 선명하다. JWT를 붙인 것이 아니라, 누가 들어올 수 있는지와 누가 수정할 수 있는지를 다른 경계로 나눈 것이다. 다음 프로젝트에서는 그 API 계약을 그대로 둔 채 저장 계층만 바뀐다.
