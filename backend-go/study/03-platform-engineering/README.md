# 03 Platform Engineering

## 이 트랙이 푸는 문제

- 정합성, 이벤트 파이프라인, 배포 자산은 백엔드 코드와 운영 자산의 경계에서 이해해야 하는데 학습 레포에서 종종 분리돼 보인다.

## 이 트랙의 답

- 트랜잭션 재시도, outbox relay, GitOps 배포 자산을 각각 재현 가능한 프로젝트로 분리했다.

## 프로젝트 순서

1. [14-cockroach-tx](14-cockroach-tx/README.md) : idempotency key, optimistic locking, transaction retry를 CockroachDB 호환 흐름으로 묶어 정합성 기초를 다지는 과제다.
2. [15-event-pipeline](15-event-pipeline/README.md) : outbox pattern, relay, idempotent consumer를 통해 DB 정합성과 비동기 전달 경계를 함께 다루는 대표 과제다.
3. [16-gitops-deploy](16-gitops-deploy/README.md) : Docker multi-stage build, Helm chart, ArgoCD manifest를 통해 코드 자산을 배포 자산으로 번역하는 인프라 과제다.

## 졸업 기준

- idempotency, transaction retry, outbox, Helm/ArgoCD의 목적과 trade-off를 서로 연결해 설명할 수 있어야 한다.
- 코드 자산과 배포 자산이 어디에서 만나는지 README와 검증 명령 기준으로 보여줄 수 있어야 한다.

## 대표 프로젝트

- [15-event-pipeline](15-event-pipeline/README.md) : 플랫폼 과제 중 정합성과 비동기 경계를 가장 잘 드러내는 대표작이다.
