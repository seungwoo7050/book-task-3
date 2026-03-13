# 02 Terraform AWS Lab 근거 정리

Terraform을 apply 도구가 아니라 이후 보안 스캐너가 읽을 선언형 입력으로 다루게 만드는 실습이다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. insecure/secure lab을 같은 검증 흐름에 묶었다

이 구간에서는 `insecure/secure lab을 같은 검증 흐름에 묶었다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: 두 Terraform 실습을 사람이 수동 비교하지 않고 같은 코드 경로로 돌릴 수 있게 만든다.
- 변경 단위: `python/src/terraform_aws_lab/verify.py`의 `AWS_ENV`, `terraform_available`, `run_lab` 진입부
- 처음 가설: 후속 프로젝트가 plan JSON을 입력으로 쓰려면, 먼저 lab 두 개가 같은 루틴으로 재현돼야 한다.
- 실제 조치: 스크립트는 Terraform CLI 유무를 먼저 확인하고, 로컬 더미 AWS 환경 변수를 주입한 뒤 각 lab 디렉터리에서 같은 명령을 반복하게 만들었다. 핵심은 실제 apply 없이도 같은 입력 구조를 계속 얻을 수 있게 하는 쪽이었다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify`
- 검증 신호:
  - 검증 스크립트 실행 결과가 `insecure: 5 resources`, `secure: 5 resources`로 떨어졌다.
  - Terraform 1.5.7 환경에서 실제 명령 경로가 살아 있어 로컬에서 그대로 재현됐다.
- 핵심 코드 앵커: `00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py:22-44`
- 새로 배운 것: CSPM 관점에서 Terraform의 핵심 산출물은 apply 결과보다 `planned_values.root_module.resources` 같은 plan 구조다. 분석은 선언형 변경 의도를 읽는 데서 시작한다.
- 다음: 이제 plan 결과를 파일로 남겨, 다른 프로젝트가 바로 읽을 수 있는 형태로 고정해야 했다.

## Phase 2. plan JSON을 산출물로 남겼다

이 구간에서는 `plan JSON을 산출물로 남겼다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: `terraform show -json` 결과를 후속 스캐너가 읽을 실제 파일로 남긴다.
- 변경 단위: `python/src/terraform_aws_lab/verify.py`의 `plan -> show -json -> tfplan.json` 경로
- 처음 가설: stdout만 보고 끝내면 다음 단계에서 다시 Terraform CLI를 호출해야 한다. JSON 파일이 남아야 rule engine이 입력을 재사용할 수 있다.
- 실제 조치: `terraform plan`으로 binary plan을 만든 뒤 `terraform show -json`으로 렌더링해 `tfplan.json`으로 저장했다. 마지막에는 `planned_values.root_module.resources` 길이를 세어 lab별 resource count를 바로 확인하게 했다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify`
- 검증 신호:
  - 스크립트는 insecure/secure 모두 5개 resource를 읽었다.
  - `tfplan.json`이 실제 파일로 남아서 05번 CSPM scanner가 fixture처럼 재사용할 수 있는 상태가 됐다.
- 핵심 코드 앵커: `00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py:45-75`
- 새로 배운 것: “배포 전에 읽는 보안”은 실행 결과가 아니라 plan의 구조화된 표현을 다룬다. JSON으로 렌더링하는 순간부터 Terraform은 분석 입력이 된다.
- 다음: 이제 테스트로 insecure/secure lab이 각각 어떤 자원을 포함하는지 잠가 두어야 했다.

## Phase 3. resource type 테스트로 입력 계약을 고정했다

이 구간에서는 `resource type 테스트로 입력 계약을 고정했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 다음 프로젝트가 기대하는 자원 종류가 실제 plan에 들어 있는지 테스트로 확인한다.
- 변경 단위: `python/tests/test_terraform_lab.py`의 insecure/secure 검증
- 처음 가설: plan JSON 파일이 만들어지기만 해서는 부족하다. insecure lab과 secure lab이 어떤 보안 차이를 대표하는지도 테스트가 말해줘야 한다.
- 실제 조치: 테스트는 insecure lab에서 `aws_s3_bucket`, `aws_security_group`가 보이는지 확인하고, secure lab에서는 `aws_s3_bucket_public_access_block`, `aws_iam_policy`가 있는지 확인했다. 이 검증이 있어야 05번 프로젝트가 S3 public access나 ingress 규칙을 안정적으로 읽을 수 있다.
- CLI:
  - `PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests`
- 검증 신호:
  - 직렬 재검증 기준 pytest가 `3 passed in 17.61s`로 통과했다.
  - insecure/secure가 서로 다른 resource type 집합을 대표한다는 계약이 테스트에 남았다.
- 핵심 코드 앵커: `00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py:19-30`
- 새로 배운 것: 보안용 fixture는 단순히 파일이 존재하는 것으로 충분하지 않다. 어떤 resource type을 담고 있어야 하는지까지 계약으로 고정해야 false positive가 줄어든다.
- 다음: 다음 프로젝트는 이 plan JSON을 직접 읽어 misconfiguration finding을 만든다.
