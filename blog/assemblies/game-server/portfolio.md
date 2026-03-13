# Game Server Portfolio

> PDF/Notion 제출용 조립본입니다. 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Game Server Engineer |
| 한 줄 포지셔닝 | authoritative state, protocol, state machine, deterministic test를 중심으로 실시간 서버 문제를 설명 가능한 형태로 구현하는 개발자 |
| 핵심 스택 | C++, Boost.Asio, TCP, UDP, SQLite, Linux, deterministic test |
| 대표 프로젝트 | `Tactical Arena Server`, `arenaserv`, `Network & Systems Foundations` |
| 링크 | [cpp-server](../../../cpp-server/README.md) · [network-atda](../../../network-atda/README.md) · [cs-core](../../../cs-core/README.md) |

## 공통 코어 요약

- 42서울 정규과정과 공통 코어 프로젝트로 시스템/네트워크 기반을 다졌습니다.
- `minishell`, `irc`, `raytracing`은 시스템 기초와 팀 협업 경험을 보여 주는 보조 사례로만 사용합니다.
- `ft_transcendence`는 42의 유일한 상세 사례이지만, 게임서버 제출본에서는 공통 코어 배경으로만 짧게 유지합니다.

## 대표 프로젝트 1. Tactical Arena Server

`C++20 + Boost.Asio + SQLite + CMake/CTest` 기반의 authoritative tactical arena server입니다. line-based TCP control protocol과 binary UDP packet을 함께 설계하고, reconnect, fixed tick, respawn, load smoke를 설명 가능한 구조로 정리했습니다.

![tactical arena bot demo](../../assets/captures/game-server/tactical-arena-bot-demo.png)

## 대표 프로젝트 2. arenaserv

pure TCP capstone으로, room queue, countdown, in-round, reconnect grace를 하나의 상태 머신으로 묶었습니다. 화려한 기능보다 authoritative 상태와 세션 연속성 검증에 집중했습니다.

![arenaserv evidence](../../assets/captures/game-server/arenaserv-evidence.png)

## 대표 프로젝트 3. Network & Systems Foundations

`network-atda`와 `cs-core`에서 reliable transport, routing, proxy, shell, runtime 문제를 별도 결과물로 학습했습니다. 게임서버 capstone만이 아니라 그 기반 학습까지 함께 설명할 수 있다는 점을 보조 근거로 사용합니다.

## 마무리

이 제출본은 게임서버를 웹 백엔드의 다른 이름으로 보지 않고, authoritative state와 네트워크 조건을 함께 다루는 별도 문제로 접근해 온 결과물을 보여 줍니다. 프로토콜, 상태 전이, 검증 하네스를 함께 설명할 수 있다는 점이 핵심입니다.
