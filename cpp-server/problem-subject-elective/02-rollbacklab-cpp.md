# 02-rollbacklab-cpp 문제지

## 왜 중요한가

ticklab이 authoritative tick simulation을 보여 주는 단계였다면, 이번 프로젝트는 네트워크를 붙이기 전에 rollback 자체를 분리해 보는 단계다. socket, matchmaking, persistence 없이 prediction -> late input -> rollback -> resimulation -> convergence check만 남겼다.

## 목표

headless simulation만으로 rollback을 설명하는 프로젝트다. 여기서 핵심은 "입력이 늦게 도착했을 때 어느 시점으로 되돌아가야 하는가"이지, 서버 소켓을 여는 것이 아니다.

## 시작 위치

- `../study/game-track/02-rollbacklab/cpp/src/RollbackSession.cpp`
- `../study/game-track/02-rollbacklab/cpp/include/inc/RollbackSession.hpp`
- `../study/game-track/02-rollbacklab/cpp/tests/test_rollbacklab.cpp`
- `../study/game-track/02-rollbacklab/problem/data/late-input-timeline.txt`
- `../study/game-track/02-rollbacklab/cpp/Makefile`

## starter code / 입력 계약

- `../study/game-track/02-rollbacklab/cpp/src/RollbackSession.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- future input fast path
- late input rollback
- no-op late input fast path
- two-player resimulation convergence
- 이 네 경계가 테스트로 고정돼야 한다.

## 제외 범위

- `../study/game-track/02-rollbacklab/problem/data/late-input-timeline.txt` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 검증 기준은 `main`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/game-track/02-rollbacklab/problem/data/late-input-timeline.txt` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/02-rollbacklab/cpp test
```

- `02-rollbacklab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-rollbacklab-cpp_answer.md`](02-rollbacklab-cpp_answer.md)에서 확인한다.
