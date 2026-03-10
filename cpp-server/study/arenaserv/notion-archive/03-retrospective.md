# arenaserv — 회고: 이 저장소에서 가장 "게임서버다운" 프로젝트

작성일: 2026-03-09

## 이 capstone이 보여주는 것

`arenaserv`는 이 저장소에서 "게임 서버로서 무엇을 할 수 있는가"를 가장 직접적으로 보여주는 프로젝트다. 다른 프로젝트들이 각각의 계층을 분리하거나 IRC 프로토콜을 구현하는 것이었다면, arenaserv는 **room queue → countdown → tick-based simulation → hit/elimination → round end → reconnect**라는 게임 서버의 전체 lifecycle을 하나로 합친다.

pure TCP라서 transport와 server authority를 직접적으로 볼 수 있다. WebSocket이나 HTTP 같은 상위 프로토콜이 없으므로, 소켓에서 읽은 바이트가 그대로 명령이고, 서버가 쓴 바이트가 그대로 이벤트다. 이 투명함이 학습 자료로서의 가치를 높인다.

## 좋았던 것

**네 가지 시나리오를 모두 smoke로 재현했다.** 2인 duel(HIT → ELIM → ROUND_END), 3인/4인 lobby(countdown → snapshot 시작), room overflow(5번째 클라이언트 거절), draw timeout(ROUND_END draw) — 이 네 가지가 자동화된 테스트로 확인된다. "동작합니다"를 주장하는 것이 아니라, "이 시나리오들이 재현됩니다"를 증거로 보여줄 수 있다.

**ticklab에서 시뮬레이션을 먼저 검증한 전략이 효과적이었다.** arenaserv에서 네트워크 관련 버그(이벤트 flush 타이밍, fd 매핑 정리)가 나왔을 때, 시뮬레이션 로직은 의심하지 않아도 됐다. "MatchEngine은 ticklab에서 검증했으니, 이 버그는 네트워크 통합 부분에 있다"는 판단이 가능했다. 이것이 bridge lab의 존재 이유다.

## 아쉬운 것

**single room 고정이다.** 실제 게임 서버에서는 방이 여러 개이고, MatchEngine 인스턴스도 여러 개다. 매칭 시스템이 방을 만들고, 각 방이 독립적으로 tick을 돌린다. 이 구조를 보여주려면 room manager 계층이 하나 더 필요하고, 이건 arenaserv의 범위를 넘는다.

**FIRE 하나만으로는 combat richness가 제한적이다.** 이동과 발사만 있고, 스킬, 아이템, 지형 효과 같은 것이 없다. 게임 서버를 보여주는 것이라면 충분하지만, "복잡한 게임 로직을 어떻게 관리하는가"라는 질문에 답하기에는 부족하다.

**client PING/latency reflection이 최소 수준이다.** `PING 12`를 보내면 서버가 no-op으로 받아들일 뿐, 실제로 latency를 측정하거나 반영하는 기능은 없다. 네트워크 게임에서 중요한 부분이지만, 이 lab의 범위 밖으로 판단했다.

## 다시 한다면 바꿀 것

- **room lifecycle과 match loop를 별도 class로 분리**: 현재 Server가 MatchEngine을 직접 소유하고 있다. RoomManager → Room → MatchEngine 구조로 분리하면, multi-room 확장이 자연스러워진다.
- **spectator reconnect**: 현재 reconnect는 참가자만 가능하다. 관전자 reconnect까지 넣으면 state continuity 시연이 더 강해진다.
- **post-round rematch**: 라운드가 끝나면 서버가 종료 상태가 된다. "다시 하기" 기능을 넣으면 room lifecycle의 순환을 보여줄 수 있다.
