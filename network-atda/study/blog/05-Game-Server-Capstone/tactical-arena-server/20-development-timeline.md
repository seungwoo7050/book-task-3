# Tactical Arena Server 개발 타임라인 2

## Day 2 — simulation 규칙, server 이벤트 루프, persistence

### Session 1

- 목표: `state.cpp`에서 "authoritative server"가 단순 relay와 어떻게 다른지 구체적인 코드로 확인한다.
- 진행: `test_state.cpp`를 먼저 읽었다. 첫 번째 블록은 sequence 5인 input과 sequence 4인 input을 순서를 뒤바꿔 submit하고, step 후 `last_input_sequence == 5`이며 플레이어가 오른쪽으로 이동했어야 한다고 단언한다.
- 이슈: 처음에는 마지막으로 받은 input을 반영하면 된다고 생각했다. 하지만 UDP는 패킷 순서가 바뀔 수 있어, "마지막으로 받은"이 아니라 "가장 높은 sequence"를 기준으로 해야 한다.
- 발견: `submit_input()`이 `input.sequence > player->latest_input.sequence`일 때만 저장한다. 이 한 줄이 out-of-order UDP input을 무시하는 전체 메커니즘이다.

핵심 코드:

```cpp
void MatchState::submit_input(const InputPacket& input) {
    if (auto* player = find_player_mut(input.player_id)) {
        if (input.sequence > player->latest_input.sequence) {
            player->latest_input = input;
        }
    }
}
```

- Session 2 예고: projectile hit → 사망 → respawn delay → 재생 흐름을 `step()`에서 어떻게 처리하는지 보기 위해 두 번째 test case를 읽는다.

### Session 2

- 목표: `MatchState::step()`의 fixed-tick 진행에서 forfeit, respawn, projectile 처리 순서를 확인한다.
- 진행: `test_state.cpp`의 두 번째 블록은 `projectile_damage=100`, `fire_cooldown_ms=0` 설정으로 플레이어 1이 발사하면 한 번에 사망, 3300ms 후 재생하는 시나리오를 검증한다. 세 번째 블록은 `resume_window_ms=200`을 초과하면 forfeit으로 처리하는가를 확인한다.
- 이슈: `step()`을 `step(100)` 한 번으로 모든 sim 업데이트가 된다고 생각했으나, 실제로는 projectile lifetime=1500ms가 남아 있어야 hit이 가능했다. 이 타이밍이 맞지 않으면 타깃이 살아 있는 채로 통과한다.
- 이슈 2: forfeit은 `resume_window_ms` 이후에 `mark_disconnected()`가 불리면 발동한다. 200ms window가 있어 짧은 disconnection은 forfeit 처리가 되지 않는다.

```cpp
// step() 내부의 처리 순서
apply_forfeit_timeouts(now_ms);
respawn_players(now_ms);
apply_inputs(now_ms, dt_seconds);
update_projectiles(now_ms, dt_seconds);
```

- 메모: 이 4줄의 순서가 중요하다. forfeit을 먼저 처리해야 죽은 플레이어가 이동하지 않고, respawn이 그 다음에 와야 respawn된 플레이어가 같은 tick에 input을 받을 수 있다.

### Session 3

- 목표: `SqliteRepository`의 `login_or_create`, `record_match`, stat 업데이트가 transaction 안에서 올바르게 동작하는지 확인한다.
- 진행: `test_repository.cpp`는 `:memory:` DB를 쓰기 때문에 파일 없이 실행된다. `login_or_create("alpha")`가 첫 호출이면 새 profile을 만들고, 두 번째 호출이면 같은 player_id를 리턴해야 한다. `record_match` 후에는 `match_history_count()`가 1이 된다.
- 이슈: `record_match()`에서 stats 업데이트와 match row 삽입이 같은 transaction에 묶여 있지 않으면, 서버 crash 시 match row만 남고 player stats가 없는 일관성 깨짐이 생긴다.
- 발견: `exec_or_throw("BEGIN TRANSACTION")` / `exec_or_throw("COMMIT")`이 `record_match()` 전체를 묶는다. SQLite `:memory:`에서도 transaction 경계는 동일하게 작동한다.

```bash
$ ctest --test-dir study/05-Game-Server-Capstone/tactical-arena-server/cpp/build \
    --output-on-failure -R test_repository
Test project .../cpp/build
    Start 3: test_repository
1/1 Test #3: test_repository ............ Passed    0.01 sec
```

- 정리:
  - `submit_input()`의 sequence guard는 authoritative server의 핵심이다. relay는 받은 순서대로 전달하지만, authoritative server는 "의미 있는 최신 상태"만 게임 세계에 반영한다.
  - `step()`의 처리 순서(forfeit → respawn → input → projectile)가 게임 규칙의 우선순위를 코드로 표현한다.
  - `record_match()`의 transaction 경계가 없으면 stats와 match history가 분리될 수 있다. `:memory:` 테스트로 이 경계를 단위 수준에서 검증할 수 있다.
