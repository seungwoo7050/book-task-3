# Concepts

- swipe, reorder, dismiss는 모두 threshold와 spring-back 규칙으로 설명할 수 있다.
- JS test에서는 gesture math를 검증하고, 디바이스에서는 UI-thread animation 체감을 확인한다.
- shared transition은 별도 라이브러리보다 Reanimated shared transition tag로 단순화한다.
