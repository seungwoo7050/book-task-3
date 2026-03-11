# 02 Terraform AWS Lab

## 풀려는 문제

Terraform을 단순 배포 도구가 아니라, 이후 보안 규칙 엔진이 읽을 선언형 입력으로 다뤄야 합니다.
이 프로젝트는 apply 없이도 insecure 설정과 secure 설정의 차이를 보안 분석 관점으로 설명할 수 있게 만드는 단계입니다.

## 내가 낸 답

- `terraform/insecure`와 `terraform/secure` 실습 쌍을 유지해 설정 차이를 비교합니다.
- `terraform init -> validate -> plan -> show -json` 흐름을 스크립트로 고정합니다.
- plan JSON을 후속 프로젝트가 바로 재사용할 수 있는 입력 형태로 남깁니다.
- AWS 계정 없이도 로컬 검증만으로 반복 학습할 수 있게 제한합니다.

## 입력과 출력

- 입력: `terraform/insecure/main.tf`, `terraform/secure/main.tf`
- 출력: lab별 `tfplan.json`과 resource count 요약

## 검증 방법

```bash
make venv
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## 현재 상태

- `verified`
- Terraform CLI가 있으면 insecure/secure plan 생성 경로를 바로 재현할 수 있습니다.
- 05번 CSPM rule engine이 이 프로젝트의 plan JSON 감각을 전제로 합니다.

## 한계와 다음 단계

- 실제 `terraform apply`는 하지 않습니다.
- plan을 해석하는 규칙 엔진 자체는 05번 프로젝트에서 따로 구현합니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [notion/README.md](notion/README.md)
