# 40 Multi Client Verification And Boundaries

## 2026-03-11
### Session 1

- 목표: 현재 `arenaserv`가 어떤 multi-client capstone path를 canonical verification으로 잡는지 고정한다.
- 진행: `Makefile`, `cpp/README.md`, `tests/test_arenaserv.py`를 함께 읽었다.
- 판단: 이 lab의 smoke coverage는 한 번의 duel만 보는 것이 아니라 `duel_and_rejoin`, `party_lobby(3)`, `party_lobby(4)`, `draw_timeout` 네 시나리오를 따로 돌려 duplicate nick, rejoin grace, room full, invalid/stale input, hit/elimination, draw timeout까지 묶는다.
- 검증: README 표면은 `verified`, 테스트 최종 신호는 `arenaserv smoke passed.`다.
- 다음: 같은 저장소의 다른 capstone 비교는 `ircserv`가 맡는다.

CLI:

```bash
$ cd study/game-track/02-arenaserv/cpp
$ sed -n '1,220p' Makefile
$ sed -n '1,260p' tests/test_arenaserv.py
$ make clean && make test
```

출력:

```text
arenaserv smoke passed.
```

이 시점의 핵심 코드는 테스트가 시나리오를 명시적으로 분리하는 부분이었다.

```python
scenario_duel_and_rejoin(server_path, base_port)
scenario_party_lobby(server_path, base_port + 1, 3)
scenario_party_lobby(server_path, base_port + 2, 4)
scenario_draw_timeout(server_path, base_port + 3)
```

처음엔 duel 하나만 확인해도 충분할 것 같았는데, 실제 capstone은 lobby capacity와 draw timeout까지 별도 시나리오로 분리해 두었다. 그래서 `arenaserv`는 단일 happy path demo가 아니라, authoritative TCP server가 지켜야 할 계약 묶음을 테스트로 고정한 프로젝트로 읽힌다.

현재 경계:

- 포함: `HELLO`, `QUEUE`, `READY`, `INPUT`, `REJOIN`, `LEAVE`, snapshot, hit/elimination, reconnect grace
- 제외: UDP, rollback, shard, persistence, external matchmaking

