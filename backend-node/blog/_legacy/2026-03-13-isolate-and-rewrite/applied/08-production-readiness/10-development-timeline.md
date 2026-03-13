# 08-production-readiness development timeline

applied 단계에 들어오면 갑자기 Docker, CI, cache 같은 단어가 등장한다. 그런데 코드를 실제로 읽어 보면 출발점은 훨씬 더 작다. 이 프로젝트가 먼저 고정한 건 runtime config, health/readiness, structured logging이라는 최소 운영 surface다. 기능을 더 붙이기 전에 "서비스가 어떻게 살아 있고 준비됐다고 말할 것인가"를 정리한다.

## 구현 순서 요약

- 환경 변수를 runtime config 타입으로 고정한다.
- health/readiness endpoint와 structured logging interceptor를 붙인다.
- env patch를 바꿔 e2e로 운영 표면이 실제로 드러나는지 확인한다.

## Phase 1

- 당시 목표: 운영 관련 env를 코드가 설명할 수 있게 만든다.
- 변경 단위: `nestjs/src/runtime/runtime-config.ts`, `nestjs/src/runtime/runtime-config.service.ts`
- 처음 가설: 운영성은 도커나 배포 스크립트보다 먼저, 애플리케이션이 어떤 env를 필요로 하는지 명확히 말할 수 있어야 시작된다.
- 실제 진행: `PORT`, `READY`, `LOG_LEVEL`, `APP_NAME`을 파싱하는 `loadRuntimeConfig()`를 만들고, 주입 가능한 `RuntimeConfigService`를 뒀다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
✓ tests/unit/runtime-config.test.ts (3 tests)
Tests 3 passed (3)
```

검증 신호:

- 잘못된 `PORT`, `READY`, `LOG_LEVEL`은 로딩 단계에서 즉시 실패한다.
- 정상 env는 `appName`, `environment`, `port`를 안정적으로 만든다.

핵심 코드:

```ts
return {
  appName,
  environment: env.NODE_ENV?.trim() || "development",
  port: parsePort(env.PORT),
  ready: parseReady(env.READY),
  logLevel: parseLogLevel(env.LOG_LEVEL),
};
```

왜 이 코드가 중요했는가:

운영성 프로젝트의 실질적인 시작점이 여기 있다. health와 logging이 모두 이 config에 기대기 때문에, env parsing이 흐리면 이후 surface도 함께 흐려진다.

새로 배운 것:

- 운영성은 나중에 붙는 옵션이 아니라 애플리케이션이 어떤 입력에 의존하는지 명시하는 설계 작업이다.

## Phase 2

- 당시 목표: 서비스가 "살아 있음"과 "준비됨"을 다르게 말할 수 있게 한다.
- 변경 단위: `nestjs/src/health.controller.ts`, `nestjs/src/runtime/structured-logging.interceptor.ts`
- 처음 가설: liveness와 readiness는 같은 200 endpoint가 아니라 다른 운영 질문에 답해야 한다.
- 실제 진행: `/health`는 현재 앱 이름과 환경을 돌려주고, `/ready`는 `READY=false`면 `ServiceUnavailableException`을 던진다. 동시에 interceptor는 request id, status, duration을 JSON log로 남긴다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ tests/e2e/health.e2e.test.ts (2 tests)
Tests 2 passed (2)
```

검증 신호:

- `READY=true`일 때 `/health`는 200과 `status: "ok"`를 반환한다.
- `READY=false`일 때 `/ready`는 503과 `status: "not-ready"`를 반환한다.

핵심 코드:

```ts
if (!config.ready) {
  throw new ServiceUnavailableException({
    status: "not-ready",
    appName: config.appName,
    reason: "Set READY=true after dependencies are available.",
  });
}
```

왜 이 코드가 중요했는가:

운영성의 핵심은 잘 돌아갈 때만 보여 주는 화면이 아니라, 아직 준비되지 않았을 때 어떤 신호를 낼지 미리 정하는 일이다. readiness가 200과 다른 응답이어야 하는 이유가 여기서 선명해진다.

새로 배운 것:

- "살아 있음"과 "준비됨"은 같은 말이 아니다. 프로세스는 살아 있어도 의존성이 안 붙었으면 준비되지 않은 상태일 수 있다.

## Phase 3

- 당시 목표: health/readiness/logging surface가 테스트와 stdout에서 실제로 보이는지 검증한다.
- 변경 단위: `nestjs/tests/e2e/health.e2e.test.ts`
- 처음 가설: 운영성 코드는 브라우저보다 테스트와 로그가 더 좋은 증거를 남긴다.
- 실제 진행: env patch를 바꿔 두 앱을 만들고, 하나는 200 health, 다른 하나는 503 readiness failure를 검증했다. 동시에 `process.stdout.write`를 spy해 structured logging이 실제로 발생했는지도 확인했다.

CLI:

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
✓ tests/e2e/health.e2e.test.ts (2 tests)
```

검증 신호:

- body에 `appName: "backend-study-app"`, `environment: "test"`가 그대로 남는다.
- readiness failure 시에도 stdout logging이 호출된다.

핵심 코드:

```ts
expect(stdoutSpy).toHaveBeenCalled();
```

왜 이 코드가 중요했는가:

운영성 기능이 실제로 존재한다는 증거는 "endpoint가 있다"가 아니라 "문제가 생긴 요청도 로그로 남는다"는 데 있다. 이 한 줄이 그걸 보여 준다.

새로 배운 것:

- 운영 surface는 기능 개발을 마친 뒤 덧붙이는 장식이 아니라, 문제를 관측할 수 있게 만드는 기본 안전장치다.

다음:

- [`../09-platform-capstone/00-series-map.md`](../09-platform-capstone/00-series-map.md)에서 03~08의 규약을 단일 NestJS 서비스로 합친다.
