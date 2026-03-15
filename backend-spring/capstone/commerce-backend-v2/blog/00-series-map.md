# commerce-backend-v2 series map

이 시리즈는 `commerce-backend-v2`를 "대표 capstone"이라고 부를 때 무엇이 실제로 baseline보다 깊어졌고, 무엇이 아직 mock 또는 미완료 seam에 남아 있는지를 소스와 `2026-03-14` 재실행 결과로 읽는다. persisted auth, role-based admin guard, validated catalog/cart/order/payment flow, Redis/Kafka wiring는 실제 구현으로 확인된다. 반대로 Google OAuth는 state/nonce mock이고, payment는 mock confirm이며, outbox publish는 notification row가 생긴 뒤에도 `published_at`가 비어 있는 현재 결함이 남아 있다. 중요한 건 automated suite가 이 마지막 bookkeeping까지 닫아 주는 것은 아니라는 점이다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   baseline 대비 무엇이 깊어졌는지, 그리고 왜 여전히 "production commerce platform"이라고 과장하면 안 되는지를 auth -> commerce flow -> async/ops 순서로 따라간다.

## 이 시리즈가 답하는 질문

- v2가 같은 커머스 도메인 위에서 실제로 더 깊어진 지점은 어디인가
- README의 "portfolio-grade" 주장 중 런타임에서 그대로 확인되는 것과 아닌 것은 무엇인가
- Redis, Kafka, health surface는 지금 어느 수준까지 검증됐고 어디서 멈추는가
