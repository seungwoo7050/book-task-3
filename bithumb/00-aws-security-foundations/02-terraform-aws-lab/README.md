# 02 Terraform AWS Lab

## Status

`verified`

## Problem Scope

- Terraform으로 AWS 리소스 기본 구조 읽기
- insecure/secure 설정 비교
- `terraform validate`, `plan`, `show -json`을 직접 돌려 보기

## Build

```bash
cd terraform/insecure
terraform init -backend=false
terraform validate
terraform plan -refresh=false -out=tfplan
terraform show -json tfplan > tfplan.json
```

## Test

```bash
cd study2
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## Learned

리소스 이름을 아는 것과 plan JSON을 읽을 수 있는 것은 다르다. 뒤 CSPM 과제를 위해
Terraform이 어떤 구조로 planned values를 내놓는지 먼저 익힌다.
