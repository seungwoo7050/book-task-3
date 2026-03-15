# commerce-backend series map

이 시리즈는 `commerce-backend`를 "7개 랩의 통합판"이라고만 보지 않고, 실제로는 얼마나 얕은 baseline인지까지 같이 읽는다. auth는 query-param 수준의 fake surface이고, admin/catalog/cart/order는 하나의 modular monolith 안에서 연결되지만, validation과 authorization은 거의 걸려 있지 않다. 더 정확히는 login이 user journey를 설명하는 장식으로는 쓰이지만, 실제 downstream identity는 bearer principal이 아니라 request param `customerEmail` 같은 입력으로 계속 흘러간다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   fake auth, public admin, cart-to-order flow, stock decrement, actuator `DOWN`까지 baseline의 실제 의미를 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 이 capstone이 "완성본"이 아니라 비교 기준선이라고 부를 만한 근거는 무엇인가
- auth, catalog, cart, order가 실제로는 어느 정도 깊이로만 연결되어 있는가
- v2가 필요한 이유가 문서가 아니라 소스와 실행 결과에서 어떻게 드러나는가
