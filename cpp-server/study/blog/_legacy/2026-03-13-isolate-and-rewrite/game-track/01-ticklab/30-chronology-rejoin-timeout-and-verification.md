# 30 Rejoin Timeout And Verification

## 2026-03-11
### Session 1

- 목표: 현재 `ticklab`이 어떤 transcript와 reconnect 규칙을 검증하는지 고정한다.
- 진행: `arena-transcript.txt`, `tests/test_ticklab.cpp`, `Makefile`을 함께 읽었다.
- 판단: canonical coverage는 transcript fixture로 `HELLO -> QUEUE -> READY -> INPUT -> TICK` 순서를 재생하는 경로와, 별도 테스트로 stale sequence, draw timeout, grace window rejoin을 확인하는 경로로 나뉜다.
- 검증: README 표면은 `verified`, 테스트 최종 신호는 `ticklab tests passed.`다.
- 다음: 이 엔진을 소켓과 token ownership 위로 올리는 쪽은 `arenaserv`가 맡는다.

CLI:

```bash
$ cd study/game-track/01-ticklab
$ sed -n '1,160p' problem/data/arena-transcript.txt
$ sed -n '1,220p' cpp/tests/test_ticklab.cpp
$ cd cpp
$ make clean && make test
```

출력:

```text
ticklab tests passed.
```

이 시점의 핵심 코드는 reconnect grace window를 다루는 부분이었다.

```cpp
if (participant.disconnect_tick < 0 || static_cast<int>(this->global_tick_) - participant.disconnect_tick > grace_ticks)
{
    error = Error("expired_session", "reconnect grace expired");
    return false;
}
```

처음엔 reconnect는 네트워크 서버에서만 의미가 있을 줄 알았는데, 실제로는 세션 만료 판단 자체를 엔진이 먼저 들고 있기 때문에 `arenaserv`는 socket과 token ownership만 bridge 하면 된다. 이게 `ticklab`을 별도 lab으로 떼어 둔 가장 큰 이유로 보였다.

현재 경계:

- 포함: queue, ready, countdown, snapshot, hit, elimination, draw timeout, reconnect grace
- 제외: socket I/O, per-connection buffering, event loop

