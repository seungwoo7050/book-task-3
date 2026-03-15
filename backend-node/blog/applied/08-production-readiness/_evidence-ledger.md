# 08-production-readiness evidence ledger

이 lab의 path history도 `2026-03-12` 신규 설계 커밋으로 압축돼 있어, chronology는 runtime config, health/readiness, structured logging, Docker/CI, 실제 재실행 CLI를 기준으로 다시 복원했다. 기존 blog 본문은 사실 근거로 사용하지 않았다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 앱이 어떤 설정으로 떠야 하는지 먼저 고정한다 | `nestjs/src/runtime/runtime-config.ts`, `runtime-config.service.ts`, `runtime.constants.ts`, `app.module.ts` | health endpoint만 있어도 운영성 예제는 충분할 것 같았다 | `APP_NAME`, `PORT`, `READY`, `LOG_LEVEL`, `NODE_ENV`를 fail-fast parsing으로 읽고 provider로 주입하게 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`, `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e` | unit 3개, e2e 2개 통과 | `useFactory: () => loadRuntimeConfig(process.env)` | 운영성의 시작점은 endpoint가 아니라 "잘못된 설정이면 앱이 어떻게 실패해야 하는가"다 | live/readiness와 로그를 붙인다 |
| 2 | Phase 2 | `/health`와 `/ready`를 다른 신호로 분리하고 structured log를 남긴다 | `nestjs/src/health.controller.ts`, `runtime/structured-logging.interceptor.ts`, `main.ts` | readiness도 health의 일부로 뭉뚱그려도 충분할 것 같았다 | `/health`는 200 liveness, `/ready`는 `READY=false`일 때 503으로 나누고, interceptor로 `x-request-id` header와 JSON log payload를 남기게 했다 | `APP_NAME=backend-study-app READY=false LOG_LEVEL=warn NODE_ENV=staging PORT=3111 node dist/main.js`, `curl -i /health`, `curl -i /ready` | `/health` 200, `/ready` 503, 응답에 `x-request-id` header 포함 | `response.setHeader("x-request-id", requestId)` | 이 lab은 live/readiness를 경로로 분리할 뿐 아니라, request id를 응답과 로그 양쪽에 남기는 최소 관찰성도 함께 만든다. 다만 header가 없을 때는 UUID가 아니라 `"generated-request-id"` placeholder를 쓴다 | 로그 payload 정확도를 점검한다 |
| 3 | Phase 3 | 실제 로그가 운영자 기대와 얼마나 맞는지 확인한다 | `nestjs/src/runtime/structured-logging.interceptor.ts`, `tests/e2e/health.e2e.test.ts` | error path도 로그에 같은 status code가 남을 것이라 기대하기 쉽다 | `/ready` 실패를 수동 재실행해 응답은 503인데 log payload의 `statusCode`는 200으로 남는 현재 동작을 확인했다 | 위 수동 재실행 + 서버 stdout 확인 | `outcome:"error"`이지만 `statusCode:200`으로 기록 | `tap({ error: () => this.logRequest(...) })` | interceptor 시점 때문에 error path 로그와 실제 응답 코드가 어긋날 수 있고, 현재 e2e는 `stdoutSpy` 호출 여부만 검증한다. 즉 payload shape와 request id 값의 품질은 자동 테스트가 직접 잠그지 않는다 | 구현 범위와 docs-only 범위를 분리한다 |
| 4 | Phase 4 | 실제 구현 범위와 문서-only 범위를 구분한다 | `docs/concepts/production-readiness-checklist.md`, `nestjs/Dockerfile`, `nestjs/ci/github-actions.yml` | problem statement가 언급한 cache/queue/rate limiting도 코드에 어느 정도 있을 것 같았다 | 실제 구현은 config, health/readiness, logging, Docker, CI에 머물고, cache/queue/rate limiting은 개념 문서에만 남아 있음을 확인했다 | 위 build/test/e2e 재실행 + 문서/CI/Docker 점검 | 로컬 검증 5개 테스트 통과, Docker/CI 파일 존재 | checklist의 "여기서는 전체 구현까지 밀어붙이지 않는다" 문장 | production-readiness라는 이름이 곧 모든 운영 기능 구현을 뜻하지는 않는다 | `09-platform-capstone`에서 규약을 실제 기능과 통합한다 |

## 근거 파일

- `applied/08-production-readiness/problem/README.md`
- `applied/08-production-readiness/README.md`
- `applied/08-production-readiness/nestjs/src/app.module.ts`
- `applied/08-production-readiness/nestjs/src/main.ts`
- `applied/08-production-readiness/nestjs/src/health.controller.ts`
- `applied/08-production-readiness/nestjs/src/runtime/runtime-config.ts`
- `applied/08-production-readiness/nestjs/src/runtime/runtime-config.service.ts`
- `applied/08-production-readiness/nestjs/src/runtime/runtime.constants.ts`
- `applied/08-production-readiness/nestjs/src/runtime/structured-logging.interceptor.ts`
- `applied/08-production-readiness/nestjs/tests/unit/runtime-config.test.ts`
- `applied/08-production-readiness/nestjs/tests/e2e/health.e2e.test.ts`
- `applied/08-production-readiness/nestjs/Dockerfile`
- `applied/08-production-readiness/nestjs/ci/github-actions.yml`
- `applied/08-production-readiness/docs/concepts/production-readiness-checklist.md`
- `applied/08-production-readiness/docs/references/checked-sources.md`
