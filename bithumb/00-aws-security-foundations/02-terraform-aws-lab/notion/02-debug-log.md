# 디버그 로그

## 실제로 자주 막히는 지점

- `terraform plan`에서 AWS API를 치지 않게 하려면 provider skip 옵션과 `-refresh=false`가 함께 필요합니다.
- Terraform이 설치되어 있지 않으면 이 프로젝트 테스트는 자동으로 skip됩니다. 따라서 실패와 skip을 구분해서 읽어야 합니다.
- plan JSON을 봤을 때 `planned_values.root_module.resources` 경로를 먼저 확인하지 않으면 뒤 프로젝트와 연결이 끊깁니다.

## 이미 확인된 테스트 시나리오

- `test_insecure_lab_generates_plan_json`: insecure 예제가 S3 버킷과 Security Group 리소스를 실제로 포함하는지 확인합니다.
- `test_secure_lab_generates_plan_json`: secure 예제가 public access block과 IAM policy 리소스를 생성하는지 확인합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_terraform_lab.py](../python/tests/test_terraform_lab.py)
- 검증 스크립트: [../python/src/terraform_aws_lab/verify.py](../python/src/terraform_aws_lab/verify.py)
- 이전 재현 기록: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
