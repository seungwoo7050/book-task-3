# 01-ticklab-cpp 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 room queue와 ready 기반 countdown을 처리한다, monotonic input sequence를 검증한다, fixed tick마다 state를 advance하고 snapshot을 생성한다를 한 흐름으로 설명하고 검증한다. 핵심은 `main`이 요구하는 동작을 source에 반영하는 것이다.

## 문제를 푸는 핵심 전략

- room queue와 ready 기반 countdown을 처리한다.
- monotonic input sequence를 검증한다.
- fixed tick마다 state를 advance하고 snapshot을 생성한다.
- 검증 기준은 `main` 테스트가 먼저 잠근 동작부터 맞추는 것이다.

## 코드 워크스루

- `../study/game-track/01-ticklab/cpp/src/MatchEngine.cpp`: 핵심 구현을 담는 파일이다.
- `../study/game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp`: 핵심 구현을 담는 파일이다.
- `../study/game-track/01-ticklab/cpp/tests/test_ticklab.cpp`: `main`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/game-track/01-ticklab/problem/data/arena-transcript.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/game-track/01-ticklab/cpp/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- 회귀 게이트는 `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../study/game-track/01-ticklab/cpp/Makefile`는 실행 루트와 모듈 경계를 고정해 검증이 어느 위치에서 돌아야 하는지 알려 준다.

## 정답을 재구성하는 절차

1. `../study/game-track/01-ticklab/cpp/src/MatchEngine.cpp`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `main`이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `main`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/game-track/01-ticklab/cpp test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/game-track/01-ticklab/cpp/src/MatchEngine.cpp`
- `../study/game-track/01-ticklab/cpp/include/inc/MatchEngine.hpp`
- `../study/game-track/01-ticklab/cpp/tests/test_ticklab.cpp`
- `../study/game-track/01-ticklab/problem/data/arena-transcript.txt`
- `../study/game-track/01-ticklab/cpp/Makefile`
