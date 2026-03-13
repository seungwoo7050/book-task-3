# 02 Terraform AWS Lab - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `verify.py`, `terraform/`, `test_terraform_lab.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- Terraform을 배포 도구가 아니라 보안 분석 입력으로 읽으려면 어디까지의 실행 경로를 고정해야 할까
- insecure/secure 예제를 plan JSON 수준에서 비교 가능하게 만들려면 무엇이 필요할까

## 실제 구현 표면

- `terraform init -> validate -> plan -> show -json` 순서를 `run_lab()` 하나로 고정합니다.
- insecure lab과 secure lab 모두 `tfplan.json`을 생성해 후속 프로젝트가 직접 읽을 수 있게 만듭니다.
- AWS 계정 없이도 plan 생성이 가능하도록 더미 환경 변수를 주입합니다.

## 대표 검증 엔트리

- `PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify`
- `PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../00-aws-security-foundations/02-terraform-aws-lab/README.md)
2. [문제 정의](../../../00-aws-security-foundations/02-terraform-aws-lab/problem/README.md)
3. [실행 진입점](../../../00-aws-security-foundations/02-terraform-aws-lab/python/README.md)
4. [대표 테스트](../../../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py)
5. [핵심 구현](../../../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py)
6. [Terraform 입력](../../../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf)
7. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../00-aws-security-foundations/02-terraform-aws-lab/README.md)
- [problem/README.md](../../../00-aws-security-foundations/02-terraform-aws-lab/problem/README.md)
- [python/README.md](../../../00-aws-security-foundations/02-terraform-aws-lab/python/README.md)
- [verify.py](../../../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py)
- [terraform/insecure/main.tf](../../../00-aws-security-foundations/02-terraform-aws-lab/terraform/insecure/main.tf)
- [terraform/secure/main.tf](../../../00-aws-security-foundations/02-terraform-aws-lab/terraform/secure/main.tf)
- [test_terraform_lab.py](../../../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
