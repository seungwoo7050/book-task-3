# Terraform을 배포가 아닌 분석의 도구로 보기

## 왜 이 과제를 만들었나

보안 직무에서 Terraform은 "인프라를 배포하는 도구"가 아니다.
적어도 이 트랙에서는, Terraform은 "인프라 설정을 정적으로 분석할 수 있는 선언"이다.

CSPM(Cloud Security Posture Management)이 하는 일의 대부분은
"이 설정이 안전한가?"를 자동으로 판단하는 것이다.
그런데 판단하려면 먼저 설정을 기계가 읽을 수 있는 형태로 가져와야 한다.
`terraform plan -out=tfplan`을 실행하고 `terraform show -json tfplan`으로 변환하면,
Terraform이 만들려는 리소스들이 JSON으로 나온다.
이 JSON이 바로 CSPM 규칙 엔진의 입력이 된다.

이 과제는 그 발견 — "plan JSON이 있으면 AWS 계정 없이도 보안 분석이 가능하다" — 을
직접 체험하는 실습이다.

## insecure vs secure: 무엇이 다른가

이 과제는 같은 종류의 리소스를 두 가지 설정으로 만든다.

### insecure 설정의 문제들

`terraform/insecure/main.tf`에는 세 가지 전형적인 misconfiguration이 들어 있다.

**1. S3 버킷 퍼블릭 접근 차단 미설정**

`block_public_acls`, `block_public_policy`, `ignore_public_acls`, `restrict_public_buckets`가
전부 `false`다. 이건 "이 버킷에 퍼블릭 접근이 가능합니다"를 의미한다.
실제 운영에서 이 설정이 열려 있으면 데이터 유출 사고의 시작점이 된다.

**2. Security Group에서 SSH를 0.0.0.0/0으로 개방**

인터넷 전체에서 22번 포트로 들어올 수 있다.
공격자가 가장 먼저 스캔하는 포트 중 하나이고,
이 설정이 있는 것만으로도 보안 감사에서 바로 HIGH finding이 된다.

**3. IAM 정책에서 Action=\*, Resource=\***

모든 리소스에 대해 모든 작업을 허용하는 관리자 정책이다.
이건 최소 권한 원칙의 정반대이며, privilege escalation의 출발점이 된다.

### secure 설정과의 차이

`terraform/secure/main.tf`는 같은 리소스 종류를 안전하게 설정한다.
- S3: 퍼블릭 접근 차단 플래그 전부 `true`
- Security Group: SSH 접근을 `10.10.10.0/24`(내부 네트워크)로 제한
- IAM 정책: `s3:GetObject`과 `s3:ListBucket`만 특정 버킷에 허용

이 두 설정을 나란히 두면, 뒤 과제(05-CSPM Rule Engine)에서 "통과/실패" 테스트 데이터를
바로 재사용할 수 있다.

## 설계 선택

### AWS 계정 없이 돌리는 방법

Terraform provider에 `skip_credentials_validation`, `skip_metadata_api_check`,
`skip_region_validation`, `skip_requesting_account_id`를 전부 `true`로 설정했다.
`access_key`와 `secret_key`는 더미 값(`study2`)을 넣었다.

이렇게 하면 `terraform init`, `terraform validate`, `terraform plan -refresh=false`까지
AWS API를 한 번도 호출하지 않고 실행할 수 있다.
`-refresh=false`가 핵심이다. 이 플래그가 없으면 Terraform이 실제 상태를 확인하려고
AWS에 요청을 보내게 된다.

### 검증 자동화를 Python에서 한 이유

`verify.py`는 `subprocess`로 `terraform init → validate → plan → show -json` 파이프라인을 실행하고,
결과 JSON에서 리소스 타입을 검증한다.

Shell 스크립트로도 할 수 있었지만, pytest로 래핑하면 전체 트랙의 `make test-integration`에
자연스럽게 포함되고, 실패했을 때 어떤 리소스가 빠졌는지 assertion 메시지로 바로 확인된다.

### plan JSON이 핵심 산출물인 이유

`tfplan.json` 안의 `planned_values.root_module.resources`가 CSPM 규칙 엔진의 입력 구조다.
각 리소스의 `type`, `name`, `values`를 읽으면 대부분의 정적 misconfiguration 규칙을 만들 수 있다.

이 구조를 먼저 눈에 익혀 두면, 과제 05에서 `scan_plan` 함수가 왜 그런 형태로 리소스를
순회하는지 바로 이해된다.

## 이 과제를 하고 나서 달라진 점

"Terraform = apply = 배포"라는 인식이 바뀌었다.
보안 팀에서 Terraform을 다루는 방식은 apply가 아니라 plan이다.
plan JSON을 읽을 수 있으면, 배포 전에 위험한 설정을 자동으로 걸러낼 수 있다.

그리고 insecure/secure 설정을 직접 나란히 두고 비교하면서,
"왜 이 설정이 위험한지"를 추상적인 규칙이 아니라 구체적인 필드 값으로 설명할 수 있게 되었다.

## 이 과제의 위치

- **과제 01 → 이 과제**: IAM 정책 평가에서 한 발 더 나아가, 인프라 설정 자체를 분석할 수 있는 입력을 만드는 과제
- **이 과제 → 과제 05**: 여기서 만든 plan JSON이 CSPM Rule Engine의 입력이 된다
- **이 과제 → 과제 10**: Control Plane의 scan API가 Terraform plan path를 받아서 finding을 생성할 때, 같은 plan JSON 구조를 사용한다

## 한계와 v1 범위

- `terraform apply`는 하지 않는다. 이 과제의 범위는 plan JSON 생성까지다.
- 실제 AWS 상태와의 drift detection은 다루지 않는다.
- module 참조가 있는 복잡한 Terraform 구성은 포함하지 않았다.
