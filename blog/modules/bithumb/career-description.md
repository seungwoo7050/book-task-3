# Bithumb 경력기술서 Module

## 한 줄 소개

보안 판단 로직을 API, worker, finding, exception, remediation, report 흐름으로 통합하는 local control plane 구현 경험을 갖고 있습니다.

## 핵심 역량

- cloud security finding 파이프라인
- exception / remediation / audit 연결
- PostgreSQL + SQLite fallback 기반 로컬 재현성

## 대표 경험

### 1. Cloud Security Control Plane

- Terraform, IAM, CloudTrail, Kubernetes 입력을 공통 finding 흐름으로 통합
- report와 remediation dry-run까지 한 서비스 표면에 연결

### 2. Cloud Security Core 트랙

- IAM analyzer, CSPM rule engine, exception manager를 개별 프로젝트로 학습한 뒤 capstone에 재통합

## 검증 습관

- `make test-capstone`, `make demo-capstone` 같은 canonical 명령을 문서 앞단에 둡니다.

## 성장 방향

보안 판단 로직을 더 큰 운영 환경과 팀 워크플로우에 맞게 확장하는 방향으로 깊이를 더하고 싶습니다.
