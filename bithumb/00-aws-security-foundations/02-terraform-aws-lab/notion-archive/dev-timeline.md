# 02 Terraform AWS Lab — 개발 타임라인

이 문서는 프로젝트를 처음부터 다시 재현할 때 필요한 모든 단계를 순서대로 기록한다.
소스코드만으로는 알 수 없는 Terraform 설치, plan 생성 과정, 환경 변수 설정을 담고 있다.

---

## 1단계: Terraform 설치

### macOS (Homebrew)

```bash
brew install terraform
terraform version
# Terraform v1.5.x 이상 확인
```

### 버전 확인

`main.tf`에서 `required_version = ">= 1.5.0"`을 지정했으므로 1.5 이상이 필요하다.

```bash
terraform version
```

### doctor 검증

프로젝트 루트에서 `make doctor`를 실행하면 terraform이 설치되어 있는지 자동으로 확인한다.

```bash
cd study2
make doctor
```

---

## 2단계: 프로젝트 디렉토리 구조 생성

```
02-terraform-aws-lab/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── terraform-plan-reading.md
│   └── references/
│       └── README.md
├── problem/
│   └── README.md
├── python/
│   ├── README.md
│   ├── src/
│   │   └── terraform_aws_lab/
│   │       ├── __init__.py
│   │       └── verify.py
│   └── tests/
│       └── test_terraform_lab.py
└── terraform/
    ├── insecure/
    │   └── main.tf
    └── secure/
        └── main.tf
```

```bash
mkdir -p 00-aws-security-foundations/02-terraform-aws-lab/{docs/{concepts,references},problem,python/{src/terraform_aws_lab,tests},terraform/{insecure,secure}}
```

---

## 3단계: Terraform 설정 파일 작성

### insecure/main.tf 작성

AWS provider 설정에서 모든 credential/metadata 검증을 스킵하도록 설정했다.
이것이 "AWS 계정 없이 plan을 생성하는" 핵심 트릭이다.

```hcl
provider "aws" {
  region                      = "ap-northeast-2"
  access_key                  = "study2"
  secret_key                  = "study2"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
}
```

세 가지 위험 리소스를 선언:
- `aws_s3_bucket` + `aws_s3_bucket_public_access_block` (전부 false)
- `aws_security_group` (SSH 0.0.0.0/0)
- `aws_iam_policy` (Action=\*, Resource=\*)

### secure/main.tf 작성

같은 리소스 종류를 안전한 설정으로 선언:
- S3: 퍼블릭 차단 플래그 전부 true
- Security Group: SSH를 내부 CIDR(10.10.10.0/24)로 제한
- IAM 정책: s3:GetObject/ListBucket만 특정 버킷에 허용

---

## 4단계: Terraform plan JSON 생성

### insecure plan 생성

```bash
cd terraform/insecure

# 프로바이더 플러그인 다운로드 (최초 1회)
terraform init -backend=false

# HCL 문법 검증
terraform validate

# plan 생성 (AWS API 호출 없이)
terraform plan -refresh=false -out=tfplan

# plan을 JSON으로 변환
terraform show -json tfplan > tfplan.json
```

`-backend=false`: 원격 state backend를 사용하지 않는다.
`-refresh=false`: AWS에 현재 상태를 물어보지 않는다.

### secure plan 생성

```bash
cd terraform/secure
terraform init -backend=false
terraform validate
terraform plan -refresh=false -out=tfplan
terraform show -json tfplan > tfplan.json
```

### plan JSON 구조 확인

생성된 `tfplan.json`에서 핵심 경로:

```bash
# 리소스 목록 확인 (jq 필요)
cat tfplan.json | jq '.planned_values.root_module.resources[].type'
```

이 경로(`planned_values.root_module.resources`)가 과제 05 CSPM Rule Engine의 입력이 된다.

---

## 5단계: Python 검증 코드 작성

### verify.py 작성

`subprocess`를 사용해 Terraform CLI를 Python에서 호출하는 래퍼를 만들었다.

`run_lab(lab_dir)` 함수의 실행 순서:
1. `terraform init -backend=false`
2. `terraform validate`
3. `terraform plan -refresh=false -out=tfplan`
4. `terraform show -json tfplan`
5. 결과 JSON을 파싱해서 반환

환경 변수로 더미 AWS credential을 주입:
```python
AWS_ENV = {
    "AWS_ACCESS_KEY_ID": "study2",
    "AWS_SECRET_ACCESS_KEY": "study2",
    "AWS_REGION": "ap-northeast-2",
}
```

### test_terraform_lab.py 작성

두 가지 테스트:
1. insecure plan에서 `aws_s3_bucket`과 `aws_security_group` 리소스가 생성되는지 확인
2. secure plan에서 `aws_s3_bucket_public_access_block`과 `aws_iam_policy` 리소스가 생성되는지 확인

테스트는 terraform이 설치되어 있지 않으면 자동 스킵된다:
```python
pytestmark = pytest.mark.skipif(not terraform_available(), reason="terraform is not installed")
```

---

## 6단계: 실행과 검증

### 직접 verify 실행

```bash
cd python
PYTHONPATH=src python -m terraform_aws_lab.verify
```

출력 예시:
```
insecure: 5 resources
secure: 5 resources
```

### 테스트 실행

```bash
cd study2
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

또는 Makefile을 통해:

```bash
make test-integration
```

이 과제는 Terraform CLI에 의존하므로 `test-unit`이 아닌 `test-integration`에 포함된다.

---

## 7단계: .gitignore 관련

Terraform이 생성하는 파일들은 보통 git에 올리지 않는다:
- `.terraform/` — 프로바이더 플러그인 디렉토리
- `tfplan` — 바이너리 plan 파일
- `tfplan.json` — 변환된 JSON (재생성 가능)
- `.terraform.lock.hcl` — 프로바이더 버전 잠금 파일

---

## 환경 요약

| 항목 | 값 |
|------|-----|
| Python | 3.13+ |
| Terraform | 1.5.0+ |
| 핵심 의존성 | subprocess (표준 라이브러리) |
| 테스트 프레임워크 | pytest |
| AWS 계정 필요 여부 | 불필요 (skip 플래그 사용) |
| 외부 서비스 의존 | 없음 |
| 테스트 카테고리 | Integration (Terraform CLI 의존) |

---

## 주의사항

- Terraform 설치가 필수다. `terraform_available()` 체크로 미설치 시 테스트가 스킵되지만,
  과제를 재현하려면 반드시 설치해야 한다.
- `terraform init`은 프로바이더 플러그인을 다운로드한다. 네트워크 연결이 최초 1회 필요하다.
- `.terraform/` 디렉토리는 각 lab 폴더(insecure/, secure/) 안에 생성된다.
- `tfplan`과 `tfplan.json`이 lab 폴더에 생성되므로, git에 올리지 않도록 주의한다.
