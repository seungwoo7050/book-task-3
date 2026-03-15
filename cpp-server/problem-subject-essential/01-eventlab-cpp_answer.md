# 01-eventlab-cpp 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 지정한 포트에서 listening socket을 연다, 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다, 줄 단위 텍스트 프로토콜에서 PING <token>에 PONG <token>으로 응답한다를 한 흐름으로 설명하고 검증한다. 핵심은 `main` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 지정한 포트에서 listening socket을 연다.
- 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다.
- 줄 단위 텍스트 프로토콜에서 PING <token>에 PONG <token>으로 응답한다.
- 첫 진입점은 `../study/shared-core/01-eventlab/cpp/src/EventManager.cpp`이고, 여기서 `main` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/shared-core/01-eventlab/cpp/src/EventManager.cpp`: 핵심 구현을 담는 파일이다.
- `../study/shared-core/01-eventlab/cpp/src/main.cpp`: `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/shared-core/01-eventlab/cpp/src/Server.cpp`: 핵심 구현을 담는 파일이다.
- `../study/shared-core/01-eventlab/cpp/src/utils.cpp`: 핵심 구현을 담는 파일이다.
- `../study/shared-core/01-eventlab/cpp/include/inc/EventManager.hpp`: 핵심 구현을 담는 파일이다.
- `../study/shared-core/01-eventlab/cpp/tests/test_eventlab.py`: `wait_for_port`, `recv_text`, `send_line`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/shared-core/01-eventlab/cpp/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `main` 구현은 `wait_for_port` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.

## 정답을 재구성하는 절차

1. `../study/shared-core/01-eventlab/cpp/src/EventManager.cpp`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `wait_for_port` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `wait_for_port`와 `recv_text`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/shared-core/01-eventlab/cpp/src/EventManager.cpp`
- `../study/shared-core/01-eventlab/cpp/src/main.cpp`
- `../study/shared-core/01-eventlab/cpp/src/Server.cpp`
- `../study/shared-core/01-eventlab/cpp/src/utils.cpp`
- `../study/shared-core/01-eventlab/cpp/include/inc/EventManager.hpp`
- `../study/shared-core/01-eventlab/cpp/tests/test_eventlab.py`
- `../study/shared-core/01-eventlab/cpp/Makefile`
