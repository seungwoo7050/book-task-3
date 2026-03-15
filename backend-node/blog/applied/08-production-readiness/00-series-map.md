# 08-production-readiness series map

이 lab은 feature를 하나 더 붙이는 단계가 아니다. 애플리케이션 바깥에서 운영자가 가장 먼저 묻게 되는 질문, 즉 "어떤 설정으로 뜨는가", "살아 있는가", "준비됐는가", "요청 하나를 어떤 로그로 남기는가"를 최소 구현으로 고정하는 단계다.

이번에 소스를 다시 따라가며 보니 중요한 사실이 세 가지 있었다. 첫째, 문제 설명이 언급하는 cache, queue, rate limiting은 실제 코드가 아니라 개념 문서에서만 다뤄진다. 둘째, structured logging interceptor는 `x-request-id` 헤더를 응답에 돌려주고 JSON 로그도 남기지만, `/ready` 실패 경로에서는 실제 응답이 `503`이어도 로그 `statusCode`는 `200`으로 찍힌다. 셋째, request id를 직접 보내지 않으면 runtime이 UUID를 생성하는 것이 아니라 문자열 `"generated-request-id"`를 placeholder처럼 넣는다.

## 이 글에서 볼 것

- `loadRuntimeConfig`가 잘못된 env를 앱 시작 전에 실패시키는 방식
- `/health`와 `/ready`가 각각 live/readiness를 어떻게 분리하는지
- structured logging, Dockerfile, GitHub Actions가 어느 수준까지는 실제 구현이고, cache/queue/rate limiting은 아직 docs-only인지

## source of truth

- `applied/08-production-readiness/problem/README.md`
- `applied/08-production-readiness/README.md`
- `applied/08-production-readiness/nestjs/src/app.module.ts`
- `applied/08-production-readiness/nestjs/src/main.ts`
- `applied/08-production-readiness/nestjs/src/health.controller.ts`
- `applied/08-production-readiness/nestjs/src/runtime/runtime-config.ts`
- `applied/08-production-readiness/nestjs/src/runtime/runtime-config.service.ts`
- `applied/08-production-readiness/nestjs/src/runtime/structured-logging.interceptor.ts`
- `applied/08-production-readiness/nestjs/tests/unit/runtime-config.test.ts`
- `applied/08-production-readiness/nestjs/tests/e2e/health.e2e.test.ts`
- `applied/08-production-readiness/nestjs/Dockerfile`
- `applied/08-production-readiness/nestjs/ci/github-actions.yml`
- `applied/08-production-readiness/docs/concepts/production-readiness-checklist.md`

## 구현 흐름 한눈에 보기

1. runtime config loader로 `APP_NAME`, `PORT`, `READY`, `LOG_LEVEL`, `NODE_ENV`를 먼저 고정한다.
2. `/health`와 `/ready`를 분리해 프로세스 생존과 준비 상태를 다르게 표현한다.
3. APP interceptor로 structured log를 남기고, Dockerfile과 CI workflow로 빌드 경로를 문서 바깥 실물로 남긴다.
4. 다만 cache, queue, rate limiting은 구현이 아니라 개념 문서 수준이고, readiness 실패 로그의 status code는 현재 응답 코드와 어긋난다.
5. 자동 검증은 stdout write 발생과 endpoint 응답까지만 본다. `x-request-id` echo의 실제 값, placeholder request id의 한계, 로그 payload shape 전체는 소스와 수동 재실행을 함께 읽어야 한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       5 passed (5)
```

```bash
$ APP_NAME=backend-study-app READY=false LOG_LEVEL=warn NODE_ENV=staging PORT=3111 node dist/main.js
$ curl -i http://localhost:3111/health
200 OK
```

```bash
$ curl -i http://localhost:3111/ready
503 Service Unavailable
{"status":"not-ready","appName":"backend-study-app","reason":"Set READY=true after dependencies are available."}
```

```text
{"level":"warn","appName":"backend-study-app","environment":"staging","requestId":"generated-request-id","method":"GET","path":"/ready","statusCode":200,"durationMs":1,"outcome":"error"}
```

마지막 로그 한 줄은 현재 구현의 중요한 한계를 보여 준다. readiness 실패는 `outcome:"error"`로 남지만, interceptor 시점 때문에 `statusCode`는 아직 `503`이 아니라 `200`으로 찍힌다. 게다가 request id를 보내지 않았을 때 들어가는 값도 고유 추적 ID가 아니라 `"generated-request-id"`라는 고정 placeholder라서, 분산 correlation을 강하게 말하려면 호출자가 실제 header를 전달한다는 전제가 필요하다.

## 다음 프로젝트와의 연결

다음 `09-platform-capstone`은 03~08에서 만든 규약을 단일 NestJS 서비스로 통합하는 단계다. 그래서 이 lab은 production-hardening 완성본이라기보다, capstone이 기대할 수 있는 최소 운영 규약의 뼈대를 먼저 만드는 단계로 보는 편이 맞다.
