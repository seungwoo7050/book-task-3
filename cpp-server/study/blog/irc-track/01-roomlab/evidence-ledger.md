# roomlab evidence ledger

`roomlab`은 `eventlab`과 `msglab`에서 나눠 둔 runtime과 parser를 실제 TCP 상태 전이 위로 올리는 첫 실험이다. 아래 ledger는 그 과정을 `Phase 1`부터 `Phase 4`까지 다시 묶은 것이다. 흐름을 따라가다 보면, 이 lab의 무게중심이 기능 수보다 `Connection`과 `Channel`의 인덱스를 어떻게 유지하느냐에 더 가까웠다는 점이 자연스럽게 드러난다.

## Phase 1

첫 phase에서 가장 먼저 커지는 것은 command 집합이 아니라 세션 객체다. 이제 fd 하나는 단순 연결이 아니라, 등록 전과 등록 후를 지나가는 사용자 상태를 담아야 한다.

- 순서: 1
- 시간 표지: Phase 1
- 당시 목표: event loop에 IRC용 connection state와 parser batch 처리를 붙인다.
- 변경 단위: `cpp/include/inc/Connection.hpp`, `cpp/src/Connection.cpp`, `cpp/src/Server.cpp`
- 처음 가설: socket loop는 거의 재사용하되, connection별 auth/registration/channel 상태만 추가하면 subset 서버가 시작된다.
- 실제 조치: `Connection`에 `nickname`, `username`, `chandb`, `is_authed`, `is_registered`를 넣고 `Server::_run_event_loop()`에서 `Parser::make_messages()`와 `Executor::process()`를 연결한다.
- CLI: `make clean && make test`
- 검증 신호: smoke test의 `register()` helper가 `005` 응답을 기다린다.
- 핵심 코드 앵커: `Connection::Connection()`, `Server::_run_event_loop()`
- 새로 배운 것: IRC 서버가 되어도 event loop의 큰 흐름은 바뀌지 않고, 상태만 `Connection`으로 옮겨 간다.
- 다음: PASS/NICK/USER 등록 단계를 고정한다.

## Phase 2

runtime과 parser가 붙으면 그다음엔 누가 "등록된 사용자"인지 정해야 한다. 이 phase는 subset 범위를 command 개수보다 registration contract로 분명히 한 시점에 가깝다.

- 순서: 2
- 시간 표지: Phase 2
- 당시 목표: subset 범위의 registration contract를 완성한다.
- 변경 단위: `cpp/src/Executor.cpp`
- 처음 가설: core subset은 `PASS`, `NICK`, `USER`만으로 registration을 끝낼 수 있어야 한다.
- 실제 조치: `_execute_pass()`, `_execute_nick()`, `_execute_user()`를 만들고 `nickdb`를 유지하며 `001`부터 `005 ISUPPORT`까지 돌려준다.
- CLI: `make clean && make test`
- 검증 신호: `test_roomlab.py`가 `register(alice)`와 `register(bob)`에서 모두 `001`과 `005`를 확인한다.
- 핵심 코드 앵커: `Executor::process()`, `_execute_pass()`, `_execute_nick()`, `_execute_user()`
- 새로 배운 것: `Executor.cpp` 안에 CAP/TOPIC/MODE helper가 있어도, 실제 subset 범위는 `process()`에서 어떤 command를 routing하는지가 결정한다.
- 다음: room lifecycle을 붙인다.

## Phase 3

등록이 끝난 뒤부터는 IRC 서버의 얼굴이 room lifecycle에서 드러난다. 그런데 이 phase에서 중요한 것은 JOIN 응답 문구보다, membership을 사용자와 서버 양쪽에서 동시에 관리하는 방식이다.

- 순서: 3
- 시간 표지: Phase 3
- 당시 목표: channel 생성, 입장, 퇴장, 빈 channel 정리를 한 흐름으로 묶는다.
- 변경 단위: `cpp/include/inc/Channel.hpp`, `cpp/src/execute_join.cpp`
- 처음 가설: channel state는 `server.chandb`와 `node->chandb`를 동시에 유지해야 cleanup이 안전하다.
- 실제 조치: `_execute_join()`이 channel 생성/재입장/limit/key/invite-only 검사를 하고 `_execute_part()`와 `JOIN 0`이 양쪽 인덱스를 함께 정리한다.
- CLI: `make clean && make test`
- 검증 신호: alice와 bob 모두 `JOIN #lab`에 성공하고, not-on-channel 오류도 테스트로 확인한다.
- 핵심 코드 앵커: `_execute_join()`, `_execute_part()`, `Channel::part()`
- 새로 배운 것: founder operator와 `privdb`, `invitedb` 같은 구조는 이미 여기서 준비되지만, roomlab은 dispatcher 단계에서 scope를 좁혀 둔다.
- 다음: 메시지 전달과 disconnect cleanup을 본다.

## Phase 4

마지막 phase는 subset 서버가 "작동한다"를 넘어서 "깨끗하게 정리된다"는 걸 보여 주는 구간이다. delivery와 cleanup이 따로 가지 않고 하나의 smoke path에서 만난다.

- 순서: 4
- 시간 표지: Phase 4
- 당시 목표: subset 서버답게 메시지를 전달하고 나간 사용자를 깨끗하게 정리한다.
- 변경 단위: `cpp/src/Executor.cpp`, `cpp/src/Server.cpp`, `cpp/tests/test_roomlab.py`
- 처음 가설: `QUIT`와 소켓 close를 같은 cleanup path로 수렴시키면 channel 잔재를 줄일 수 있다.
- 실제 조치: `_execute_privmsg()`, `_execute_notice()`, `_execute_quit()`가 delivery와 broadcast를 처리하고, `Server::_disconnect()`가 nickdb와 chandb를 함께 비운다.
- CLI: `make clean && make test`
- 검증 신호: `roomlab smoke passed.`
- 핵심 코드 앵커: `_execute_privmsg()`, `_execute_notice()`, `_execute_quit()`, `Server::_disconnect()`, `tests/test_roomlab.py`
- 새로 배운 것: subset 서버에서도 duplicate nick, broadcast, quit cleanup, not-on-channel error까지 들어가야 capstone과의 차이가 선명해진다.
- 다음: advanced command를 dispatcher에 연결한 [`../02-ircserv/README.md`](../02-ircserv/README.md)로 넘어간다.

