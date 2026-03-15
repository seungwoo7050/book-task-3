# 02-terraform-aws-lab-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 실제 terraform apply는 하지 않습니다와 AWS 계정 없이 로컬에서 plan JSON을 재현하는 데 집중합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `terraform_available`와 `run_lab`, `default_labs_root` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 실제 terraform apply는 하지 않습니다.
- AWS 계정 없이 로컬에서 plan JSON을 재현하는 데 집중합니다.
- 첫 진입점은 `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/__init__.py`이고, 여기서 `terraform_available`와 `run_lab` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.
- 검증 기준은 `_project_root`와 `test_default_labs_root_points_to_project_terraform_dir` 테스트가 먼저 잠근 동작부터 맞추는 것이다.

## 코드 워크스루

- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py`: `terraform_available`, `run_lab`, `default_labs_root`가 핵심 흐름과 상태 전이를 묶는다.
- `../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py`: `_project_root`, `test_default_labs_root_points_to_project_terraform_dir`, `test_insecure_lab_generates_plan_json`가 통과 조건과 회귀 포인트를 잠근다.
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf`: 핵심 구현을 담는 파일이다.
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/secure/main.tf`: 핵심 구현을 담는 파일이다.
- `terraform_available` 구현은 `_project_root` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf` 등을 함께 읽어 입력 fixture나 trace를 추측이 아니라 근거로 고정한다.

## 정답을 재구성하는 절차

1. `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `_project_root` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `_project_root`와 `test_default_labs_root_points_to_project_terraform_dir`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/__init__.py`
- `../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py`
- `../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py`
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf`
- `../00-aws-security-foundations/02-terraform-aws-lab/terraform/secure/main.tf`
