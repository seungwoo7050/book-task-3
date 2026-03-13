# 02 rollbacklab

| 항목 | 내용 |
| --- | --- |
| 상태 | `verified` |
| 문제 질문 | late input 때문에 이미 계산한 frame을 어떻게 되감고 다시 계산할 것인가 |
| 내가 만든 답 | `RollbackSession`, `FrameInputBuffer`, `StateSnapshot`, `ResimResult`로 분리한 headless rollback simulation lab |
| 검증 | `cd cpp && make clean && make test` |

## 문제를 어떻게 해석했나

`01-ticklab`이 authoritative tick simulation을 보여 주는 단계였다면, 이번 프로젝트는 네트워크를 붙이기 전에 rollback 자체를 분리해 보는 단계다. socket, matchmaking, persistence 없이 prediction -> late input -> rollback -> resimulation -> convergence check만 남겼다.

## 공개 표면

- `problem/README.md`
- `cpp/README.md`
- `cpp/include/inc/RollbackSession.hpp`
- `cpp/src/RollbackSession.cpp`
- `cpp/tests/test_rollbacklab.cpp`
- `docs/README.md`
- `notion/README.md`

## 지금 고정한 약속

- future input은 버퍼에만 쌓고 바로 rollback하지 않는다.
- 이미 지난 frame의 입력이 바뀌면 그 frame부터 현재 frame까지 다시 계산한다.
- 같은 late input이 다시 오면 no-op fast path로 끝낸다.
- replay 뒤에는 같은 입력 세트로 한 번 더 굴려 deterministic convergence를 확인한다.

## 다음 단계

rollback을 분리해 본 뒤에는 이 엔진을 TCP transport와 room/session 관리에 연결하는 [03-arenaserv](../03-arenaserv/README.md)로 넘어간다.
