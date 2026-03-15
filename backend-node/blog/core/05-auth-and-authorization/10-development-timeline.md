# 05-auth-and-authorization development timeline

`04-request-pipeline`이 요청의 공통 규약을 세우는 단계였다면, 이 lab은 그 규약 위에 누가 들어올 수 있고 누가 쓰기 작업을 할 수 있는지를 올리는 단계다. 다만 이번에 실제 소스를 다시 읽어 보니, 이 lab은 이전 pipeline을 깔끔하게 확장했다기보다 인증과 권한 경계에 집중하면서 response envelope와 validation 일관성은 잠시 내려놓은 형태에 더 가깝다. 그래서 문서도 "JWT를 붙였다"보다 "어느 지점에서 어떤 이유로 요청을 끊는가"를 중심으로 다시 썼다.

## 흐름 먼저 보기

1. Express/NestJS 모두 auth service에서 해시와 JWT claim을 먼저 고정한다.
2. 요청 경계에서는 인증과 권한 검사를 다른 단계로 나눠 `401`과 `403`을 분리한다.
3. 실제 응답 body와 빈 credential 재실행을 통해, role 경계는 있지만 validation/pipeline 일관성은 아직 느슨하다는 점을 확인한다.

## auth service에서 claim을 먼저 고정한 장면

보안 lab이라고 하면 middleware나 guard를 먼저 떠올리기 쉽지만, 실질적인 시작점은 둘 다 auth service다. Express `AuthService`는 사용자 등록 때 비밀번호를 해시하고, 로그인 성공 시 JWT payload를 만든다.

```ts
const hashedPassword = await bcrypt.hash(dto.password, 10);
...
const payload: JwtPayload = {
  sub: user.id,
  username: user.username,
  role: user.role,
};
const token = jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
```

NestJS도 거의 같은 역할 분담을 유지한다.

```ts
const payload = { sub: user.id, username: user.username, role: user.role };
const token = this.jwtService.sign(payload);
```

이 단계가 중요한 이유는 protected route들이 결국 이 claim을 믿고 동작하기 때문이다. 인증은 `Authorization` 헤더를 읽는 순간 시작되는 게 아니라, 어떤 최소 정보를 토큰에 담아 다음 단계로 넘길지 결정하는 순간부터 시작된다.

또 하나 눈에 띄는 점은 secret 관리 방식이다. Express는 `process.env.JWT_SECRET || "super-secret"`로 환경변수 override를 허용하지만, NestJS `AuthModule`과 `JwtStrategy`는 둘 다 `"super-secret"`을 하드코딩한다. 학습용 샘플이라는 맥락은 이해되지만, 현재 문서에는 이 차이도 드러내는 편이 맞다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       9 passed (9)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
Test Files  1 passed (1)
Tests       4 passed (4)
```

테스트는 둘 다 통과하지만, 여기서 고정되는 것은 registration/login happy path와 권한 경계이지 입력 validation까지는 아니다.

## Express에서 `401 -> 403`을 middleware 두 단계로 나눈 장면

Express 쪽의 핵심은 `book.router.ts` 한 줄에 거의 다 드러난다.

```ts
router.post("/", authmiddleware, requireRole("ADMIN"), asyncHandler(controller.create));
```

`authmiddleware`는 먼저 토큰의 존재와 서명을 검사한다.

```ts
if (!authHeader || !authHeader.startsWith("Bearer ")) {
  res.status(401).json({ error: "Authentication required" });
  return;
}
...
const decoded = jwt.verify(token, JWT_SECRET) as JwtPayload;
req.user = decoded;
```

그 다음 `requireRole("ADMIN")`가 `req.user.role`을 확인한다.

```ts
if (!allowedRoles.includes(req.user.role)) {
  res.status(403).json({ error: "Insufficient permissions" });
  return;
}
```

그래서 Express lane에서는 "누군지 모름"과 "누군지는 알지만 권한이 부족함"이 아주 노골적으로 다른 middleware에 배치된다. 이 구성 덕분에 `401`과 `403`의 의미 차이가 코드 표면에 그대로 남는다.

직접 응답 body를 확인해 보니 그 차이는 더 분명했다.

```bash
$ node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); ... "
{"unauth":{"status":401,"body":{"error":"Authentication required"}},"forbidden":{"status":403,"body":{"error":"Insufficient permissions"}}}
```

다만 이 결과는 동시에 한 가지 한계도 보여 준다. 이전 `04-request-pipeline`에서 만들었던 `{ success, error }` envelope는 여기서 재사용되지 않는다. 즉 auth 경계는 분명하지만, 응답 표면 일관성은 한 단계 뒤로 물러나 있다.

## NestJS에서 같은 경계를 strategy와 guard chain으로 옮긴 장면

NestJS에서는 이 흐름이 Passport strategy와 guard 조합으로 옮겨 간다. `JwtStrategy`가 bearer token을 해석해 `req.user`에 넣고,

```ts
super({
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  ignoreExpiration: false,
  secretOrKey: "super-secret",
});

