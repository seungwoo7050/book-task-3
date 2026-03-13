# 04-request-pipeline development timeline

이 프로젝트에 들어오면 CRUD 자체는 더 이상 새롭지 않다. 대신 어떤 값이 handler까지 들어와야 하는지, 성공과 실패가 어떤 모양으로 나가야 하는지, 그 규약을 누가 책임질지 같은 질문이 앞에 나온다. 그래서 이 글도 기능 설명보다 pipeline ordering을 따라가는 편이 더 자연스럽다.

## 흐름 먼저 보기

1. validation을 handler 밖으로 뺀다.
2. success/error envelope를 공통 표면으로 만든다.
3. 같은 규약을 NestJS global pipeline으로 다시 세운다.

## 검증을 handler 밖으로 뺀 장면

Express 쪽에서 가장 먼저 눈에 들어오는 건 `validate` middleware다. 이 함수가 등장하는 순간 controller는 더 이상 "이 body가 맞는가"부터 시작하지 않는다.

```ts
export function validate(schema: ZodSchema) {
  return (req, _res, next): void => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (err) {
      if (err instanceof ZodError) {
        const details = err.errors.map((e) => ({
          field: e.path.join("."),
          message: e.message,
        }));
        next(new ValidationError("검증 실패", details));
        return;
      }
      next(err);
    }
  };
}
```

이 장면이 중요한 이유는, validation이 controller의 조건문 묶음이 아니라 pipeline의 한 단계로 고정됐기 때문이다. 그 순간부터 handler는 "이미 검증된 값이 들어온다"는 가정을 가질 수 있고, 그 가정이 이후 코드 전체를 단순하게 만든다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       16 passed (16)
test:e2e    9 passed (9)
```

이 검증 결과가 보여 주는 것도 같다. validation failure, partial update, full CRUD가 모두 같은 pipeline 위에서 돌아간다.

## 응답 표면을 고정한 장면

validation만 밖으로 빼면 절반이다. 다음 전환점은 성공과 실패가 어떤 shape로 나갈지를 한 번에 고정한 부분에서 나온다.

```ts
res.json = function (body?: unknown): Response {
  if (body && typeof body === "object" && "success" in (body as Record<string, unknown>)) {
    return originalJson(body);
  }
  return originalJson({ success: true, data: body });
};
```

이 래퍼가 생기면 route handler는 body만 반환해도 되고, 바깥에서 성공 응답을 `{ success: true, data }`로 감싼다. 즉 controller는 값에 집중하고, pipeline은 표면에 집중한다.

실패도 같은 원리로 모인다.

```ts
if (err instanceof ValidationError) {
  res.status(err.statusCode).json({
    success: false,
    error: {
      message: err.message,
      statusCode: err.statusCode,
      details: err.details,
    },
  });
  return;
}
```

이 error handler가 중요한 이유는, validation failure, application error, malformed JSON이 모두 같은 envelope 안에 들어오면서도 status code와 details는 분리해서 남길 수 있기 때문이다. 지금부터 클라이언트는 응답을 받을 때마다 다른 JSON shape를 대비할 필요가 줄어든다.

## NestJS global pipeline으로 옮긴 장면

NestJS로 넘어오면 이 규약은 middleware가 아니라 global pipe/filter/interceptor 조합으로 다시 나타난다.

```ts
response.status(status).json({
  success: false,
  error: errorBody,
});
```

`HttpExceptionFilter`는 Nest 기본 예외 응답을 그대로 쓰지 않고, 프로젝트가 원하는 error envelope로 다시 감싼다. 즉 프레임워크 기본값을 받아들이는 대신, 공통 계약을 한 번 더 명시하는 셈이다.

성공 경로는 interceptor가 맡는다.

```ts
return next.handle().pipe(
  map((data) => ({
    success: true as const,
    data,
  })),
);
```

이제 controller는 CRUD 값을 그냥 반환해도 된다. response shaping은 pipeline이 하고, validation도 global pipe가 맡는다. Express와 역할 배치는 다르지만 결과 표면은 거의 비슷해진다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       7 passed (7)
test:e2e    8 passed (8)
```

여기까지 읽으면 이 프로젝트의 핵심은 기능 추가가 아니라 바닥 규약 세우기였다는 점이 분명해진다. 다음 프로젝트 `05-auth-and-authorization`은 바로 이 규약 위에 JWT와 RBAC를 얹는다.
