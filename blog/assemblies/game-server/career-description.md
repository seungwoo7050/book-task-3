# Game Server 경력기술서

## 한 줄 소개

authoritative server, TCP/UDP protocol, state machine, deterministic test를 중심으로 실시간 서버 문제를 구현하고 검증하는 게임서버 지향 개발자입니다.

## 공통 코어

- 42서울 정규과정 수료
- `minishell`, `irc`, `raytracing`는 팀 단위 보조 사례로만 사용
- `cs-core`, `network-atda`를 통한 시스템/네트워크 기반 강화

## 대표 경험

### 1. Tactical Arena Server

- TCP/UDP 혼합 authoritative tactical arena server
- reconnect, respawn, load smoke까지 포함한 capstone

### 2. arenaserv

- pure TCP 기반 상태 머신 중심 capstone
- multi-client smoke test로 세션 연속성 검증

### 3. Network / Systems Foundations

- reliable transport, proxy, routing, shell lab으로 기반 문제 별도 학습

## 기술 스택

- C++, Boost.Asio, TCP, UDP, SQLite
- CMake, CTest, smoke test, bot demo

## 검증 습관

- 기능 수보다 상태 전이와 재현 가능한 검증 경로를 더 중요하게 봅니다.

## 성장 방향

실시간 운영 환경, latency, anti-cheat, sharding 같은 더 큰 문제로 범위를 넓혀 가고 싶습니다.
