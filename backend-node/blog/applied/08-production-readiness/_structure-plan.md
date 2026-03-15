# 08-production-readiness structure plan

이 문서는 운영성 체크리스트 나열보다 "실제로 구현된 운영 규약이 무엇이고, 무엇은 아직 문서에만 남아 있는가"가 먼저 읽혀야 한다. 서사의 중심은 `runtime config -> health/readiness -> structured logging -> Docker/CI -> docs-only 범위`다.

## 읽기 구조

1. 왜 `loadRuntimeConfig`가 health endpoint보다 먼저 읽혀야 하는지부터 잡는다.
2. `/health`와 `/ready`를 live/readiness 질문으로 분리해 설명한다.
3. `StructuredLoggingInterceptor`의 `x-request-id` header와 JSON payload를 잇는다.
4. 수동 재실행에서 `/ready` 실패 로그가 `statusCode:200`으로 남는 현재 한계를 분리해서 적는다.
5. 마지막에는 Docker/CI는 실구현이고 cache/queue/rate limiting은 docs-only라는 범위 차이를 남긴다.

## 반드시 남길 근거

- `nestjs/src/runtime/runtime-config.ts`
- `nestjs/src/runtime/runtime-config.service.ts`
- `nestjs/src/health.controller.ts`
- `nestjs/src/runtime/structured-logging.interceptor.ts`
- `nestjs/tests/unit/runtime-config.test.ts`
- `nestjs/tests/e2e/health.e2e.test.ts`
- 수동 `/health` `/ready` 재실행 결과
- `nestjs/Dockerfile`
- `nestjs/ci/github-actions.yml`
- `docs/concepts/production-readiness-checklist.md`

## 리라이트 톤

- 운영성 일반론보다 현재 소스가 실제로 구현한 경계를 중심으로 쓴다.
- 성공한 부분과 아직 docs-only인 부분을 섞지 않는다.
- 로그 payload 한계처럼 수동 재실행에서 드러난 차이를 숨기지 않는다.
