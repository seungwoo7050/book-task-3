# I-event-integration-lab

동기 API 경계를 서비스 간 이벤트 통합으로 확장하는 랩입니다. `workspace-service`의 outbox와 `notification-service`의 idempotent consumer를 붙여 eventual consistency를 설명하는 데 집중합니다.

## 이 랩에서 배우는 것

- outbox handoff를 서비스 경계로 옮기는 방법
- Redis Streams 기반 이벤트 전달
- idempotent consumer와 중복 흡수
- `comment.created.v1` 계약 설명

## 선수 지식

- [H-service-boundary-lab](../H-service-boundary-lab/README.md) 수준의 서비스 분리
- [E-async-jobs-lab](../E-async-jobs-lab/README.md) 수준의 outbox 개념

## 구현 범위

- workspace outbox 적재
- Redis Streams relay
- notification consume와 dedupe

## 일부러 단순화한 점

- consumer group 대신 단순 consumer 흐름으로 제한합니다.
- dead-letter queue와 재처리 UI는 범위 밖입니다.

## 실행 방법

1. [problem/README.md](problem/README.md)로 이벤트 계약을 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 workspace와 notification stack을 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 eventual consistency를 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 댓글 생성 시점과 알림 전달 시점을 분리해 적습니다.
2. `comment.created.v1` payload를 읽습니다.
3. consume를 두 번 실행해도 왜 중복이 생기지 않는지 확인합니다.

## 포트폴리오로 확장하려면

- consumer group, retry policy, replay 도구를 추가할 수 있습니다.
- 계약 버전 업 전략을 같이 적으면 좋습니다.
