# Roadmap

이 레포의 순서는 `AWS를 이해하는 기초 -> 보안 도구를 만드는 코어 -> 하나의 control plane으로 통합`
으로 고정한다.

## 00 AWS Security Foundations

- `01-aws-security-primitives`: IAM 정책이 실제로 어떻게 평가되는지 코드로 익힌다.
- `02-terraform-aws-lab`: 안전한 설정과 위험한 설정을 Terraform으로 비교한다.
- `03-cloudtrail-log-basics`: CloudTrail/VPC Flow Logs를 정규화하고 기본 분석을 수행한다.

## 01 Cloud Security Core

- `04-iam-policy-analyzer`: least privilege 관점의 finding을 생성한다.
- `05-cspm-rule-engine`: misconfiguration 탐지 규칙 엔진을 구현한다.
- `06-remediation-pack-runner`: dry-run 중심의 조치 패키지를 만든다.
- `07-security-lake-mini`: 보안 로그를 Parquet + DuckDB로 적재하고 탐지한다.
- `08-container-guardrails`: Kubernetes manifest와 이미지 메타데이터를 점검한다.
- `09-exception-and-evidence-manager`: 거버넌스/예외/증적 흐름을 모델링한다.

## 02 Capstone

- `10-cloud-security-control-plane`: Terraform plan, IAM policy, CloudTrail logs, Kubernetes
  manifests를 하나의 상태 저장소와 report 흐름으로 통합한다.

