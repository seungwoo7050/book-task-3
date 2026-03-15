# 02 Terraform AWS Lab evidence ledger

- 복원 원칙: 기존 blog 본문은 제외하고 `README/problem/docs`, Terraform 소스, Python 검증 스크립트, pytest, 실제 재실행 결과만 사용했다.
- 날짜 고정: 아래 실행 결과는 `2026-03-14` 기준이다.
- 프로젝트 성격: 이 lab의 산출물은 "배포 성공"이 아니라 다음 프로젝트가 읽을 수 있는 `tfplan.json`이다.

## 사용한 입력 근거

- 설명 문서
  - `README.md`
  - `problem/README.md`
  - `python/README.md`
  - `docs/README.md`
  - `docs/concepts/terraform-plan-reading.md`
- 구현
  - `python/src/terraform_aws_lab/verify.py`
  - `terraform/insecure/main.tf`
  - `terraform/secure/main.tf`
  - `terraform/insecure/tfplan.json`
  - `terraform/secure/tfplan.json`
- 테스트
  - `python/tests/test_terraform_lab.py`

## 다시 실행한 명령

```bash
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src \
  .venv/bin/python -m terraform_aws_lab.verify

PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src \
  .venv/bin/python -m pytest \
  00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

## 재실행 결과

- `python -m terraform_aws_lab.verify` -> `insecure: 5 resources`, `secure: 5 resources`
- pytest 최종 결과 -> `3 passed in 11.35s`

## 이번 재검증에서 추가로 확인한 사실

- `2026-03-14`에 `verify`와 `pytest`를 병렬로 돌렸을 때 insecure lab의 `terraform plan`이 state lock으로 실패했다.
- 실패 메시지 핵심은 `Error acquiring the state lock`이었다.
- 같은 명령을 순차로 다시 돌리면 pytest는 정상 통과했다.
- `run_lab()`가 각 lab 디렉터리 안의 고정 파일명 `tfplan`과 `tfplan.json`을 덮어쓰는 구조이기 때문에, 이 동작은 소스와 재실행 결과를 함께 본 source-based inference로 설명할 수 있다.

## 단계별 근거

### 1. insecure/secure를 같은 재현 루프로 묶었다

- 근거 소스: `verify.py`
- 핵심 코드: `terraform_available()`, `AWS_ENV`, `run_lab()` 앞부분
- 확인한 사실:
  - Terraform CLI가 없으면 바로 실패한다.
  - AWS 계정 없이도 돌 수 있도록 dummy credential과 region을 주입한다.
  - `init -> validate -> plan -> show -json`이 insecure/secure 둘 다 같은 순서로 실행된다.

### 2. plan JSON을 후속 입력으로 저장했다

- 근거 소스: `verify.py`, `tfplan.json`
- 핵심 코드: `json_path.write_text(rendered.stdout)`
- 확인한 사실:
  - binary plan을 만든 뒤 `terraform show -json`으로 렌더링한다.
  - 결과를 stdout으로만 소비하지 않고 각 lab 디렉터리에 `tfplan.json`으로 남긴다.
  - 메인 스크립트는 `planned_values.root_module.resources` 길이를 세어 `5 resources` 요약을 출력한다.

### 3. insecure/secure 차이를 resource contract로 고정했다

- 근거 소스: `test_terraform_lab.py`, `main.tf`, `tfplan.json`
- 확인한 사실:
  - insecure plan에는 `aws_s3_bucket`, `aws_security_group`, `aws_iam_policy broad_admin`가 포함된다.
  - secure plan에는 `aws_s3_bucket_public_access_block`, `aws_iam_policy scoped_read`가 포함된다.
  - `public_access_block` 값은 insecure에서 모두 `false`, secure에서 모두 `true`다.
  - security group ingress는 insecure `0.0.0.0/0`, secure `10.10.10.0/24`다.
  - IAM policy는 insecure `Action: "*" / Resource: "*"`, secure는 S3 read 범위로 제한된다.

## 남은 한계

- `problem/README.md`가 명시한 대로 apply는 하지 않는다.
- drift detection과 misconfiguration rule evaluation은 아직 없다.
- `run_lab()`는 고정 파일명 `tfplan`을 사용하므로 병렬 실행에 안전하지 않다. 이 문장은 `verify.py` 구조와 `2026-03-14` state lock 실패를 함께 본 source-based inference다.
