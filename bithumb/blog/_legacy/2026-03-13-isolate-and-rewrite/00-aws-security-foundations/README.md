# 00 AWS Security Foundations blog

이 트랙의 블로그는 `입력과 판단 규칙 만들기`에 해당하는 세 프로젝트를 실제 소스와 테스트 기준으로 다시 읽습니다.

## 이 트랙이 다루는 질문

- IAM policy 판단 규칙을 어디까지 구현하면 이후 least privilege 분석의 기반이 되는가
- Terraform을 배포 도구가 아니라 보안 분석 입력으로 읽으려면 어떤 경로를 고정해야 하는가
- CloudTrail과 VPC Flow Logs를 어떤 공통 이벤트 구조로 바꿔야 후속 탐지에 재사용할 수 있는가

## 프로젝트 인덱스

1. [01 AWS Security Primitives](01-aws-security-primitives/00-series-map.md)
2. [02 Terraform AWS Lab](02-terraform-aws-lab/00-series-map.md)
3. [03 CloudTrail Log Basics](03-cloudtrail-log-basics/00-series-map.md)

## 권장 읽기 순서

1. 01에서 `explicit deny > allow > implicit deny` 판단 규칙을 먼저 읽습니다.
2. 02에서 Terraform plan JSON이 어떻게 후속 규칙 엔진 입력으로 고정되는지 확인합니다.
3. 03에서 로그가 DuckDB와 Parquet로 바뀌며 queryable한 이벤트 구조가 되는 지점을 봅니다.

## 공통 검증 경로

```bash
make test-unit
make test-integration
```
