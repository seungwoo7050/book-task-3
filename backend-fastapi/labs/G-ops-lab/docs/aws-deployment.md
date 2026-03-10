# AWS 배포 형태 문서

이 문서는 `G-ops-lab`이 상정하는 AWS target shape를 요약한 참고 문서입니다. 실제 배포가 검증되었다는 뜻이 아니라, 로컬 학습용 백엔드를 클라우드에 옮긴다면 어떤 구성 요소가 필요할지 설명하는 수준의 문서입니다.

## 기본 가정

- compute: ECS Fargate
- image registry: ECR
- database: RDS PostgreSQL
- cache: ElastiCache Redis
- secrets: AWS Secrets Manager
- logs: CloudWatch Logs

## 이 문서의 한계

- 실제 AWS 계정에서 배포를 실행한 기록은 포함하지 않습니다.
- IaC, 비용 산정, 운영 runbook은 다루지 않습니다.
- 목적은 "어떤 조합을 상정했는가"를 설명하는 것이지 "배포가 끝났다"를 주장하는 것이 아닙니다.
