# 08-production-readiness evidence ledger

이 프로젝트의 path 단위 `git log`도 `2026-03-12`의 이관 커밋 하나로만 보인다. chronology는 runtime config, health/readiness, structured logging, 테스트, 재검증 CLI를 기준으로 복원했다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 운영성 설정을 env와 fail-fast parsing으로 먼저 고정한다 | `nestjs/src/runtime/runtime-config.ts`, `runtime-config.service.ts` | health endpoint만 있으면 운영성 예제로는 충분할 것 같았다 | `APP_NAME`, `PORT`, `READY`, `LOG_LEVEL`를 파싱 함수로 검증하고 service로 주입했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e` | `Tests 3 passed`, `test:e2e 2 passed` | `loadRuntimeConfig` | 운영성의 시작점은 endpoint가 아니라 앱이 어떤 설정으로 떠야 하는지를 명시하는 데 있다 | live와 ready를 나눠야 한다 |
| 2 | Phase 2 | `/health`와 `/ready`를 다른 신호로 분리한다 | `nestjs/src/health.controller.ts` | health endpoint 하나면 상태 확인은 충분해 보였다 | `/health`는 liveness, `/ready`는 `READY=false`일 때 `503`을 돌려주는 readiness check로 나눴다 | 같은 명령 재실행 | `/health` 200, `/ready` 503 경계가 e2e에서 확인된다 | `if (!config.ready) { throw new ServiceUnavailableException(...) }` | 프로세스가 살아 있는 것과 트래픽을 받아도 되는 건 다른 질문이다 | 요청 단위 observability도 함께 붙여야 한다 |
| 3 | Phase 3 | structured logging을 운영 규약 안에 넣는다 | `nestjs/src/runtime/structured-logging.interceptor.ts`, e2e tests | console log 몇 줄이면 충분해 보였다 | request id, method, path, statusCode, duration, outcome을 JSON 한 줄로 남기고 e2e에서 stdout 호출까지 확인했다 | 위 명령 재실행 | readiness 실패 경로에서도 stdout write가 남는다 | `process.stdout.write(JSON.stringify(payload))` | 운영성은 별도 시스템보다 요청 하나를 어떤 shape의 로그로 남기는지에서 먼저 시작된다 | 다음 프로젝트에서 이 규약을 capstone 전체에 붙인다 |

## 근거 파일

- `applied/08-production-readiness/README.md`
- `applied/08-production-readiness/problem/README.md`
- `applied/08-production-readiness/nestjs/src/runtime/runtime-config.ts`
- `applied/08-production-readiness/nestjs/src/runtime/runtime-config.service.ts`
- `applied/08-production-readiness/nestjs/src/health.controller.ts`
- `applied/08-production-readiness/nestjs/src/runtime/structured-logging.interceptor.ts`
- `applied/08-production-readiness/nestjs/tests/unit/runtime-config.test.ts`
- `applied/08-production-readiness/nestjs/tests/e2e/health.e2e.test.ts`
