# ticklab — 접근 방식: 네트워크 없이 시뮬레이션만 먼저 검증한다

작성일: 2026-03-09

## 가장 먼저 결정해야 했던 것

이 lab의 핵심 결정은 "네트워크 서버로 만들 것인가, headless engine으로 만들 것인가"였다. 최종 목표인 `arenaserv`는 TCP 서버이므로, 바로 서버로 만드는 것이 자연스러워 보일 수 있다. 하지만 그렇게 하면 이 lab의 존재 이유가 사라진다.

## 접근 A: 바로 네트워크 서버로 구현한다

이 방법의 장점은 최종 결과물과 형태가 같다는 것이다. 하지만 단점이 치명적이었다. 소켓 lifecycle, reconnect 타이밍, send buffer flush, 그리고 tick advance와 입력 검증 — 이 모든 것이 한 프로세스 안에서 동시에 돌아간다. 테스트에서 실패했을 때, 그것이 네트워크 문제인지 시뮬레이션 문제인지 구분할 수 없다.

## 접근 B: headless simulation engine을 먼저 만든다

이 방법을 택했다. `MatchEngine` 클래스의 public API를 직접 호출하는 C++ 테스트를 작성하면, 네트워크 변수를 완전히 제거한 상태에서 시뮬레이션 로직만 검증할 수 있다.

대가는 있다 — `arenaserv`에서 같은 `MatchEngine`을 다시 사용하게 되므로, 코드 중복은 아니더라도 두 프로젝트를 유지해야 한다. 하지만 이 저장소는 학습 우선 구조이므로, concept boundary를 명확하게 만드는 편이 맞다고 판단했다.

## 구체적인 설계 결정

### Single room

이 단계에서 multi-room sharding은 필요 없다. room이 하나뿐이라는 제약이 오히려 "tick correctness에만 집중"이라는 목표를 강화한다.

### Countdown은 tick 기반 정수 step

카운트다운을 wall-clock 시간으로 처리하지 않았다. headless engine에는 시계가 없으므로, `countdown_remaining_`이라는 정수를 매 tick마다 1씩 줄이는 방식을 택했다. `countdown_steps = 3`이므로 3 tick이면 카운트다운이 끝난다. `arenaserv`에서는 이 tick을 100ms 간격의 timer event에 연결하면 wall-clock과 대응된다.

### Reconnect grace도 tick 수로 계산

같은 이유로, reconnect grace window도 `grace_ticks = 100`이라는 정수로 표현한다. 네트워크 서버에서는 100 tick × 100ms = 10초가 된다.

### Snapshot은 JSON 문자열

snapshot의 목적이 두 가지다: (1) 클라이언트에게 현재 상태를 전달하는 것, (2) 재접속 시 복구용 상태를 제공하는 것. JSON 문자열로 만들면 두 가지 모두에 사용할 수 있고, deterministic test에서 내용을 검증하기도 편하다.

## 버린 선택들

- **float physics**: 검증 범위가 불필요하게 커진다. 정수 grid(20×20)와 orthogonal 1타일 이동으로 충분하다.
- **multiple action types**: FIRE 하나만으로도 input → projectile → hit → elimination → round end라는 전체 이벤트 흐름을 보여줄 수 있다.
- **observer client model**: capstone으로 넘기기에 알맞은 복잡도다.
