# 07-domain-events series map

이 lab은 persistence 위에 side effect를 올리는 첫 단계다. 하지만 소스를 다시 따라가 보니 핵심은 "이벤트를 도입했다"는 말보다 훨씬 좁고 구체적이다. 저장이 실제로 성공한 뒤에만 어떤 사실을 바깥으로 흘리고, 실패했을 때는 그 사실을 절대 흘리지 않는 경계를 만드는 일이다.

읽을 때는 Express `EventBus`와 `BookService`를 먼저 보는 편이 좋다. EventEmitter 기반 수동 wiring에서 emit 시점이 어떻게 보이는지 먼저 잡아야, NestJS의 `EventEmitterModule`, `@OnEvent`, `EventEmitter2`가 같은 문제를 프레임워크 안으로 어떻게 감싸는지 비교가 선명해진다.

## 이 글에서 볼 것

- service가 side effect를 직접 실행하지 않고 `book.*` 사실만 발행하도록 바뀌는 장면
- create/update/delete 성공 뒤에만 emit가 일어나고, 실패 경로에서는 이벤트가 발행되지 않는 현재 계약
- Express는 `removeAllListeners()`와 수동 `on/off`로, NestJS는 module wiring과 `eventEmitter.on/off`로 테스트 간 listener 누수를 어떻게 제어하는지

## source of truth

- `core/07-domain-events/problem/README.md`
- `core/07-domain-events/README.md`
- `docs/native-sqlite-recovery.md`
- `core/07-domain-events/express/src/events/event-bus.ts`
- `core/07-domain-events/express/src/events/book-event-listener.ts`
- `core/07-domain-events/express/src/services/book.service.ts`
- `core/07-domain-events/express/src/app.ts`
- `core/07-domain-events/express/test/unit/event-bus.test.ts`
- `core/07-domain-events/express/test/e2e/events.e2e.test.ts`
- `core/07-domain-events/nestjs/src/app.module.ts`
- `core/07-domain-events/nestjs/src/events/events.module.ts`
- `core/07-domain-events/nestjs/src/events/book-event.listener.ts`
- `core/07-domain-events/nestjs/src/events/events.ts`
- `core/07-domain-events/nestjs/src/books/books.service.ts`
- `core/07-domain-events/nestjs/test/unit/book-event.listener.test.ts`
- `core/07-domain-events/nestjs/test/unit/books.service.test.ts`
- `core/07-domain-events/nestjs/test/e2e/events.e2e.test.ts`

## 구현 흐름 한눈에 보기

1. Express에서 typed `EventBus`와 `BookEventListener`를 분리해, service가 side effect 대신 event fact만 발행하게 만든다.
2. NestJS에서는 `EventEmitterModule`과 `@OnEvent` listener로 같은 경계를 프레임워크 안으로 옮긴다.
3. 두 레인 모두 성공한 저장 뒤에만 `book.created`, `book.updated`, `book.deleted`를 emit하고, 실패한 삭제/갱신 경로에서는 emit하지 않는다.
4. 다만 Express e2e는 persistence 유지까지 한 번 더 확인하고, Nest e2e는 이벤트 발행 자체에 더 집중한다.
5. 두 레인 모두 현재는 in-process synchronous emitter를 쓴다. 테스트가 잠그는 것은 durable queue가 아니라 "같은 요청 흐름 안에서 handler가 즉시 호출된다"는 경계다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  2 passed (2)
Tests       10 passed (10)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run test:e2e
Test Files  3 passed (3)
Tests       12 passed (12)
```

e2e 재실행에서는 두 레인 모두 `DELETE /books/nonexistent`에서 이벤트 handler가 호출되지 않는다는 점이 다시 확인됐다. Express 쪽은 여기에 더해 "이벤트가 있어도 데이터 조회가 그대로 동작한다"는 시나리오까지 별도로 고정하고 있다. 다만 여기서 검증된 emit는 outbox나 broker publish가 아니라, EventEmitter 계열이 같은 프로세스 안에서 즉시 호출되는 형태다.

## 다음 프로젝트와의 연결

다음 `08-production-readiness`는 기능 확장보다 운영 규약을 다룬다. 그래서 이 lab은 이벤트 아키텍처 일반론이라기보다, 이후 운영/통합 계층이 기대할 수 있는 최소한의 "저장 성공 뒤 사실 발행" 경계를 먼저 고정하는 단계로 보는 편이 맞다.
