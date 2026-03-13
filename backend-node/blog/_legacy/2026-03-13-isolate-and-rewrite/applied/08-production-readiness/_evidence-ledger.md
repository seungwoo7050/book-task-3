# 08-production-readiness evidence ledger

근거는 [`README.md`](../../../study/Node-Backend-Architecture/applied/08-production-readiness/README.md), [`nestjs/src/runtime/runtime-config.ts`](../../../study/Node-Backend-Architecture/applied/08-production-readiness/nestjs/src/runtime/runtime-config.ts), [`nestjs/src/runtime/runtime-config.service.ts`](../../../study/Node-Backend-Architecture/applied/08-production-readiness/nestjs/src/runtime/runtime-config.service.ts), [`nestjs/src/health.controller.ts`](../../../study/Node-Backend-Architecture/applied/08-production-readiness/nestjs/src/health.controller.ts), [`nestjs/src/runtime/structured-logging.interceptor.ts`](../../../study/Node-Backend-Architecture/applied/08-production-readiness/nestjs/src/runtime/structured-logging.interceptor.ts), [`nestjs/tests/e2e/health.e2e.test.ts`](../../../study/Node-Backend-Architecture/applied/08-production-readiness/nestjs/tests/e2e/health.e2e.test.ts), 실제 검증 출력이다.

## Phase 1

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: 운영성 규약을 환경 변수 기반 runtime config로 먼저 고정한다.
- 변경 단위: `nestjs/src/runtime/runtime-config.ts`, `nestjs/src/runtime/runtime-config.service.ts`
- 처음 가설: health, logging, readiness를 제대로 설명하려면 먼저 `PORT`, `READY`, `LOG_LEVEL` 같은 운영 입력을 코드 모델로 묶어야 한다.
- 실제 조치: `loadRuntimeConfig()`가 env를 파싱하고 `RuntimeConfigService`가 그 snapshot을 주입하도록 만들었다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`
- 검증 신호: unit `Tests 3 passed (3)`
- 핵심 코드 앵커: `loadRuntimeConfig()`, `RuntimeConfigService.snapshot`
- 새로 배운 것: 운영성 프로젝트의 첫 단계는 Dockerfile이 아니라 "무엇을 runtime contract로 볼 것인가"를 타입으로 정의하는 일이었다.
- 다음: health/readiness endpoint와 structured logging을 이 config 위에 얹는다.

## Phase 2

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: liveness, readiness, request logging을 서비스 바깥 표면으로 끌어올린다.
- 변경 단위: `nestjs/src/health.controller.ts`, `nestjs/src/runtime/structured-logging.interceptor.ts`
- 처음 가설: 운영성 예제의 최소 단위는 비즈니스 도메인이 아니라 "서비스가 지금 살아 있는지, 준비됐는지, 어떤 요청이 지나갔는지"다.
- 실제 조치: `/health`, `/ready`를 만들고 `StructuredLoggingInterceptor`가 request id, duration, status code를 JSON으로 남기게 했다.
- CLI: `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e`
- 검증 신호: `✓ tests/e2e/health.e2e.test.ts (2 tests)`, `Tests 2 passed (2)`
- 핵심 코드 앵커: `HealthController.getReady()`, `StructuredLoggingInterceptor.logRequest()`
- 새로 배운 것: readiness는 단순 상태 문자열이 아니라 "의존성이 아직 안 붙었다면 503을 내보낼 수 있어야 한다"는 태도에 더 가깝다.
- 다음: 운영성 표면이 실제 테스트에서 어떻게 읽히는지 정리한다.

## Phase 3

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: health/readiness/logging 규약이 실제로 테스트와 stdout에서 보이는지 확인한다.
- 변경 단위: `nestjs/tests/e2e/health.e2e.test.ts`
- 처음 가설: 운영성 코드는 화면보다 테스트와 로그 출력이 더 좋은 증거다.
- 실제 조치: `READY=true`일 때 `/health`가 200을 반환하고, `READY=false`일 때 `/ready`가 503과 `not-ready` body를 반환하는 시나리오를 만들었다.
- CLI: `pnpm run test:e2e`
- 검증 신호: `status: "ok"`, `appName: "backend-study-app"`, `status: "not-ready"`, `stdoutSpy` called
- 핵심 코드 앵커: `health.e2e.test.ts`
- 새로 배운 것: 운영성 기능은 "문제가 생기면 무엇을 볼 수 있는가"를 미리 제공하는 일이다.
- 다음: `09-platform-capstone`에서 이제까지 만든 규약을 단일 서비스로 통합한다.
