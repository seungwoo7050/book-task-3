# E-async-jobs-lab

요청-응답 API 뒤에 숨어 있는 비동기 작업 경계를 따로 떼어 보는 랩입니다. Celery와 Redis를 붙여 백그라운드 작업을 실행하되, 핵심은 outbox와 idempotency를 통해 "안전하게 넘기는 법"을 설명하는 데 있습니다.

## 이 랩에서 배우는 것

- 비동기 enqueue와 실제 실행의 분리
- outbox handoff
- idempotency key
- retry-aware 상태 전이
- Redis + Celery 로컬 실행 구조

## 선수 지식

- [D-data-api-lab](../D-data-api-lab/README.md) 수준의 데이터 계층 이해
- 메시지 큐와 worker의 기본 개념
- 실패 재시도와 중복 처리의 차이

## 구현 범위

- 알림 작업 enqueue API
- outbox 저장과 drain 흐름
- Celery worker 실행
- 재시도 가능한 상태 모델

## 일부러 단순화한 점

- 대규모 분산 메시징 대신 로컬 Redis + Celery 조합으로 제한합니다.
- 알림 도메인은 일반화된 예시로 유지합니다.

## 실행 방법

1. [problem/README.md](problem/README.md)로 비동기 작업의 성공 기준을 읽습니다.
2. [fastapi/README.md](fastapi/README.md)에서 API와 worker를 함께 띄우는 경로를 확인합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 outbox와 idempotency를 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 동기 요청과 비동기 처리의 책임 경계를 먼저 적습니다.
2. 중복 요청과 재시도 실패를 어떻게 흡수하는지 확인합니다.
3. capstone에서 어떤 이벤트를 큐로 밀어낼지 연결해 봅니다.

## 포트폴리오로 확장하려면

- dead-letter queue, 작업 모니터링 화면, 재처리 도구를 추가할 수 있습니다.
- Kafka나 SQS 같은 대체 수단으로 비교 실험을 해 볼 수 있습니다.
- 포트폴리오에서는 "왜 굳이 큐를 썼는가"와 "중복 요청을 어떻게 막았는가"가 중요한 설명 포인트입니다.
