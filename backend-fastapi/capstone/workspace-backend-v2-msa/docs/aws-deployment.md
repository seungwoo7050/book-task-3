# AWS 배포 형태 문서

이 문서는 `workspace-backend-v2-msa`가 상정하는 AWS target shape를 설명한다. 실제 배포 완료를 주장하지 않으며, 로컬 Compose 기반 학습 스택을 클라우드로 옮긴다면 어떤 조합이 필요한지 정리하는 수준에 머문다.

## target shape

- edge: ALB
- public API: ECS Fargate `gateway`
- internal services: ECS Fargate `identity-service`, `workspace-service`, `notification-service`
- database: 서비스별 RDS PostgreSQL 또는 분리된 스키마를 가진 RDS 인스턴스
- event / cache: ElastiCache for Redis
- secrets: AWS Secrets Manager

## 로컬 구조와의 대응 관계

- Compose의 `gateway` 컨테이너는 ALB 뒤의 public ECS service로 대응한다.
- Compose의 세 내부 서비스는 개별 ECS service로 대응한다.
- SQLite 학습 DB는 실제 target shape에서 RDS PostgreSQL로 바뀐다.
- Redis Streams와 pub/sub 실습은 ElastiCache for Redis로 대응한다.

## 이 문서가 일부러 답하지 않는 것

- 실제 VPC, subnet, security group 세부 설정
- autoscaling 정책과 비용 추정
- IaC 코드 존재 여부
- blue/green deployment, canary release, service mesh

## 이 문서가 보장하지 않는 것

- 실제 AWS 계정에서의 배포 성공
- 장애 복구 실험이나 성능 튜닝
- 운영 팀 수준의 보안 검토 완료

## 문서 사용 원칙

- 이 문서는 “어떤 배치를 상정했는가”를 설명하는 참고 자료다.
- verification report가 실제 실행 증거를 대신하지 않는다.
- 학습 저장소에서는 target shape와 검증 완료 주장을 절대 섞지 않는다.
