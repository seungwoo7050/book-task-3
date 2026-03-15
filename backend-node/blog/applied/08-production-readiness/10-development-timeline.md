# 08-production-readiness development timeline

`07-domain-events`까지는 기능 경계와 side effect 경계를 세우는 일이 중심이었다면, 이 lab은 그 위에 운영자가 실제로 기대하는 최소 규약을 얹는 단계다. 이번 재검토에서는 README의 체크리스트를 그대로 반복하지 않고, 코드로 구현된 것과 문서로만 남아 있는 것을 분리해서 chronology를 다시 세웠다.

## 흐름 먼저 보기

1. runtime config를 fail-fast loader로 먼저 고정한다.
2. `/health`와 `/ready`로 live/readiness를 나누고, interceptor로 structured log를 남긴다.
3. Dockerfile과 CI workflow를 코드 바깥의 실행 경로로 확인하되, cache/queue/rate limiting은 아직 docs-only라는 점을 분리한다.

## 운영성 설정을 먼저 고정한 장면

이 lab에서 가장 먼저 읽어야 할 파일은 `runtime-config.ts`다. health endpoint보다도 먼저, 앱이 어떤 환경변수를 허용하고 어떤 설정을 즉시 실패시킬지부터 결정한다.

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

`READY`와 `LOG_LEVEL`도 같은 방식으로 좁은 입력 계약을 갖는다.

```ts
function parseReady(value: string | undefined): boolean {
  const rawReady = value ?? "true";
  if (rawReady === "true") return true;
  if (rawReady === "false") return false;
  throw new Error(`READY must be either true or false. Received: ${rawReady}`);
}
```

```ts
function parseLogLevel(value: string | undefined): LogLevel {
  const rawLogLevel = value ?? "info";
  if (!ALLOWED_LOG_LEVELS.has(rawLogLevel as LogLevel)) {
    throw new Error(`LOG_LEVEL must be one of debug, info, warn, error. Received: ${rawLogLevel}`);
  }
  return rawLogLevel as LogLevel;
}
```

이 덕분에 `AppModule`은 단순히 provider wiring만 맡는다.

```ts
{
  provide: RUNTIME_CONFIG,
  useFactory: () => loadRuntimeConfig(process.env),
}
```