validate(payload: { sub: string; username: string; role: string }) {
  return { sub: payload.sub, username: payload.username, role: payload.role };
}
```

`BooksController`는 `JwtAuthGuard`와 `RolesGuard`를 순서대로 건다.

```ts
@Post()
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles("ADMIN")
create(@Body() dto: { ... }) {
  return this.booksService.create(dto);
}
```

`RolesGuard`는 metadata에서 required role을 읽고, 맞지 않으면 `ForbiddenException`을 던진다.

```ts
if (!user || !requiredRoles.includes(user.role)) {
  throw new ForbiddenException("Insufficient permissions");
}
```

응답 body도 직접 확인해 보니 Express와는 표면이 다르다.

```bash
$ node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/books') ..."
{"unauth":{"status":401,"body":{"message":"Unauthorized","statusCode":401}},"forbidden":{"status":403,"body":{"message":"Insufficient permissions","error":"Forbidden","statusCode":403}}}
```

즉 NestJS는 기본 exception response shape를 그대로 사용하고 있고, Express는 수동 `{ error }` 객체를 쓴다. 둘 다 상태코드 경계는 맞지만, 이전 pipeline lab에서 기대했던 공통 envelope는 여기서 유지되지 않는다.

## role 경계와 validation 공백을 함께 본 장면

이번 lab에서 가장 품질 차이를 크게 만든 건 "역할 경계가 있다"와 "입력 검증도 갖췄다"를 분리해서 보는 일이었다. e2e 테스트는 duplicate username, invalid credentials, unauthenticated write, non-admin write, public read를 고정한다. 하지만 auth DTO 쪽 validation은 거의 비어 있다.

Express는 register body를 바로 받아서 해시하고 저장하고,

```ts
const { username, password, role } = req.body;
const user = await this.authService.register({ username, password, role });
```

NestJS도 `RegisterDto`, `LoginDto`를 쓰지만 decorator 기반 validator도 없고 `main.ts`에 `ValidationPipe`도 없다.

```ts
export class RegisterDto {
  username!: string;
  password!: string;
  role?: "USER" | "ADMIN";
}
```

실제로 빈 문자열 credential을 넣어 보니 두 레인 모두 등록에 성공했다.

```bash
$ node -e "const request=require('supertest'); const { createApp } = require('./dist/app.js'); request(createApp()).post('/auth/register').send({ username:'', password:'' }) ..."
201 { id: '...', username: '', role: 'USER' }
```

```bash
$ node -e "require('reflect-metadata'); ... request(app.getHttpServer()).post('/auth/register').send({ username:'', password:'' }) ..."
201 { id: '...', username: '', role: 'USER' }
```

그래서 이 lab의 현재 상태를 가장 정확하게 요약하면 이렇다. JWT 발급과 admin-only write 경계는 분명하게 세워졌지만, credential validation과 response envelope 일관성은 아직 다음 정리 대상이다.

## 여기서 남는 것

문서를 다시 쓰고 나니 다음 `06-persistence-and-repositories`와의 연결도 더 현실적으로 보였다. 다음 단계는 auth 체계를 완성하는 단계가 아니라, 지금 세워 둔 공개/보호 route 계약을 유지한 채 저장 계층을 교체하는 단계다. 다시 말해 이 lab은 보안 시스템의 완결판이 아니라, 이후 영속 계층과 도메인 계층이 기대할 수 있는 최소한의 인증/인가 경계를 먼저 고정한 실험이다.
