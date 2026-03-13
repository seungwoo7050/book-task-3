# 04-request-pipeline series map

`04-request-pipeline`은 Books CRUD를 더 키우는 프로젝트가 아니라, 이후 모든 API가 공유할 request/response 규약을 먼저 고정하는 단계다. 그래서 이 시리즈는 "validation, error envelope, logging, response wrapping이 어떤 순서로 붙었는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 Express middleware chain을 먼저 만들고, NestJS global pipeline으로 같은 규약을 재구성하는 순서로 복원한다.
- 근거는 `express/src/middleware/*`, `nestjs/src/common/*`, `nestjs/src/main.ts`, 두 레인의 e2e 출력이다.

## 대표 검증

```bash
$ cd express && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
$ cd ../nestjs && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   middleware/pipe/filter/interceptor가 어떤 순서로 공통 규약을 만들었는지 따라간다.
