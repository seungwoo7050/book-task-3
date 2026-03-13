# 05. Game Server Capstone blog

이 트랙의 blog 시리즈는 지금까지의 네트워크 학습이 하나의 설명 가능한 서버 프로젝트로 어떻게 통합됐는지 복원한다. `problem/Makefile`, `cpp/src/`, `cpp/tests/`, `problem/script/*`, `docs/`를 기준으로 chronology를 세 구간으로 나눠 기록한다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| :--- | :--- | :--- |
| Tactical Arena Server | [`README.md`](tactical-arena-server/README.md) | [`../../05-Game-Server-Capstone/tactical-arena-server/README.md`](../../05-Game-Server-Capstone/tactical-arena-server/README.md) |

## 읽는 순서
1. [`Tactical Arena Server`](tactical-arena-server/README.md)에서 source set과 구간 분할 기준을 본다.
2. `10-development-timeline.md`로 build/setup과 프로토콜 경계를 잡는다.
3. `20-development-timeline.md`로 state, room, resume 흐름을 따라간다.
4. `30-development-timeline.md`로 CTest, integration, load smoke까지 마무리한다.

## source-first 메모
- capstone은 파일 수가 많아 하나의 timeline으로 압축하지 않고 `setup`, `protocol/state`, `integration/verification` 세 구간으로 나눴다.
- inline 증거는 `protocol.cpp`, `arena_server.cpp`, `state.cpp`, `repository.cpp`, `test_protocol.cpp`에서 뽑는다.
- 정확한 일시 대신 `Day/Session`을 쓰고, `problem/Makefile`의 `configure/build/test/run-bot-demo/load-test` 순서를 기준 chronology로 삼는다.
- 구간 분할은 소스/테스트/하네스가 드러내는 일반적인 개발자 흐름에 맞춰 추론했다.
