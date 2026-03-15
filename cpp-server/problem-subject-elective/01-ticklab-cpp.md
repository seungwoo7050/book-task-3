# 01-ticklab-cpp 문제지

## 왜 중요한가

authoritative simulation의 핵심 판단을 네트워크 없이 먼저 검증할 수 있어야 한다.

## 목표

시작 위치의 구현을 완성해 room queue와 ready 기반 countdown을 처리한다, monotonic input sequence를 검증한다, fixed tick마다 state를 advance하고 snapshot을 생성한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/game-track/01-ticklab/cpp/src/MatchEngine.cpp`
- `../study/game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp`
- `../study/game-track/01-ticklab/cpp/tests/test_ticklab.cpp`
- `../study/game-track/01-ticklab/problem/data/arena-transcript.txt`
- `../study/game-track/01-ticklab/cpp/Makefile`

## starter code / 입력 계약

- `../study/game-track/01-ticklab/cpp/src/MatchEngine.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- room queue와 ready 기반 countdown을 처리한다.
- monotonic input sequence를 검증한다.
- fixed tick마다 state를 advance하고 snapshot을 생성한다.
- hit, elimination, round timeout draw를 판정한다.
- reconnect grace window와 snapshot 재전송을 처리한다.

## 제외 범위

- `../study/game-track/01-ticklab/problem/data/arena-transcript.txt` fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 검증 기준은 `main`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/game-track/01-ticklab/problem/data/arena-transcript.txt` fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test
```

- `01-ticklab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-ticklab-cpp_answer.md`](01-ticklab-cpp_answer.md)에서 확인한다.
