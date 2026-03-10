# 문제 프레이밍

## 학습 목표

v2의 목표는 서비스를 많이 늘리는 것이 아니라, v1에서 한 프로세스 안에 있던 경계를 서비스 수준으로 다시 드러내는 것이다. 같은 협업형 도메인을 유지해야 v1과 v2의 차이가 기능이 아니라 아키텍처에서 왔다는 점을 설명할 수 있다.

## 왜 중요한가

- v1은 모듈 경계가 있는 단일 FastAPI 백엔드로서 충분히 교육적이다.
- 하지만 MSA를 배우려면 “왜 이 책임을 다른 프로세스로 밀어냈는가”를 코드와 문서로 같이 보여 줘야 한다.
- 같은 도메인을 다시 분해해야만 v1과 v2의 차이를 정직하게 비교할 수 있다.

## 핵심 성공 조건

- public API는 gateway가 유지해야 한다.
- 각 서비스는 자기 DB만 읽어야 한다.
- comment 생성은 outbox와 stream consumer를 거쳐 websocket 전달로 이어져야 한다.
- notification-service 장애가 comment 생성 트랜잭션을 깨지 않아야 한다.

## 선수 지식

- `labs/A`부터 `labs/G`까지의 핵심 개념
- H, I, J, K 랩에서 정리한 service boundary, event integration, edge gateway, distributed ops
- FastAPI, SQLAlchemy, Redis, WebSocket, Docker Compose 기본

## 일부러 제외한 범위

- Kubernetes, service mesh, IaC
- 실제 클라우드 배포 완료 주장
- 고급 retry policy, contract registry, distributed tracing backend

## 이 capstone이 답하려는 질문

- v1에서 자연스러웠던 경계는 v2에서 어디까지 유지되고 어디서 깨지는가
- gateway, outbox, consumer, pub/sub가 한 도메인 흐름 안에서 왜 동시에 필요한가
- 학습 저장소에서 “설명 가능한 MSA”는 어디까지를 목표로 삼아야 하는가

이번 범위에서는 Compose에서 다시 실행 가능하고, 실패 지점을 숨기지 않으며, 문서와 코드가 같은 이야기를 하도록 만드는 것을 우선한다.
