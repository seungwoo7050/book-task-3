# 02 Terraform AWS Lab 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- Terraform을 deploy 결과가 아니라 보안 스캐너가 먹는 입력 산출물로 다시 읽는다.
- 본문은 `insecure/secure fixture 쌍 -> plan JSON 산출 -> resource contract 테스트` 순서로 배치해 후속 CSPM rule engine과의 연결을 선명하게 만든다.

## 먼저 붙들 소스 묶음
- [`../../../00-aws-security-foundations/02-terraform-aws-lab/README.md`](../../../00-aws-security-foundations/02-terraform-aws-lab/README.md)
- [`../../../00-aws-security-foundations/02-terraform-aws-lab/problem/README.md`](../../../00-aws-security-foundations/02-terraform-aws-lab/problem/README.md)
- [`../../../00-aws-security-foundations/02-terraform-aws-lab/docs/concepts/terraform-plan-reading.md`](../../../00-aws-security-foundations/02-terraform-aws-lab/docs/concepts/terraform-plan-reading.md)
- [`../../../00-aws-security-foundations/02-terraform-aws-lab/python/README.md`](../../../00-aws-security-foundations/02-terraform-aws-lab/python/README.md)
- [`../../../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py`](../../../00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py)
- [`../../../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py`](../../../00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - apply 없이도 왜 이 lab이 독립 프로젝트인지, 어떤 verify 흐름을 공식 경로로 볼지 정리한다.
- `10-development-timeline.md`
  - 도입: Terraform의 핵심 산출물을 infra state가 아니라 scan input으로 전환하는 맥락을 먼저 준다.
  - Phase 1. insecure/secure lab을 같은 검증 흐름에 묶었다.
  - Phase 2. `terraform show -json`을 산출물로 남겼다.
  - Phase 3. resource type 테스트로 입력 계약을 고정했다.
  - 마무리: 다음 프로젝트에서 이 plan JSON이 CSPM finding으로 변하는 질문을 남긴다.

## 강조할 코드와 CLI
- 코드 앵커: `verify_lab`, terraform subprocess 호출, insecure/secure fixture 비교, resource type assertions
- CLI 앵커: `terraform init`, `terraform validate`, `terraform plan`, `terraform show -json`, `pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests`
- 개념 훅: Terraform에서 중요한 것은 apply 이전에도 plan graph가 이미 보안 분석 입력이 된다는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
