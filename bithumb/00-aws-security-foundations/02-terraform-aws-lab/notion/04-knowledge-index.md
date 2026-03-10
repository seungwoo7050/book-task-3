# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- Terraform plan JSON은 CSPM에서 가장 다루기 쉬운 shift-left 입력 중 하나입니다.
- insecure/secure 쌍은 보안 학습과 테스트 설계에서 둘 다 중요합니다.
- provider credential이 더미 값이어도 `init`, `validate`, `plan`, `show -json` 흐름은 충분히 재현 가능합니다.
- 보안 분석의 첫 단계는 반드시 live cloud scan일 필요가 없습니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/terraform-plan-reading.md](../docs/concepts/terraform-plan-reading.md)
- 문제 범위: [../problem/README.md](../problem/README.md)
- 검증 코드: [../python/tests/test_terraform_lab.py](../python/tests/test_terraform_lab.py)
- 실행 스크립트: [../python/src/terraform_aws_lab/verify.py](../python/src/terraform_aws_lab/verify.py)
- Terraform insecure 예제: [../terraform/insecure/main.tf](../terraform/insecure/main.tf)
- Terraform secure 예제: [../terraform/secure/main.tf](../terraform/secure/main.tf)

## 재현 체크포인트

- `terraform/insecure/tfplan.json`과 `terraform/secure/tfplan.json`이 모두 생성되는지 확인합니다.
- insecure plan에는 `aws_s3_bucket`과 `aws_security_group`이, secure plan에는 `aws_s3_bucket_public_access_block`과 `aws_iam_policy`가 포함되는지 봅니다.
- Terraform이 설치되지 않았을 때 테스트가 skip되는 이유를 이해하고, skip와 pass를 혼동하지 않습니다.

## 다음 프로젝트로 이어지는 질문

- `05-cspm-rule-engine`은 이 plan JSON을 직접 읽어 misconfiguration finding을 생성합니다.
- `10-cloud-security-control-plane`은 Terraform scan 요청에서도 같은 입력 구조를 사용합니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
