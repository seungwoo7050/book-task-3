# 02-terraform-aws-lab-python 문제지

## 왜 중요한가

Terraform을 배포 성공 여부가 아니라 보안 분석 입력으로 읽는 실습입니다. insecure 설정과 secure 설정을 plan JSON 기준으로 비교해, 다음 프로젝트가 읽을 입력 구조를 먼저 고정해야 합니다.

## 목표

시작 위치의 구현을 완성해 실제 terraform apply는 하지 않습니다와 AWS 계정 없이 로컬에서 plan JSON을 재현하는 데 집중합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/__init__.py`
- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py`
- `../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py`
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf`
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/secure/main.tf`

## starter code / 입력 계약

- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 실제 terraform apply는 하지 않습니다.
- AWS 계정 없이 로컬에서 plan JSON을 재현하는 데 집중합니다.

## 제외 범위

- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `terraform_available`와 `run_lab`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `_project_root`와 `test_default_labs_root_points_to_project_terraform_dir`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-terraform-aws-lab-python_answer.md`](02-terraform-aws-lab-python_answer.md)에서 확인한다.
