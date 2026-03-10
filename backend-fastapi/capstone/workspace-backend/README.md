# workspace-backend

이 프로젝트는 capstone v1 기준선입니다. 앞선 랩을 하나의 단일 FastAPI 백엔드로 다시 조합한 버전이며, 이후 `workspace-backend-v2-msa`와 비교할 때 기준이 되는 구조입니다.

이 capstone은 앞선 FastAPI 랩을 하나의 협업형 SaaS 백엔드로 다시 조합한 프로젝트입니다. 랩에서 따로 익힌 인증, 인가, 데이터 API, 비동기 작업, 실시간 전달을 한 구조 안에서 어떻게 통합하는지 보여 줍니다.

## 이 랩에서 배우는 것

- 인증과 인가를 제품형 워크스페이스 도메인에 묶는 방법
- 프로젝트, 태스크, 댓글을 중심으로 한 협업 API 구조
- queued notification과 realtime delivery의 결합
- 작은 랩의 패턴을 통합 설계로 재해석하는 방법

## 선수 지식

- `labs/A`부터 `labs/G`까지의 핵심 개념
- FastAPI 서비스 계층, SQLAlchemy, Redis, WebSocket의 기본
- 작은 예제를 제품 구조로 확장할 때 생기는 경계 문제

## 구현 범위

- 로컬 로그인과 Google 스타일 로그인
- 워크스페이스 멤버십과 초대
- 프로젝트, 태스크, 댓글 API
- 알림 큐와 실시간 전달
- health endpoint

## 일부러 단순화한 점

- 랩 코드를 공용 패키지로 묶지 않고 다시 구현합니다.
- 프런트엔드, 정적 자산, 실제 클라우드 인프라는 제외합니다.

## 실행 방법

1. [problem/README.md](problem/README.md)에서 통합 범위를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)를 따라 워크스페이스를 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 통합 설계 의도를 복습합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 개별 랩에서 익힌 경계를 먼저 떠올립니다.
2. capstone에서 어떤 개념을 다시 조합했는지 비교합니다.
3. "왜 import 대신 재구성했는가"를 스스로 설명해 봅니다.

## 포트폴리오로 확장하려면

- 멀티테넌시, 이벤트 로그, 관리자용 운영 화면을 추가할 수 있습니다.
- 제품 도메인을 자신만의 문제로 바꾸고 랩에서 익힌 경계를 재배치해 볼 수 있습니다.
- 통합 프로젝트 README에는 기능 수보다도 경계, 검증 수준, 운영 가정을 더 선명하게 적는 것이 좋습니다.
- 같은 도메인을 MSA로 다시 쪼개 보고 싶다면 `../workspace-backend-v2-msa/README.md`와 비교하며 어떤 복잡성이 새로 생기는지 기록합니다.
