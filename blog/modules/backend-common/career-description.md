# Backend Common 경력기술서 Module

## 한 줄 소개

FastAPI 기반 학습 트랙을 통해 인증/인가, API 경계, 비동기 처리, 운영성까지 하나의 백엔드 기준선으로 반복 구현했습니다.

## 핵심 역량

- 서비스 경계 설계: gateway와 내부 서비스 분리
- 데이터 흐름 설계: service별 DB ownership, event payload, eventually consistent flow
- 재현 가능한 검증: `make lint`, `make test`, `make smoke`, compose runtime

## 대표 경험

### 1. workspace-backend

- 협업형 도메인을 단일 FastAPI 서비스로 구현했습니다.
- 인증, 워크스페이스 도메인, 알림을 한 프로세스에서 통합해 제품형 기준선을 만들었습니다.

### 2. workspace-backend-v2-msa

- gateway, identity, workspace, notification 서비스를 나누고 public route shape는 유지했습니다.
- outbox, Redis Streams consumer, websocket fan-out을 통해 비동기 알림 경계를 설명 가능한 결과물로 남겼습니다.

## 검증 습관

- verification report를 따로 남겨 실제 재실행 결과만 기록합니다.
- smoke와 health check를 문서의 핵심 근거로 둡니다.

## 성장 방향

이 모듈은 모든 백엔드 가지의 공통 바닥입니다. 이후 제출본에서는 Go, Node, Spring의 주력 결과물 위에 이 경험을 덧붙여 공통 백엔드 감각을 보여 줍니다.
