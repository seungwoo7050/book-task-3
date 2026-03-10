# Game Server Capstone

앞선 네트워크 학습을 하나의 설명 가능한 서버 프로젝트로 묶는 capstone 트랙입니다.

## 이 트랙이 맡는 역할

소켓, 프로토콜, 상태 관리, persistence, 부하 검증을 한 프로젝트 안에서 동시에 설명하게 만듭니다. 학습용 저장소가 실제 포트폴리오 산출물로 이어지는 지점입니다.

## 추천 선수 지식

- 앞선 트랙에서 다룬 TCP/UDP, 신뢰 전송, 진단 도구 개념
- CMake와 C++20 빌드 흐름
- 동시성, 상태 머신, SQLite 같은 시스템 설계 키워드를 읽을 준비

## 권장 프로젝트 순서

1. [Tactical Arena Server](tactical-arena-server/README.md) - `verified`
   TCP 제어 채널, UDP 실시간 채널, authoritative simulation, SQLite persistence를 하나의 서버로 묶습니다.

## 공통 읽기 방법

- `problem/README.md`로 서버 범위와 canonical 검증 명령을 먼저 읽습니다.
- `cpp/README.md`에서 빌드 흐름과 구현 범위를 확인합니다.
- `docs/README.md`와 `docs/presentation/README.md`로 설계 근거와 발표 자료를 봅니다.
- `notion/README.md`는 설계 로그와 회고를 담은 공개 백업용 기술 노트입니다.

## 포트폴리오로 확장하기

- 이 트랙은 시연 자료가 중요합니다. `docs/presentation/README.md`와 실행 캡처를 함께 제시하세요.
- 기능 목록보다 아키텍처 결정 이유, 검증 방법, 남겨 둔 한계를 먼저 설명하는 편이 좋습니다.
- Bot demo, reconnect 흐름, DB 반영, load smoke처럼 서로 다른 품질 증거를 한 페이지에 묶어 보여 주세요.
