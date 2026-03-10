# 문제 프레이밍

## 학습 목표

K 랩의 목표는 “다중 서비스도 운영 질문에 답할 수 있어야 한다”는 감각을 만드는 것이다. 따라서 기능 추가보다 live/ready, metrics, JSON 로그, target shape 문서가 먼저 나온다.

## 왜 중요한가

- 서비스가 네 개로 늘어나는 순간 “돌아간다”는 말만으로는 상태를 설명할 수 없다.
- 어떤 서비스가 살아 있고, 어떤 서비스가 준비됐고, 어떤 요청이 어디서 실패했는지를 말할 수 있어야 운영성이 생긴다.
- 학습 레포에서도 이 질문에 답하지 못하면 구조만 복잡한 데모에 머물기 쉽다.

## 선수 지식

- J 랩의 gateway와 internal service 구조
- health check, readiness, request id의 기본 개념
- Docker Compose와 서비스 healthcheck 기본

## 성공 기준

- 각 서비스의 `/health/live`, `/health/ready`를 따로 설명할 수 있어야 한다.
- JSON 로그와 metrics가 최소한의 운영 질문에 답해야 한다.
- Compose health matrix가 실제 부팅 순서를 설명해야 한다.
- AWS 문서는 `ECS Fargate + ALB + RDS + ElastiCache + Secrets Manager` target shape로만 서술돼야 한다.

## 일부러 제외한 범위

- full observability stack
- tracing backend와 dashboards
- IaC와 실제 AWS 배포 완료 주장

## 이 랩이 답하려는 질문

- 분산 구조에서 “프로세스가 산다”와 “요청을 받을 준비가 됐다”는 어떻게 다른가
- request id와 metrics는 어디까지가 최소선인가
- 학습 저장소에서 운영 문서는 어느 수준까지 사실이라고 말할 수 있는가
