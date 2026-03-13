# ticklab 3. reconnect grace와 transcript proof로 엔진을 닫기

headless engine이라고 해서 happy path만 보면 부족하다. `ticklab`의 마지막 장면은 reconnect grace, stale input rejection, draw timeout까지 엔진 자체가 책임진다는 사실을 확인하는 데 있다. 그래야 뒤의 TCP server가 규칙을 다시 해석하지 않고 bridge 역할에 집중할 수 있다.

[`rejoin_player()`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)는 그 점을 가장 잘 보여 준다. 세션 토큰이 존재하고 `disconnect_tick`이 `grace_ticks` 안에 있으면, 엔진은 다시 `WELCOME <token>`을 보내고 현재 room phase를 알려 준다. phase가 `Countdown`이면 남은 countdown을, `InRound`나 `Finished`면 최신 snapshot을 함께 보낸다. reconnect가 transport 복구가 아니라 session continuity 정책이라는 뜻이다.

반대로 grace를 넘기면 [`expire_disconnected_players()`](../../../game-track/01-ticklab/cpp/src/MatchEngine.cpp)가 disconnected participant를 처리한다. round 중이라면 그 사용자를 `ELIM`시키고, 이어서 `maybe_finish_round()`가 승패나 draw를 닫는다. 즉 끊어진 플레이어는 단순히 잊히는 것이 아니라 authoritative world state 안에서 정리된다.

[`cpp/tests/test_ticklab.cpp`](../../../game-track/01-ticklab/cpp/tests/test_ticklab.cpp)는 이 흐름을 네 방향에서 확인한다. `arena-transcript.txt`를 따라가며 `COUNTDOWN`, `ROOM ... in_round`, `HIT`, `ROUND_END alpha`를 보는 transcript fixture가 있고, stale sequence와 invalid diagonal move를 거절하는 validation test가 있다. 이어서 reconnect grace 안팎을 비교하는 test와, 아무도 죽지 않았을 때 `ROUND_END draw`로 닫히는 timeout test가 따라온다.

직접 실행한 CLI는 아래처럼 매우 간단하게 끝난다.

```sh
cd /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp
make clean && make test
```

```text
./ticklab_tests
ticklab tests passed.
```

짧은 출력이지만 의미는 크다. authoritative 판단의 핵심, 즉 phase 전이, stale sequence, snapshot, reconnect grace, draw timeout은 이미 네트워크 없이 proof를 마쳤다는 뜻이기 때문이다. 다음 문서인 [`../02-rollbacklab/README.md`](../02-rollbacklab/README.md)은 바로 이 엔진에 late input correction을 붙이고, 그 뒤 [`../03-arenaserv/README.md`](../03-arenaserv/README.md)에서 TCP 서버에 올린다.
