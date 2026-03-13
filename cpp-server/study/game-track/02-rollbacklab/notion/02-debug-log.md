# Debug Log

- late input이 이미 적용된 입력과 같으면 rollback하지 않는 fast path를 먼저 넣었다.
- replay 검증은 "같은 applied input map을 다시 돌렸을 때 최종 상태가 같은가"로 단순화했다.
