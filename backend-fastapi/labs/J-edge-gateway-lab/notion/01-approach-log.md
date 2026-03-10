# 접근 로그

## 처음 고려한 선택지

1. 각 서비스가 자기 쿠키와 CSRF를 직접 처리하게 둔다.
2. gateway는 두되, 인증 API만 모으고 platform API는 클라이언트가 내부 서비스로 직접 호출한다.
3. gateway가 public API shape와 브라우저 상태를 전담하고, 내부는 bearer only로 고정한다.

## 선택한 방향

세 번째 방식을 채택했다. gateway를 public contract의 단일 진입점으로 두고, 내부 서비스는 browser-aware 상태를 알지 못하도록 만들었다.

## 그렇게 고른 이유

- 첫 번째 방식은 브라우저 상태가 서비스 전체로 퍼져 edge 책임이 사라진다.
- 두 번째 방식은 일부 route만 통합돼 public contract를 비교하기 어렵다.
- 세 번째 방식은 구현은 더 무겁지만, v1 public API와 v2 internal structure를 비교하기 가장 좋다.

## 의도적으로 단순화한 점

- request id는 단순 UUID 한 개로만 전달한다.
- gateway fan-out도 필요한 route에만 적용한다.
- edge cache, rate limit, circuit breaker 같은 운영 기능은 넣지 않는다.

## 이번 선택이 만든 제약

- gateway가 죽으면 public API 전체가 영향을 받는다.
- timeout, 오류 번역, websocket fan-out 같은 새 책임이 edge에 붙는다.
- 테스트도 service unit test와 top-level system test를 함께 봐야 한다.
