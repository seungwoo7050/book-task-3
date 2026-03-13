# 07-domain-events series map

이 프로젝트는 persistence 위에 side effect를 얹는 첫 단계다. 핵심 질문은 이벤트를 도입했다는 사실보다, 성공한 상태 변화 뒤에만 어떤 사실을 바깥으로 흘려보낼 것인가에 있다.

처음 읽을 때는 Express 쪽 `EventBus`와 `BookService`를 먼저 보는 편이 좋다. emit가 어디서 일어나는지 감이 잡힌 뒤 NestJS listener 쪽으로 넘어가면, 같은 구조를 프레임워크가 어떻게 감싸는지 더 쉽게 읽힌다.

## 이 글에서 볼 것

- 왜 service 안에서 직접 side effect를 호출하지 않았는지
- save/remove 뒤에만 event를 내보내는 이유가 무엇인지
- listener unit test와 e2e가 각각 무엇을 증명하는지

## source of truth

- `core/07-domain-events/README.md`
- `core/07-domain-events/problem/README.md`
- `core/07-domain-events/express/src/events/*`
- `core/07-domain-events/express/src/services/book.service.ts`
- `core/07-domain-events/nestjs/src/events/*`
- `core/07-domain-events/nestjs/src/books/books.service.ts`
- `core/07-domain-events/express/test/unit/event-bus.test.ts`
- `core/07-domain-events/nestjs/test/unit/book-event.listener.test.ts`

## 구현 흐름 한눈에 보기

1. EventBus와 listener를 분리해 side effect 수신자를 service 밖으로 뺀다.
2. create/update/delete 성공 뒤에만 `book.*` 이벤트를 발행한다.
3. unit/e2e로 emit와 consume 경계를 함께 확인한다.

## 대표 검증

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       5 passed (5)
test:e2e    5 passed (5)
```

```bash
$ COREPACK_ENABLE_AUTO_PIN=0 pnpm run build && pnpm run test && pnpm run test:e2e
Tests       8 passed (8)
test:e2e    4 passed (4)
```

## 다음 프로젝트와의 연결

다음 장 `08-production-readiness`에서는 feature 계층을 조금 더 키우기보다, health/readiness, runtime config, structured logging 같은 운영 규약이 앞에 나온다.
