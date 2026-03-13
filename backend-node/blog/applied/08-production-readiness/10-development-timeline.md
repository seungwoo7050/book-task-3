# 08-production-readiness development timeline

이 프로젝트에 오면 더 이상 Books CRUD를 넓히는 게 중심이 아니다. 대신 "이 앱이 어떤 설정으로 뜨고, 언제 살아 있다고 말할 수 있고, 요청 하나를 어떤 로그로 남길 것인가" 같은 질문이 앞에 나온다. 그래서 읽는 순서도 business logic보다 runtime config와 health 쪽이 더 자연스럽다.

## 흐름 먼저 보기

1. env parsing과 `RuntimeConfigService`로 운영 설정을 고정한다.
2. `/health`와 `/ready`를 다른 신호로 나눈다.
3. structured logging interceptor로 요청 단위 관찰 가능성을 붙인다.

## 설정을 먼저 고정한 장면

운영성이라고 하면 health endpoint부터 떠올리기 쉽지만, 이 프로젝트의 첫 장면은 `loadRuntimeConfig`다.

```ts
function parsePort(value: string | undefined): number {
  const rawPort = value ?? "3000";
  const port = Number(rawPort);

  if (!Number.isInteger(port) || port <= 0) {
    throw new Error(`PORT must be a positive integer. Received: ${rawPort}`);
  }
  return port;
}
```

이 작은 parsing 함수가 중요한 이유는, 앱이 뜨기도 전에 잘못된 설정을 거부해야 그 뒤의 `/health`나 `/ready`도 의미가 생기기 때문이다.

`loadRuntimeConfig`는 이런 판단을 한곳에 모은다.

```ts
return {
  appName,
  environment: env.NODE_ENV?.trim() || "development",
  port: parsePort(env.PORT),
  ready: parseReady(env.READY),
  logLevel: parseLogLevel(env.LOG_LEVEL),
};
```

이 지점에서 운영성은 endpoint 개수가 아니라, 어떤 설정을 허용하고 어떤 설정을 즉시 실패로 볼지 결정하는 일로 바뀐다.

## live와 ready를 나눈 장면

설정이 정리되고 나면 그다음 질문은 "이 프로세스가 살아 있는가"와 "이 프로세스가 트래픽을 받아도 되는가"를 어떻게 다르게 표현할지다.

```ts
@Get("ready")
getReady() {
  const config = this.runtimeConfig.snapshot;

  if (!config.ready) {
    throw new ServiceUnavailableException({
      status: "not-ready",
      appName: config.appName,
      reason: "Set READY=true after dependencies are available.",
    });
  }

  return {
    status: "ready",
    appName: config.appName,
    environment: config.environment,
  };
}
```

이 분기가 중요한 이유는, 프로세스가 살아 있는 것과 준비가 끝난 것이 같은 말이 아니라는 점을 코드로 보여 주기 때문이다. 나중에 DB나 Redis 같은 의존성이 붙는 서비스로 가면 이 차이는 더 중요해진다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       3 passed (3)
test:e2e    2 passed (2)
```

e2e에서도 같은 차이가 잡힌다. `/health`는 200이고, `READY=false`일 때 `/ready`는 503으로 떨어진다.

## structured logging을 붙인 장면

마지막 장면은 structured logging이다. health와 readiness만으로는 앱이 살아 있는지 알 수 있어도, 요청 하나가 어떻게 지나갔는지는 잘 보이지 않는다.

```ts
const payload = {
  level: config.logLevel,
  appName: config.appName,
  environment: config.environment,
  requestId,
  method: request.method,
  path: request.originalUrl ?? request.url ?? "/",
  statusCode: response.statusCode,
  durationMs: Date.now() - startedAt,
  outcome,
};

process.stdout.write(`${JSON.stringify(payload)}\n`);
```

이 로그 포맷이 중요한 이유는, 사람이 콘솔에서 한 번 보는 메시지보다 다른 시스템이 그대로 ingest할 수 있는 shape를 먼저 택했기 때문이다. request id를 헤더와 로그에 같이 남기는 것도 같은 맥락이다.

즉 이 프로젝트는 운영성 항목을 조금씩 붙인 예제가 아니라, "앱이 어떤 설정으로 뜨고 어떤 상태를 내보내며 요청 하나를 어떤 이벤트로 남기는가"를 묶어 보는 첫 실험이었다. 다음 프로젝트에서는 이 규약이 auth, books, events, persistence가 한곳에 모인 capstone 전체로 옮겨 간다.
