# ircserv evidence ledger

`ircserv`은 roomlab의 subset 서버를 capstone 범위로 넓힌 프로젝트다. 아래 ledger는 그 확장을 `Phase 1`부터 `Phase 4`까지 다시 세운 것이다. 흐름을 따라가다 보면, capstone의 차이가 helper 수보다 dispatcher에서 실제로 어떤 command를 열었는지, 그리고 그 command가 channel state cleanup까지 책임지는지에 더 가까웠다는 점이 보인다.

## Phase 1

처음 바뀌는 곳은 서버 뼈대보다 dispatcher다. 이미 정의돼 있던 helper들이 비로소 실제 command surface로 열린다.

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: subset skeleton을 유지한 채 dispatcher 표면을 capstone 범위로 넓힌다.
- 변경 단위: `cpp/src/Executor.cpp`
- 처음 가설: roomlab의 helper 정의를 실제 command routing에 연결하는 것만으로도 capstone의 차이를 선명하게 보여 줄 수 있다.
- 실제 조치: `Executor::process()`에 `KICK`, `INVITE`, `TOPIC`, `CAP`, `MODE` 분기를 추가한다.
- CLI: `make clean && make test`
- 검증 신호: smoke test가 `CAP LS 302`를 registration 전에도 확인한다.
- 핵심 코드 앵커: `Executor::process()`
- 새로 배운 것: capstone 차이는 helper 존재 여부보다 dispatcher가 실제로 여는 command surface에서 가장 명확하게 드러난다.
- 다음: registration과 capability 광고를 baseline으로 다시 확인한다.

## Phase 2

capstone이라고 해서 registration 흐름이 완전히 새로워지지는 않는다. 대신 같은 registration 위에 "지금은 capstone 표면에 와 있다"는 최소 capability 신호가 더해진다.

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: registration은 roomlab와 이어 가되, client 호환성 신호를 더 분명히 한다.
- 변경 단위: `cpp/src/Executor.cpp`, `cpp/tests/test_irc_join.py`
- 처음 가설: `CAP LS 302`와 `005 ISUPPORT`만 있어도 raw TCP smoke에서 capstone 수준의 호환성 최소 신호를 보여 줄 수 있다.
- 실제 조치: `_execute_cap()`이 `CAP * LS :`를 돌려주고 `_execute_user()`는 `005`를 포함한 registration bundle을 유지한다.
- CLI: `make clean && make test`
- 검증 신호: alice, bob, carol 세 사용자가 모두 registration을 완료하고 alice는 `CAP LS 302` 응답도 먼저 받는다.
- 핵심 코드 앵커: `_execute_cap()`, `_execute_user()`, `tests/test_irc_join.py`
- 새로 배운 것: capstone이라도 CAP negotiation을 모두 구현하지 않고, smoke에 필요한 최소 surface만 열 수 있다.
- 다음: channel privilege와 mode state를 본다.

## Phase 3

이 phase부터 channel은 단순 room이 아니다. `invitedb`, `privdb`, mode bit가 실제 의미를 얻으면서, roomlab에서 준비해 둔 구조가 capstone 수준의 권한 모델로 바뀐다.

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: channel을 단순한 room이 아니라 privilege-bearing state machine으로 만든다.
- 변경 단위: `cpp/src/Channel.cpp`, `cpp/src/Executor.cpp`, `cpp/src/execute_join.cpp`
- 처음 가설: invite-only, topic lock, channel key, limit, operator 권한은 모두 channel state bit로 묶는 편이 설명하기 쉽다.
- 실제 조치: `Channel`의 `lbit`, `ibit`, `tbit`, `kbit`와 `privdb`, `invitedb`를 중심으로 `_execute_mode()`, `_execute_topic()`, `_execute_invite()`를 구현한다.
- CLI: `make clean && make test`
- 검증 신호: smoke test가 `MODE #ops +i`, `INVITE carol #ops`, `TOPIC #ops :control room`을 end-to-end로 통과한다.
- 핵심 코드 앵커: `Channel::part()`, `_execute_mode()`, `_execute_topic()`, `_execute_invite()`, `_execute_join()`
- 새로 배운 것: roomlab에서 이미 준비된 `invitedb`와 `privdb`가 capstone에서 실제 의미를 얻는다.
- 다음: KICK과 invite-only 재입장 거절, 최종 verification을 본다.

## Phase 4

마지막 phase는 advanced command가 reply만 맞는지보다, state cleanup까지 버티는지 보는 구간이다. `KICK`과 invite-only 재입장 거절이 특히 그 성격을 잘 보여 준다.

- 순서: 4
- 시간 표지: Phase 4
- 당시 목표: advanced command가 cleanup을 깨지 않는지 확인한다.
- 변경 단위: `cpp/src/Executor.cpp`, `cpp/tests/test_irc_join.py`
- 처음 가설: `KICK`은 broadcast만으로 끝나지 않고 target의 `chandb`까지 함께 지워야 room state가 남지 않는다.
- 실제 조치: `_execute_kick()`이 broadcast 뒤 `targetnode->chandb.erase(channame)`와 `chan->part(targetnode)`를 함께 수행하고, smoke test는 bob의 rejoin이 `473 invite-only`로 막히는지 본다.
- CLI: `make clean && make test`
- 검증 신호: `ircserv capstone smoke passed.`
- 핵심 코드 앵커: `_execute_kick()`, `tests/test_irc_join.py`
- 새로 배운 것: advanced command가 추가될수록 진짜 위험은 응답 포맷보다 state cleanup 누락이다.
- 다음: 다른 도메인 capstone인 [`../../game-track/02-arenaserv/README.md`](../../game-track/02-arenaserv/README.md)와 비교할 수 있다.

