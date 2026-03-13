# Game Server 경력기술서

> 게임서버 포지션 제출용으로 정리한 프로젝트 기반 경력기술서 초안입니다.

## 한 줄 소개

authoritative server, TCP/UDP protocol, state machine, deterministic test를 중심으로 실시간 서버 문제를 구현하고 검증하는 게임서버 지향 개발자입니다.

## 핵심 역량 요약

- C++ 기반 서버 구현: Boost.Asio, socket I/O, protocol handling
- 상태 전이 설계: room queue, countdown, in-round, reconnect grace, authoritative simulation
- 네트워크 기초: reliable transport, traceroute, routing, concurrent connection 처리
- 검증 습관: multi-client smoke test, bot demo, deterministic harness, `make test` 기반 재현성

## 대표 경험 1. 현재 워크스페이스의 게임서버/네트워크 대표군

- 주요 근거:
  - [cpp-server](../../../cpp-server/README.md)
  - [network-atda](../../../network-atda/README.md)
  - [cs-core](../../../cs-core/README.md)
- 핵심 내용:
  - `arenaserv`, `Tactical Arena Server`, proxy/routing/reliable transport 프로젝트를 통해 authoritative server와 네트워크 기초를 반복적으로 구현하고 검증했습니다.
  - pure TCP capstone과 TCP/UDP 혼합 authoritative capstone을 각각 별도로 설명 가능한 구조로 정리했습니다.
- 게임서버 관점의 의미:
  - 세션, 입력, state sync, reconnect, protocol contract를 단순 개념이 아니라 테스트 가능한 결과물로 다뤘습니다.

## 대표 경험 2. 42서울 정규과정 수료

- 형태: 정규 교육 과정
- 핵심 내용:
  - 시스템 프로그래밍, 메모리 관리, 네트워크, 문제 해결 중심 과정을 수행했습니다.
- 게임서버 관점의 의미:
  - 저수준 디버깅과 시스템 이해를 바탕으로, 런타임과 성능 문제를 더 깊게 추적하는 기반을 만들었습니다.

## 대표 경험 3. mini-vrew

- 형태: 프론트엔드 단독 개발 및 배포
- 링크:
  - GitHub: <https://github.com/seungwoo7050/mini-vrew>
  - Deploy: <https://mini-vrew.vercel.app>
- 게임서버 관점의 의미:
  - 주력 경험은 아니지만, 무거운 처리 파이프라인과 사용자 경험을 끝까지 완성한 경험은 서버 개발에서도 전체 제품 흐름을 고려하는 태도로 이어졌습니다.

## 기술 스택

### 핵심 스택

- C++
- Boost.Asio
- TCP / UDP
- SQLite
- Linux
- CMake / CTest
- state machine
- deterministic test / smoke test

### 보조 이해

- process / signal / concurrent I/O
- reliable transport / routing / traceroute
- Go/FastAPI 기반 서버 운영성 및 비동기 처리 기초

## 검증과 재현 습관

- 게임서버 성격의 프로젝트는 bot demo, smoke test, integration harness를 함께 둡니다.
- 프로토콜과 상태 전이는 README와 테스트 경로에서 바로 확인할 수 있게 정리합니다.
- 기능 수보다 authoritative state와 세션 연속성을 어디까지 증명했는지를 더 중요하게 생각합니다.

## 성장 방향

- 실무에서는 더 복잡한 동시성, latency, 운영 환경, anti-cheat, sharding 문제를 경험하며 실시간 서버 역량을 넓히고 싶습니다.
- 장기적으로는 게임 로직과 네트워크 조건을 함께 이해하고, 안정적인 authoritative server 구조를 설계할 수 있는 엔지니어로 성장하고 싶습니다.
