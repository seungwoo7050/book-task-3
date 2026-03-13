# ticklab series map

`ticklab`을 세 편으로 나눈 이유는 간단하다. 이 lab은 게임 규칙을 많이 설명하려는 문서가 아니라, authoritative engine이 먼저 무엇을 고정해야 하는지 보여 주는 문서이기 때문이다. 그래서 시리즈도 "공개 표면과 phase machine -> input과 tick 처리 -> reconnect와 proof" 순서로 흘러간다.

첫 글은 `MatchEngine`이 어떤 상수와 타입, 어떤 room phase를 갖는지부터 잡는다. 둘째 글은 stale sequence, 이동 제약, projectile, snapshot 같은 실제 authoritative 메커니즘을 따라간다. 마지막 글은 reconnect grace, draw timeout, transcript fixture를 묶어서 이 엔진이 어디까지 이미 검증됐는지 보여 준다.

## 글 순서

1. [10-engine-surface-and-room-phases.md](10-engine-surface-and-room-phases.md)
2. [20-input-ticks-and-projectiles.md](20-input-ticks-and-projectiles.md)
3. [30-rejoin-timeout-and-verification.md](30-rejoin-timeout-and-verification.md)

