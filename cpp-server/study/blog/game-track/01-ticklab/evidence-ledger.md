# ticklab evidence ledger

`ticklab`의 chronology는 서버 프로세스가 아니라 엔진 API가 어떻게 자라나는지에 맞춰 읽는 편이 자연스럽다. 먼저 공개 타입과 상수를 고정하고, 이어서 room phase를 만들고, 그다음 tick 안의 입력과 투사체 처리를 정리한 뒤, 마지막에 reconnect grace와 timeout proof로 닫히는 흐름이다.

## Phase 1

첫 phase에서 가장 먼저 필요한 것은 물리 계산이 아니라 엔진이 어떤 상태를 들고 살지 정하는 일이다. 이 시점의 설계가 뒤의 TCP capstone까지 그대로 이어진다.

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: headless authoritative engine의 공개 타입과 상수를 먼저 고정한다.
- 변경 단위: `cpp/include/inc/MatchEngine.hpp`
- 처음 가설: 네트워크 없이도 session, input, event, participant, projectile를 모두 표현할 수 있어야 나중에 transport를 갈아 끼울 수 있다.
- 실제 조치: `Error`, `Input`, `Event`, `Participant`, `Projectile`, `Phase`와 board/HP/countdown/grace 상수를 선언한다.
- CLI: `make clean && make test`
- 검증 신호: 엔진 테스트가 네트워크 없이 직접 public API를 호출한다.
- 핵심 코드 앵커: `MatchEngine.hpp`
- 새로 배운 것: authoritative server의 핵심은 소켓보다 먼저 "무슨 상태를 저장할지"를 명시하는 데 있다.
- 다음: 방 입장과 phase 전이를 만든다.

## Phase 2

상태 그릇이 생기고 나면, 그다음에는 한 room이 어떤 순서로 lobby에서 round로 넘어가는지 정해야 한다. 여기서부터 엔진은 단순한 데이터 저장소가 아니라 phase machine으로 읽힌다.

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: player registration, queue, ready, countdown, round start를 한 흐름으로 묶는다.
- 변경 단위: `cpp/src/MatchEngine.cpp`
- 처음 가설: lobby/countdown/in_round/finished 네 phase만 분명하면 transport 없이도 match lifecycle을 설명할 수 있다.
- 실제 조치: `register_player()`, `queue_player()`, `ready_player()`, `start_countdown()`, `start_round()`가 token 발급과 room phase event를 만든다.
- CLI: `make clean && make test`
- 검증 신호: transcript fixture가 `COUNTDOWN 3`과 `ROOM arena-1 in_round`를 확인한다.
- 핵심 코드 앵커: `register_player()`, `queue_player()`, `ready_player()`, `start_countdown()`, `start_round()`
- 새로 배운 것: match lifecycle은 socket accept보다 먼저 phase machine으로 고정하는 편이 훨씬 읽기 쉽다.
- 다음: tick 안에서 input과 projectile를 처리한다.

## Phase 3

phase가 고정되면 authoritative 엔진의 진짜 성격은 입력 acceptance 규칙과 tick 순서에서 드러난다. 누가 움직일 수 있고, 어떤 입력이 버려지고, snapshot이 언제 찍히는지가 이 구간에서 정해진다.

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: fixed tick 안에서 이동, 발사, hit, elimination, round end를 판정한다.
- 변경 단위: `cpp/src/MatchEngine.cpp`
- 처음 가설: authoritative engine의 핵심 버그는 physics보다 "입력 seq와 phase 제약"에서 먼저 나온다.
- 실제 조치: `submit_input()`이 stale sequence와 invalid move를 막고, `advance_one_tick()`이 `process_inputs()`, `move_projectiles()`, `maybe_finish_round()`를 순서대로 부른다.
- CLI: `make clean && make test`
- 검증 신호: `test_stale_sequence_and_validation()`과 transcript fixture가 `HIT`, `ELIM`, `ROUND_END alpha`를 확인한다.
- 핵심 코드 앵커: `submit_input()`, `advance_one_tick()`, `process_inputs()`, `move_projectiles()`, `maybe_finish_round()`
- 새로 배운 것: snapshot이 매 tick emitted 되기 때문에 authoritative state를 외부에 증명하기 쉬워진다.
- 다음: reconnect grace와 timeout draw를 확인한다.

## Phase 4

마지막 phase는 엔진이 happy path만 처리하지 않는다는 걸 보여 준다. session continuity와 종료 조건도 transport 밖에서 먼저 고정된다.

- 순서: 4
- 시간 표지: Phase 4
- 당시 목표: 세션 연속성과 종료 조건까지 엔진 레벨에서 닫는다.
- 변경 단위: `cpp/src/MatchEngine.cpp`, `cpp/tests/test_ticklab.cpp`, `problem/data/arena-transcript.txt`
- 처음 가설: reconnect는 transport 기능이 아니라 엔진이 기억하는 session/grace 정책이어야 한다.
- 실제 조치: `disconnect_player()`, `rejoin_player()`, `expire_disconnected_players()`를 두고, transcript fixture와 draw timeout test를 함께 돌린다.
- CLI: `make clean && make test`
- 검증 신호: `ticklab tests passed.`
- 핵심 코드 앵커: `rejoin_player()`, `expire_disconnected_players()`, `tests/test_ticklab.cpp`
- 새로 배운 것: headless engine만으로도 reconnect grace, stale input, draw timeout을 모두 증명할 수 있다.
- 다음: 같은 simulation을 rollback correction으로 확장한 [`../02-rollbacklab/README.md`](../02-rollbacklab/README.md)로 넘어간다.
