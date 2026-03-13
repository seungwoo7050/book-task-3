# Tactical Arena Server 개발 타임라인 3

## Day 3 — integration 시나리오, 부하 스모크, bot demo

### Session 1

- 목표: `integration_test.py`가 어떤 시나리오를 실제 프로세스로 돌리는지 확인하고, resume token 흐름을 단위 테스트가 아닌 end-to-end로 검증하는 방식을 이해한다.
- 진행: `integration_test.py`를 열었다. `running_server()` context manager가 임시 포트를 할당해 서버를 subprocess로 띄우고, 테스트 후 종료한다. 시나리오는 세 가지다: (1) full match 완주, (2) player 1이 disconnection 후 resume token으로 재접속, (3) player 1이 disconnect하고 `resume_window_ms`를 초과해 forfeit 처리.
- 이슈: 처음에는 "reconnect 로직은 `state.cpp`에 있으니 단위 테스트로 충분하다"고 생각했다. 하지만 TCP connection의 actual close → re-accept → RESUME verb 처리 → game 재합류 흐름은 socket 계층까지 포함해야만 검증된다.
- 발견: `running_server()` context manager 하나가 실제 port binding, subprocess lifecycle, `:memory:` DB lifetime을 모두 감싸기 때문에 테스트 코드를 짧게 유지할 수 있다.

핵심 증거:

```py
with running_server(build_dir, match_duration_ms=3500, resume_window_ms=1200) as ctx:
    alpha = TcpClient(ctx.host, ctx.port)
    alpha.send("LOGIN", name="alpha")
    verb, fields = alpha.recv()
    assert verb == "LOGIN_OK"
    alpha_token = fields["token"]

    # ... match 진행 ...

    alpha.close()
    time.sleep(0.3)  # disconnection 시뮬레이션

    resumed = TcpClient(ctx.host, ctx.port)
    resumed.send("RESUME", token=alpha_token)
    verb, fields = resumed.recv()
    assert verb == "LOGIN_OK"
```

### Session 2

- 목표: `load_smoke_test.py`로 2 rooms / 8 bots 시나리오가 최소 보증 수준에서 통과하는지 확인한다.
- 진행: `load_smoke_test.py`는 `arena_loadtest` binary를 `--room-count 2 --bots-per-room 4`로 실행하고, stdout에 `status=ok`, `match_history` ≥ 2, `players` ≥ 8이 포함되면 통과한다.
- 이슈: capstone review에서 흔한 실수는 "단일 match는 통과하지만 2개 동시 match는 메모리 경합이나 accept thread 누락으로 실패"하는 경우다. load smoke가 이 경계를 확인한다.
- 발견: `arena_loadtest.cpp`는 bot을 2개 room에 분산해 각 room의 match를 독립적으로 완주시킨다. 각 bot은 `arena_bot.cpp`의 랜덤 입력 루프를 사용하며 real UDP socket을 쓴다.

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem load-test
[arena_loadtest] room_count=2 bots_per_room=4
[arena_loadtest] status=ok match_history=2 players=8
```

### Session 3

- 목표: `make test`가 CTest + integration + load smoke를 순서대로 통과하는지 최종 확인하고, bot demo로 시각적 확인을 마친다.

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test
[100%] Linked CXX executable arena_server
...
1/3 Test #1: test_protocol .............. Passed    0.00 sec
2/3 Test #2: test_state ................. Passed    0.00 sec
3/3 Test #3: test_repository ............ Passed    0.01 sec
100% tests passed, 0 tests failed out of 3
[integration] full_match: PASS
[integration] reconnect: PASS
[integration] forfeit: PASS
[load_smoke] status=ok match_history=2 players=8
```

```bash
$ make -C study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo
[server] listening on tcp 0.0.0.0:7000, udp 0.0.0.0:7001
[bot alpha] connected, match_id=1
[bot beta] connected, match_id=1
[server] match 1 finished, winner=alpha
```

- 정리:
  - integration harness의 `running_server()` + `RESUME` 시나리오는 `resume_window_ms` 설계를 "문서"가 아닌 "실제 프로세스 동작"으로 증명한다.
  - load smoke의 `status=ok match_history=2 players=8` 한 줄이 이 capstone의 scale assumption을 데이터로 남긴다.
  - `make test` 한 줄이 C++ 단위, Python integration, bot 부하 세 계층을 모두 통과해야 완성이다.
