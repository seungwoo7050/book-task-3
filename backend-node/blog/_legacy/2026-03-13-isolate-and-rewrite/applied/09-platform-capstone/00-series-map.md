# 09-platform-capstone series map

`09-platform-capstone`은 backend-node의 core 규약들을 처음으로 한 NestJS 서비스 안에 모아 보는 통합판이다. 그래서 이 시리즈는 "무엇을 새로 추가했는가"보다 "이전 단계에서 배운 규약들이 한 프로세스 안에서도 일관적인가"라는 질문으로 읽는 편이 맞다.

## 복원 원칙

- chronology는 `AppModule` 통합부터 시작해 auth/books/events service 연결, e2e 재검증 순서로 복원한다.
- 근거는 `app.module.ts`, `books.service.ts`, `auth.service.ts`, `app-event.listener.ts`, `capstone.e2e.test.ts`, 실제 검증 출력이다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   module 통합, service/event 경계, capstone e2e가 어떤 순서로 맞물리는지 따라간다.
