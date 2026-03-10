# 재현 가이드

## 무엇을 재현하나

- insecure lab과 secure lab이 모두 local plan JSON으로 변환되는지
- 실제 AWS 계정 없이도 Terraform 검증 흐름이 재현되는지
- 다음 CSPM 엔진이 읽을 수 있는 입력이 안정적으로 생성되는지

## 사전 조건

- `python3` 3.13+, `terraform` CLI 설치가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## 기대 결과

- 모듈 실행 시 stdout에 `insecure:`와 `secure:` 두 줄이 출력되고, 각 lab 디렉터리에 `tfplan.json`이 생성돼야 합니다.
- pytest는 Terraform이 설치된 환경에서 2개 테스트를 통과해야 하며, insecure/secure plan 모두 특정 리소스 타입을 포함해야 합니다.
- 이 재현의 핵심 산출물은 리소스 배포가 아니라 `tfplan.json`입니다.

## 결과가 다르면 먼저 볼 파일

- Terraform 실행 흐름이 막히면: [../python/src/terraform_aws_lab/verify.py](../python/src/terraform_aws_lab/verify.py)
- insecure 입력을 다시 보려면: [../terraform/insecure/main.tf](../terraform/insecure/main.tf)
- secure 입력을 다시 보려면: [../terraform/secure/main.tf](../terraform/secure/main.tf)
- 검증 기준을 다시 보려면: [../python/tests/test_terraform_lab.py](../python/tests/test_terraform_lab.py)
- 도구 설치 기준을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 “Terraform을 끝까지 배포해야만 배울 수 있다”는 오해를 깨고, 분석 친화적인 입력을 안정적으로 만드는 방법을 보여 줍니다.
- 학습자는 이 단계에서 insecure 예제를 보는 것만큼 secure 예제가 왜 통과해야 하는지도 같이 설명할 수 있어야 합니다.
