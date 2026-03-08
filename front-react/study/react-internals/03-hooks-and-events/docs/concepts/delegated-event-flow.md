# Delegated Event Flow

이 단계는 DOM prop에 직접 listener를 다는 대신 root container에 필요한 event type만 등록한다.

## 흐름

1. host tree를 만들 때 handler를 DOM prop과 분리한다.
2. commit 뒤 DOM node와 handler map을 다시 sync한다.
3. native event가 root까지 올라오면 target부터 parent 방향으로 handler를 찾는다.
4. handler는 `currentTarget`이 고정된 delegated event wrapper를 받는다.

## 왜 이렇게 했는가

- handler binding이 rerender 이후에도 한 경로로 다시 맞춰진다.
- 동적으로 생긴 node도 같은 dispatch 경로를 탄다.
- "framework event system"을 magic이 아니라 data structure와 dispatch loop로 설명할 수 있다.
