# Game Server Portfolio

> PDF/Notion 제출용으로 정리한 게임서버 포지션 제출본입니다.  
> 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Game Server Engineer |
| 한 줄 포지셔닝 | authoritative server, socket/network protocol, state machine, deterministic test를 중심으로 실시간 서버 문제를 설명 가능한 형태로 구현하는 개발자 |
| 핵심 스택 | C++, Boost.Asio, TCP/UDP, SQLite, Linux, deterministic test, state machine |
| 대표 프로젝트 | `Tactical Arena Server`, `arenaserv`, `Network & Systems Foundations` |
| 링크 | [cpp-server](../../../cpp-server/README.md) · [network-atda](../../../network-atda/README.md) · [cs-core](../../../cs-core/README.md) |
| 핵심 검증 | `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test` · `cd cpp && make clean && make test` |

## 대표 프로젝트 1. Tactical Arena Server

프로젝트: [Tactical Arena Server](../../../network-atda/study/05-Game-Server-Capstone/tactical-arena-server/README.md)

**문제**  
이전 네트워크 학습에서 익힌 TCP/UDP, 신뢰 전송, deterministic test 패턴을 하나의 설명 가능한 authoritative arena server로 통합해야 했습니다.

**내가 한 일**  
`C++20 + Boost.Asio + SQLite + CMake/CTest` 기반으로 2~4인 authoritative tactical arena server를 구현했습니다. line-based TCP control protocol과 binary UDP packet을 함께 설계하고, reconnect window, forfeit, fixed tick, respawn 같은 게임 서버 상태 전이를 하나의 서버 구조에 담았습니다.

**검증**  
`run-server`, `run-bot-demo`, `load-test`, `test` 명령을 통해 bot demo와 load smoke를 포함한 검증 경로를 유지했습니다.

**왜 이 역할에 맞는가**  
authoritative state, protocol 설계, deterministic harness, reconnect/ordering 문제를 모두 텍스트와 테스트로 설명할 수 있다는 점이 게임서버 직군과 가장 직접적으로 맞닿아 있습니다.

## 대표 프로젝트 2. arenaserv

프로젝트: [arenaserv](../../../cpp-server/study/game-track/02-arenaserv/README.md)

**문제**  
화려한 기능보다 authoritative 상태와 세션 연속성을 어디까지 설계하고 검증했는지 보여 주는 pure TCP capstone이 필요했습니다.

**내가 한 일**  
`HELLO`, `QUEUE`, `READY`, `INPUT`, `REJOIN`, `LEAVE`를 처리하는 pure TCP 서버를 구현하고, room queue, countdown, in-round, finished를 하나의 상태 머신으로 묶었습니다. snapshot, hit, elimination, round end, reconnect grace를 multi-client smoke test로 검증했습니다.

**검증**  
`cd cpp && make clean && make test` 기준으로 verified 상태를 유지합니다.

**왜 이 역할에 맞는가**  
세션, 입력, 상태 전이, reconnect grace 같은 실시간 서버 핵심 문제를 네트워크와 state machine 관점에서 정리했다는 점이 강한 근거가 됩니다.

## 대표 프로젝트 3. Network & Systems Foundations

근거 프로젝트:

- [Proxy Lab](../../../cs-core/study/Systems-Programming/proxylab/README.md)
- [Shell Lab](../../../cs-core/study/Systems-Programming/shlab/README.md)
- [RDT Protocol / Traceroute / Routing](../../../network-atda/README.md)

**문제**  
게임서버 구현 전에 socket I/O, concurrent connection, process/signal, reliable transport, routing 같은 기반 문제를 별도 단위로 체득할 필요가 있었습니다.

**내가 한 일**  
HTTP proxy, tiny shell, reliable transport, traceroute, routing 프로젝트를 각각 구현하고 검증했습니다. 이를 통해 socket I/O, concurrency hazard, race discipline, protocol reasoning을 별도 문제로 연습했습니다.

**검증**  
각 프로젝트가 `make test` 또는 단계별 문제 검증 명령을 유지하며 public verified 상태로 정리되어 있습니다.

**왜 이 역할에 맞는가**  
게임서버는 결국 네트워크와 시스템 기초 위에 서 있기 때문에, 저는 capstone만 보여 주는 대신 그 기반 학습까지 함께 설명할 수 있습니다.

## 보조 프로젝트와 학습 아카이브

| 영역 | 근거 | 게임서버 관점에서 의미 |
| --- | --- | --- |
| 42서울 | [42서울](https://42.fr/en/homepage/) | 시스템 프로그래밍, 메모리, 네트워크, 디버깅 기초 |
| 시스템 프로그래밍 | [cs-core](../../../cs-core/README.md) | process group, signal, concurrent proxy, allocator 등 런타임 감각 강화 |
| 서버 구조 비교 | [backend-go](../../../backend-go/README.md), [backend-fastapi](../../../backend-fastapi/README.md) | 운영성, 비동기 처리, smoke/demo 경로를 서버 도구 관점에서 보조 학습 |

## 검증 근거

```bash
# authoritative tactical arena server
make -C network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem test
make -C network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem run-bot-demo
make -C network-atda/study/05-Game-Server-Capstone/tactical-arena-server/problem load-test
```

```bash
# pure TCP capstone
cd cpp-server/study/game-track/02-arenaserv/cpp
make clean && make test
```

게임서버 포지션에서는 화면보다 테스트 하네스와 상태 전이를 어떻게 검증했는지가 더 중요하다고 생각합니다. 그래서 이 버전의 포트폴리오는 시각 자료 대신 protocol, state machine, smoke test, bot demo 중심으로 정리했습니다.

## 마무리 요약

저는 게임서버를 "웹 백엔드의 다른 이름"으로 보지 않고, authoritative state와 네트워크 조건을 함께 다뤄야 하는 별도 문제로 받아들이고 있습니다. `Tactical Arena Server`와 `arenaserv`는 실시간 입력, reconnect, state transition을 직접 다룬 결과물이고, `network-atda`와 `cs-core`는 그 기반을 이루는 네트워크/시스템 학습을 보여 줍니다. 게임서버 포지션에서는 이 조합이 제가 C++, 네트워크, 상태 머신을 중심으로 문제를 설명 가능한 형태로 구현해 온 개발자라는 점을 가장 잘 보여 준다고 생각합니다.
