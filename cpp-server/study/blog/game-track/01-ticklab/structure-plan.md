# ticklab structure plan

`ticklab`은 구현량보다 관점 전환이 더 중요한 문서다. 독자는 "게임 규칙을 많이 넣었다"보다 "왜 authoritative simulation을 네트워크보다 먼저 떼어 냈는가"를 이해해야 한다. 그래서 글도 phase machine, input order, reconnect proof 순서로 읽히게 설계한다.

## 10-engine-surface-and-room-phases.md

첫 글은 `MatchEngine.hpp`와 `register_player()`, `queue_player()`, `ready_player()`, `start_countdown()`, `start_round()`를 중심으로 잡는다. transport가 아직 없는데도 room lifecycle이 이미 충분히 설명 가능하다는 점을 독자가 먼저 받아들이게 만드는 것이 목표다.

## 20-input-ticks-and-projectiles.md

둘째 글은 authoritative 성격이 가장 잘 보이는 구간이다. `submit_input()`, `advance_one_tick()`, `process_inputs()`, `move_projectiles()`, `maybe_finish_round()`, `snapshot_json()`을 따라가며 stale sequence, orthogonal move 제약, projectile resolution, snapshot emission이 한 흐름이라는 점을 보여 준다.

## 30-rejoin-timeout-and-verification.md

마지막 글은 `rejoin_player()`, `expire_disconnected_players()`, `tests/test_ticklab.cpp`, `problem/data/arena-transcript.txt`를 중심에 둔다. `make clean && make test`, `ticklab tests passed.`를 proof의 마감 신호로 사용하고, engine이 이미 어디까지 책임지고 transport로 넘기는 몫은 무엇인지 정리한다.

