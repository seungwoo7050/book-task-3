# ticklab — 회고: 네트워크 없는 게임 서버가 가르쳐준 것

작성일: 2026-03-09

## 이 lab의 크기와 의미

`ticklab`은 이 저장소에서 가장 작은 프로젝트다. 소스 파일이 `MatchEngine.cpp` 하나뿐이고, 바이너리도 테스트 실행 파일(`ticklab_tests`) 하나다. 서버가 아니니까 `main.cpp`도 없고, event loop도 없고, 소켓도 없다.

그런데 이 작은 프로젝트가 커리큘럼에서 하는 역할은 생각보다 크다. `roomlab`은 "소켓에서 읽은 메시지로 서버 상태를 바꾸는 것"을 보여주었다. 하지만 `roomlab`의 상태 변화는 "사용자가 요청할 때만" 일어난다 — JOIN을 보내야 채널에 가입되고, PRIVMSG를 보내야 메시지가 전달된다. 이건 **이벤트 드리븐** 모델이다.

게임 서버는 다르다. 사용자가 입력을 보내든 안 보내든, **서버의 시뮬레이션은 매 tick 전진한다**. 투사체는 매 tick 이동하고, 충돌은 매 tick 판정되고, 라운드 타임아웃은 매 tick 카운트된다. 이것이 ticklab에서 분리해 본 핵심 개념이다.

## 좋았던 것

**reconnect grace와 snapshot regeneration을 네트워크 없이 검증할 수 있었다.** 이건 headless engine의 가장 큰 장점이다. `disconnect_player()`와 `rejoin_player()`를 직접 호출하고, tick을 원하는 만큼 정확히 전진시킨 뒤, 이벤트를 확인한다. 네트워크 지연이나 타이밍 문제가 전혀 없다.

그리고 **최종 `arenaserv`에서 재사용할 시뮬레이션 규칙을 먼저 고정했다.** `arenaserv`의 `MatchEngine.cpp`는 ticklab에서 복사한 것이다(import가 아니라 copy — 이 결정에 대해서는 arenaserv의 notion에서 다룬다). 시뮬레이션 규칙이 ticklab에서 이미 네 가지 테스트로 검증되었으므로, arenaserv에서는 네트워크 통합만 신경 쓰면 된다.

## 아쉬운 것

**single-room 고정이라 실제 운영형 matchmaking을 보여주지는 못한다.** 이 lab에서는 MatchEngine이 room 하나를 직접 관리한다. 실제 게임 서버에서는 방이 여러 개이고, 방마다 독립적인 tick이 돌아야 한다. 이건 scope 제한이라 어쩔 수 없지만, 독자가 "MatchEngine = 서버 전체"라고 오해하지 않도록 문서에서 명시해야 한다.

**countdown이 tick step이라 wall-clock과 1:1 대응되지 않는다.** `countdown_steps = 3`은 "3 tick"이지 "3초"가 아니다. `arenaserv`에서 tick_interval이 100ms이면 0.3초가 된다. 이 변환이 문서에서 명확하지 않으면 혼란을 줄 수 있다.

## 다시 한다면 바꿀 것

- **fixture transcript를 두 개 이상 둘 수 있다.** 현재는 `arena-transcript.txt` 하나로 win path만 검증한다. draw path용 fixture를 별도로 두면 시나리오 커버리지가 늘어난다.
- **snapshot schema를 별도 문서로 뺄 수 있다.** ticklab과 arenaserv가 같은 schema를 사용하므로, 문서로 계약을 명시하면 두 프로젝트 사이의 관계가 더 명확해진다.
