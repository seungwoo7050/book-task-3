# eventlab series map

이 시리즈는 별도 노트 계층 없이 `eventlab`의 런타임 경계를 다시 읽기 위한 지도다. 설명이 비는 부분은 현재 소스와 테스트를 읽는 일반적인 수준의 개발자가 자연스럽게 도달할 수 있는 범위까지만 추론한다.

## 이 프로젝트가 답하는 질문

- non-blocking TCP 서버의 최소 runtime surface를 parser 없이 어디까지 설명할 수 있을까
- keep-alive와 disconnect cleanup을 application contract로 잡으면 어떤 코드 경계가 생길까

## 읽는 순서

1. [10-chronology-runtime-and-socket-surface.md](10-chronology-runtime-and-socket-surface.md)
2. [20-chronology-protocol-loop-and-keepalive.md](20-chronology-protocol-loop-and-keepalive.md)
3. [30-chronology-smoke-verification-and-boundaries.md](30-chronology-smoke-verification-and-boundaries.md)

## 참조한 실제 파일

- `study/shared-core/01-eventlab/README.md`
- `study/shared-core/01-eventlab/problem/README.md`
- `study/shared-core/01-eventlab/cpp/README.md`
- `study/shared-core/01-eventlab/cpp/Makefile`
- `study/shared-core/01-eventlab/cpp/include/inc/EventManager.hpp`
- `study/shared-core/01-eventlab/cpp/include/inc/Server.hpp`
- `study/shared-core/01-eventlab/cpp/src/EventManager.cpp`
- `study/shared-core/01-eventlab/cpp/src/Server.cpp`
- `study/shared-core/01-eventlab/cpp/src/main.cpp`
- `study/shared-core/01-eventlab/cpp/tests/test_eventlab.py`
- `study/shared-core/01-eventlab/docs/README.md`

## Canonical CLI

```bash
cd study/shared-core/01-eventlab/cpp
make clean && make test
```

## Git Anchor

- `2026-03-09 73372bd Add project: backend-fastapi, backend-spring, cpp-server`
- `2026-03-10 7dc71a8 docs: enhance cpp-server`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`

## 추론 원칙

- `2026-03-11` 이전의 세부 구현 순서는 commit granularity로 복원하지 않는다.
- chronology는 `main.cpp`와 `Server.hpp`가 보여 주는 entrypoint, `EventManager.cpp`가 보여 주는 runtime substrate, `test_eventlab.py`가 요구하는 smoke path 순서로 재구성한다.
