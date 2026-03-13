# 07-domain-events structure plan

이 문서는 이벤트를 "로그 몇 줄 찍는 기능"으로 읽히지 않게 해야 한다. 핵심은 `event boundary -> emit timing -> listener/e2e verification`이다.

## 읽기 구조

1. 왜 service 밖에 event bus와 listener를 둬야 했는지 먼저 잡는다.
2. 저장 성공 뒤에만 emit하는 이유를 Express/Nest 양쪽에서 보여 준다.
3. unit/e2e가 각각 어느 경계를 증명하는지 정리한다.

## 반드시 남길 근거

- Express `EventBus`
- Express `BookEventListener`
- Express `BookService`
- Nest `BookEventListener`
- Nest `BooksService`
- Express/Nest unit tests
- 두 레인의 `build && test && test:e2e`

## 리라이트 톤

- 이벤트 아키텍처 일반론으로 흐르지 않는다.
- "왜 이 시점에서 emit해야 했는가"가 먼저 읽히게 쓴다.
