# 08-production-readiness series map

이 프로젝트는 기능을 하나 더 추가하는 단계가 아니다. 서비스 바깥에서 앱을 읽고 운영하는 기준, 즉 runtime config, health/readiness, structured logging 같은 규약을 붙이는 단계다.

처음 읽을 때는 `runtime-config.ts`를 먼저 보는 편이 좋다. 어떤 env를 허용하고, 무엇을 잘못된 설정으로 보고, 그 설정을 어디서 읽는지부터 잡혀야 `/health`와 `/ready`, structured logging이 왜 필요한지도 자연스럽게 이어진다.

## 이 글에서 볼 것

- 운영성 설정을 왜 fail-fast parsing으로 먼저 고정하는지
- `/health`와 `/ready`가 각각 어떤 질문에 답하는지
- request id와 duration을 남기는 structured logging이 왜 최소 단위 observability가 되는지

## source of truth

- `applied/08-production-readiness/README.md`
- `applied/08-production-readiness/problem/README.md`
- `applied/08-production-readiness/nestjs/src/runtime/*`
- `applied/08-production-readiness/nestjs/src/health.controller.ts`
- `applied/08-production-readiness/nestjs/tests/unit/runtime-config.test.ts`
- `applied/08-production-readiness/nestjs/tests/e2e/health.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. runtime config loader와 service로 운영 설정을 먼저 고정한다.
2. `/health`와 `/ready`를 다른 신호로 분리한다.
3. structured logging interceptor로 요청 단위 로그를 남긴다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       3 passed (3)
test:e2e    2 passed (2)
```

## 다음 프로젝트와의 연결

다음 장 `09-platform-capstone`은 지금까지 만든 auth, pipeline, persistence, events, 운영 규약을 하나의 NestJS 서비스 안에서 다시 조립한다.
