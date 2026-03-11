# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- insecure/secure Terraform 예제를 비교합니다.
- plan JSON을 생성하고 후속 프로젝트에서 재사용할 입력 형태를 정리합니다.
- AWS 계정 없이도 로컬 검증 중심으로 실습합니다.

## 핵심 엔트리포인트

- `python/src/terraform_aws_lab/verify.py`
- `terraform/insecure/main.tf`
- `terraform/secure/main.tf`

## 실행

```bash
make venv
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
```

## 테스트

```bash
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## 대표 출력 예시

```text
insecure: 5 resources
secure: 5 resources
```

## 구현 메모

검증 스크립트는 Terraform 결과를 후속 프로젝트에서 재사용할 수 있는 입력으로 정리하는 데 초점을 둡니다.
