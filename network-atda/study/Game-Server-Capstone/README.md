# Game Server Capstone

기존 네트워크 학습을 채용용 산출물 하나로 묶는 capstone 트랙이다.

## 왜 이 트랙인가

이 저장소의 기존 과제들은 프로토콜과 진단 도구를 잘게 나눠 학습하게 만들지만, 실제 서버 설계 판단을 한 프로젝트에서 설명하는 단계는 비어 있었다. 이 트랙은 그 공백을 메우기 위해 추가했다.

## 프로젝트 순서

1. [Tactical Arena Server](tactical-arena-server/README.md) - `verified`
   핵심: TCP 제어 채널, UDP 실시간 채널, fixed tick simulation, reconnect, SQLite persistence, bot/load smoke를 한 C++ 서버로 묶는다.

## 공통 규칙

- `problem/`은 공개 사양과 canonical 검증 래퍼만 둔다.
- `cpp/`는 빌드 가능한 공개 구현과 테스트만 둔다.
- `docs/`는 오래 남길 개념 문서와 load report만 유지한다.
- `notion/`은 Notion 업로드용 기술 노트이며 Git 공개 구조에 의존하지 않는다.
