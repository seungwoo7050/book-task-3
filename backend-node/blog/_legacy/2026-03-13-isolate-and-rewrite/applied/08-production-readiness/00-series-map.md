# 08-production-readiness series map

`08-production-readiness`는 backend-node가 applied 단계로 넘어가는 첫 프로젝트다. 여기서는 Books 도메인을 더 키우지 않고, 서비스 바깥에서 제일 먼저 보이는 운영 표면을 정리한다. 그래서 이 시리즈는 "runtime config, health/readiness, structured logging을 어떤 순서로 붙였는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 runtime config를 먼저 세우고, health/readiness와 logging을 그 위에 얹는 순서로 복원한다.
- 근거는 `runtime-config.ts`, `health.controller.ts`, `structured-logging.interceptor.ts`, `health.e2e.test.ts`, 실제 검증 출력이다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   runtime config, health/readiness, structured logging이 applied 단계의 첫 surface로 어떻게 고정됐는지 따라간다.
