# 01-eventlab-cpp 문제지

## 왜 중요한가

non-blocking TCP 서버의 최소 event loop를 구현하고, 연결 수명주기를 다른 도메인 규칙 없이 관찰할 수 있어야 한다.

## 목표

시작 위치의 구현을 완성해 지정한 포트에서 listening socket을 연다, 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다, 줄 단위 텍스트 프로토콜에서 PING <token>에 PONG <token>으로 응답한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/shared-core/01-eventlab/cpp/src/EventManager.cpp`
- `../study/shared-core/01-eventlab/cpp/src/main.cpp`
- `../study/shared-core/01-eventlab/cpp/src/Server.cpp`
- `../study/shared-core/01-eventlab/cpp/src/utils.cpp`
- `../study/shared-core/01-eventlab/cpp/tests/test_eventlab.py`
- `../study/shared-core/01-eventlab/cpp/Makefile`

## starter code / 입력 계약

- `../study/shared-core/01-eventlab/cpp/src/EventManager.cpp`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 지정한 포트에서 listening socket을 연다.
- 여러 클라이언트를 accept하고 read/write 이벤트를 처리한다.
- 줄 단위 텍스트 프로토콜에서 PING <token>에 PONG <token>으로 응답한다.
- 일반 입력은 ECHO <line>으로 되돌린다.
- idle connection에 keep-alive를 보내고 응답이 없으면 정리한다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `wait_for_port`와 `recv_text`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/cpp-server/study/shared-core/01-eventlab/cpp test
```

- `01-eventlab`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-eventlab-cpp_answer.md`](01-eventlab-cpp_answer.md)에서 확인한다.
