# 문제 정리

## 문제 요약

최종 목표는 AWS-first local security control plane을 만드는 것입니다. 여러 입력을 받아 findings, exceptions, remediation plan, markdown report, audit event까지 한 흐름으로 연결합니다.

## 입력

- Terraform plan JSON
- IAM policy JSON
- CloudTrail fixture
- Kubernetes manifest

## 출력

- finding 목록
- exception 상태
- remediation dry-run plan
- markdown report
- audit events

## 학습 포인트

작은 도구를 하나의 운영 흐름으로 연결하는 데 있습니다.
