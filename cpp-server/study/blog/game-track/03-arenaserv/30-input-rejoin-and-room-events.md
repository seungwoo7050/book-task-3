# arenaserv 3. input, rejoin, room event가 실제 소켓에서 버티는지 보기

capstone의 마지막 장면은 raw TCP 입력이 authoritative engine 규칙을 얼마나 정확하게 드러내는지 확인하는 데 있다. [`Server::handle_input()`](../../../game-track/03-arenaserv/cpp/src/Server.cpp)은 그 점을 잘 보여 준다. 함수는 `INPUT <seq> <dx> <dy> <facing> <fire>` 형식을 직접 파싱하고, 각 토큰을 정수로 바꾼 뒤 `MatchEngine::Input`으로 넘긴다. 문법이 틀리면 즉시 `ERROR invalid_input`을 보내고, 문법은 맞지만 규칙을 어기면 engine이 `stale_sequence`나 `invalid_input`을 돌려준다.

rejoin도 같은 방식으로 읽을 수 있다. `disconnect()`는 연결이 끊길 때 `engine.disconnect_player(token)`와 `token_to_fd.erase(token)`를 함께 호출한다. 그리고 새 소켓이 `REJOIN <token>`을 보내면 `handle_rejoin()`이 engine에게 grace window를 확인하게 하고, 성공하면 그 token을 새 fd에 다시 연결한다. transport는 끊겼지만 세션은 이어지는 구조다.

[`tests/test_arenaserv.py`](../../../game-track/03-arenaserv/cpp/tests/test_arenaserv.py)는 이 capstone proof를 세 시나리오로 나눠 보여 준다. `scenario_duel_and_rejoin()`은 duplicate nick 거절, grace 안 rejoin 성공, grace 밖 rejoin 실패, invalid input, stale sequence, 세 번의 `HIT` 뒤 `ELIM`과 `ROUND_END alpha`를 본다. `scenario_party_lobby()`는 3인과 4인 lobby, `room_full`, countdown, `SNAPSHOT 0`를 확인한다. `scenario_draw_timeout()`는 입력이 없어도 timed tick이 계속 흘러 `ROUND_END draw`가 도착하는지 본다.

직접 실행한 CLI는 아래처럼 닫힌다.

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/03-arenaserv/cpp
make clean && make test
```

```text
python3 tests/test_arenaserv.py
arenaserv smoke passed.
```

이 테스트가 중요한 이유는, arenaserv가 단순히 ticklab 엔진을 링크만 한 것이 아니라는 점을 보여 주기 때문이다. 동일한 engine이라도 token mapping, timed loop, error surface, rejoin bridge가 없으면 이 시나리오는 소켓에서 재현되지 않는다.

물론 일부러 남겨 둔 범위도 있다. UDP, prediction, rollback은 없고, 여러 room shard나 persistence도 다루지 않는다. `PING` 역시 usage 검증만 하고 별도 `PONG` surface를 열지 않는다. 그래도 이 capstone은 충분히 선명하다. ticklab에서 고정한 authoritative 규칙이 TCP 위에서도 그대로 유지된다는 것을 duel, rejoin, overflow, draw 네 장면으로 직접 증명하고 있기 때문이다.

