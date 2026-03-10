# AWS 배포 형태 문서

이 문서는 `K-distributed-ops-lab`이 상정하는 AWS target shape를 요약한다. 실제 배포를 검증했다는 뜻은 아니다. 목표는 “분산 구조를 클라우드에 옮긴다면 어떤 구성 조합이 필요할까”를 운영성 관점에서 설명하는 데 있다.

## target shape

- edge: ALB
- compute: ECS Fargate
- data: RDS PostgreSQL
- event/cache: ElastiCache for Redis
- secrets: AWS Secrets Manager

## 이 문서를 읽을 때의 기준

- 이것은 배치 가정 문서이지, 배포 완료 보고서가 아니다.
- health, logs, metrics가 어떤 식으로 분산 서비스에 매핑될지 생각하는 참고 자료다.
- 실제 VPC 설계, autoscaling, 장애 복구 실험은 이 문서 범위 밖이다.

## 이 문서가 보장하지 않는 것

- 실제 AWS 계정에서의 실행 성공
- IaC 코드 존재
- 비용, 보안, 성능 최적화 검증
