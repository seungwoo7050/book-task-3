# 07-domain-events series map

`07-domain-events`는 persistence까지 들어간 서비스에서 side effect를 처음으로 본문 밖으로 밀어내는 단계다. 그래서 이 시리즈는 "어떤 연산 뒤에 이벤트를 발행하고, 어떤 실패에서는 절대 발행하지 않는가"라는 질문으로 읽는다.

## 복원 원칙

- chronology는 Express `EventBus`로 시작해 NestJS listener registration으로 옮겨 가는 순서로 복원한다.
- 근거는 `event-bus.ts`, `book-event.listener.ts`, 각종 unit/e2e 테스트, 실제 이벤트 로그 출력이다.

## 대표 검증

```bash
$ cd express && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
$ cd ../nestjs && COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test && COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
```

## 글 순서

1. [10-development-timeline.md](10-development-timeline.md)
   event boundary, listener registration, 성공/실패 발행 조건이 어떤 순서로 고정됐는지 따라간다.
