# C-authorization-lab

인증이 끝난 뒤 "누가 무엇을 할 수 있는가"를 분리해서 다루는 랩입니다. 워크스페이스, 초대, 역할, 소유권을 중심으로 인가 규칙을 서비스 계층에서 어떻게 설명할지 연습합니다.

## 이 랩에서 배우는 것

- workspace membership 모델
- invitation 생성, 수락, 거절 흐름
- RBAC 역할 경계
- owner와 member의 권한 차이
- 인가 규칙을 HTTP 계층 밖에서 설명하는 방법

## 선수 지식

- 사용자와 리소스 관계를 데이터 모델로 표현하는 기본기
- FastAPI request/response 흐름
- 역할 기반 접근 제어 개념

## 구현 범위

- 워크스페이스 생성
- 초대 발행과 응답
- 역할 변경
- 문서/리소스 접근 제어

## 일부러 단순화한 점

- 인증은 별도 헤더 기반 actor 모델로 단순화합니다.
- 핵심은 "누가 할 수 있나"이지 "어떻게 로그인했나"가 아닙니다.

## 실행 방법

1. [problem/README.md](problem/README.md)에서 인가 규칙 문제를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)로 워크스페이스를 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 역할 경계를 복습합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 역할과 소유권을 표로 먼저 정리합니다.
2. 서비스 계층이 어떤 체크를 담당하는지 코드와 문서를 같이 봅니다.
3. capstone에서 이 규칙을 어떻게 다시 합칠지 메모합니다.

## 포트폴리오로 확장하려면

- 리소스별 세분화 권한이나 정책 엔진 연동으로 확장할 수 있습니다.
- 감사 로그와 관리자 승인 흐름을 붙이면 협업형 제품 설명이 더 탄탄해집니다.
- 자신의 포트폴리오에서는 권한 정책 표와 예외 사례를 README에 함께 넣는 것이 좋습니다.
