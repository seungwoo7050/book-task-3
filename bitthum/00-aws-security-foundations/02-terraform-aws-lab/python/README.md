# Python Implementation

- Scope: Terraform lab의 validate/plan/show-json 검증을 자동화한다.
- Build: `PYTHONPATH=src python -m terraform_aws_lab.verify`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: apply는 하지 않는다. v1은 plan JSON 읽기까지가 범위다.