운영성의 출발점이 endpoint 수가 아니라 "앱이 어떤 설정이면 아예 시작하지 않아야 하는가"라는 데 있다는 점이 이 장면에서 가장 분명해진다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/unit/runtime-config.test.ts (3 tests)
```

unit test는 기본값, 명시적 파싱, invalid port fail-fast까지 고정한다. 다만 현재는 invalid `READY`, invalid `LOG_LEVEL`, 빈 `APP_NAME` trimming 같은 branch까지는 테스트가 직접 덮지 않는다.

## live/readiness와 structured logging을 붙인 장면

그 다음 장면은 health controller다. 이 lab은 `health/live`와 `health/ready`라는 경로 대신 `/health`와 `/ready`를 쓴다. 이름은 조금 다르지만 의미 분리는 분명하다.

```ts
@Get("health")
getHealth() {
  return {
    status: "ok",
    appName: config.appName,
    environment: config.environment,
    timestamp: new Date().toISOString(),
  };
}
```

```ts
@Get("ready")
getReady() {
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

이 흐름 덕분에 liveness와 readiness가 명확히 갈린다. 실제 재실행에서도 그 차이는 그대로 나타났다.

```bash
$ APP_NAME=backend-study-app READY=false LOG_LEVEL=warn NODE_ENV=staging PORT=3111 node dist/main.js
$ curl -i http://localhost:3111/health
200 OK

$ curl -i http://localhost:3111/ready
503 Service Unavailable
{"status":"not-ready","appName":"backend-study-app","reason":"Set READY=true after dependencies are available."}
```

structured logging은 APP interceptor로 전역에 붙는다.

```ts
{
  provide: APP_INTERCEPTOR,
  inject: [RuntimeConfigService],
  useFactory: (runtimeConfig: RuntimeConfigService) => {
    return new StructuredLoggingInterceptor(runtimeConfig);
  },
}
```

interceptor는 요청마다 request id를 계산하고 헤더에 다시 써 준다.

```ts
const requestId = Array.isArray(requestIdHeader)
  ? requestIdHeader[0] ?? "unknown-request-id"
  : requestIdHeader ?? "generated-request-id";

response.setHeader("x-request-id", requestId);
```

이 구성은 "항상 request id가 있다"는 점에선 단순하지만 실용적이다. 다만 여기서 자동 생성되는 값은 UUID 같은 고유 식별자가 아니라 literal `"generated-request-id"`다. 그래서 호출자가 헤더를 보내지 않으면, 로그 간 correlation은 "없다"기보다 "placeholder 수준으로만 있다"고 보는 편이 정확하다.

그리고 로그는 사람이 읽기 좋은 문자열보다 JSON payload를 우선한다.

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

## 실제 재실행에서 드러난 한계

이번 턴에서 가장 중요한 발견은 readiness 실패 로그의 status code였다. `/ready`는 응답으로는 분명히 `503`을 돌려주지만, interceptor가 error path에서 로그를 남길 때는 아직 response status가 갱신되기 전이라 다음처럼 찍힌다.

```text
{"level":"warn","appName":"backend-study-app","environment":"staging","requestId":"generated-request-id","method":"GET","path":"/ready","statusCode":200,"durationMs":1,"outcome":"error"}
```

즉 현재 구현은 `outcome:"error"`로 실패를 남기긴 하지만, `statusCode` 필드는 운영자 관점에서 정확하지 않다. e2e가 `stdoutSpy` 호출 여부만 확인하고 payload shape나 `x-request-id` echo의 실제 값까지는 검증하지 않기 때문에, 이 차이는 테스트에서는 드러나지 않는다.

또 하나는 범위 차이다. 문제 설명과 README는 cache, queue, rate limiting까지 production-readiness 항목으로 언급하지만, 실제 코드에는 그에 해당하는 구현 파일이 없다. 해당 주제는 [`production-readiness-checklist.md`](/Users/woopinbell/work/book-task-3/backend-node/study/Node-Backend-Architecture/applied/08-production-readiness/docs/concepts/production-readiness-checklist.md) 에서 "여기서는 전체 구현까지 밀어붙이지 않는다"는 문장으로만 다뤄진다. 그러니 이 lab의 실구현 범위는 config, health/readiness, structured logging, Docker, CI까지라고 보는 편이 정확하다.

## Docker와 CI가 실물로 남는 장면

이 lab이 applied 단계인 이유는 문서 바깥 실물이 있기 때문이다. Dockerfile은 build stage와 runtime stage를 분리한 2-stage 구성을 갖고,

```dockerfile
FROM node:22-alpine AS build
...
RUN pnpm run build

FROM node:22-alpine
...
CMD ["node", "dist/main.js"]
```

GitHub Actions workflow도 로컬 README와 같은 순서로 `install -> build -> test -> test:e2e`를 돈다.

```yaml
- run: pnpm install
- run: pnpm run build
- run: pnpm run test
- run: pnpm run test:e2e
```

즉 이 lab은 운영성 항목을 추상적으로 설명하는 데서 멈추지 않고, 적어도 "어떤 빌드 경로를 반복해야 verified라고 말할 수 있는가"를 파일로 남겨 둔다.

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       5 passed (5)
```

## 여기서 남는 것

이 문서를 다시 쓰고 나니 이 lab의 요점이 더 분명해졌다. production readiness는 모든 운영성 기능을 구현하는 단계가 아니라, capstone이 기대할 수 있는 최소 운영 규약을 먼저 고정하는 단계다. 설정은 fail-fast로 읽고, `/health`와 `/ready`는 다르게 말하고, 요청은 JSON 로그로 남기고, 빌드 검증 경로는 Docker/CI 파일로 남긴다. 다만 request id와 log payload를 얼마나 강하게 신뢰할 수 있는지는 자동 테스트보다 소스와 수동 재실행이 더 많은 설명을 맡는다. 다음 `09-platform-capstone`은 바로 이 규약들을 실제 도메인 기능과 함께 한 서비스 안에 통합하는 단계다.
