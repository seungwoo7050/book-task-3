# 07-domain-events structure plan

이 문서는 이벤트 소개문보다 "어느 성공 경계 뒤에서만 side effect가 흘러가도록 만들었는가"가 먼저 읽혀야 한다. 서사의 중심은 `Express 수동 event boundary -> emit timing -> Nest framework event boundary -> 테스트 격리 방식`이다.

## 읽기 구조

1. 왜 service 밖에 bus/listener를 둬야 했는지부터 잡는다.
2. Express `EventBus`, `BookEventListener`, `BookService`, `createApp`으로 수동 wiring과 emit 시점을 보여 준다.
3. NestJS `EventEmitterModule`, `BookEventListener`, `BooksService`로 같은 경계를 프레임워크 안으로 옮기는 흐름을 잇는다.
4. 실패 경로 비발행과 listener cleanup을 테스트 관점에서 분리해 적는다.
5. 마지막에 Express e2e는 persistence 유지까지, Nest e2e는 이벤트 발행 자체에 더 집중한다는 차이를 남긴다.

## 반드시 남길 근거

- Express `src/events/event-bus.ts`
- Express `src/events/book-event-listener.ts`
- Express `src/services/book.service.ts`
- Express `src/app.ts`
- Express unit/e2e 결과
- NestJS `src/app.module.ts`
- NestJS `src/events/events.module.ts`
- NestJS `src/events/book-event.listener.ts`
- NestJS `src/books/books.service.ts`
- NestJS service unit/listener unit/e2e 결과
- `docs/native-sqlite-recovery.md`

## 리라이트 톤

- 이벤트 아키텍처 일반론으로 길게 가지 않는다.
- emit 시점과 실패 비발행을 가장 먼저 읽히게 쓴다.
- 테스트가 증명하는 범위 차이를 감추지 않는다.
