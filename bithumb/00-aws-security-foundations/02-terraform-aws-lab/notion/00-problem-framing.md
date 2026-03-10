# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

Terraform을 보안 실습에서 어떻게 써야 하는가? 이 프로젝트의 답은 분명합니다.
`apply`보다 먼저 `plan JSON`을 읽을 수 있어야 한다는 것입니다. 실제 AWS 계정이 없어도 인프라 설정을
정적으로 분석할 수 있어야 이후 CSPM 규칙 엔진으로 자연스럽게 이어집니다.

## 실제 입력과 출력

입력:
- `terraform/insecure/main.tf`
- `terraform/secure/main.tf`
- Terraform이 생성한 plan JSON

출력:
- insecure/secure 설정 차이를 보여 주는 plan 결과
- 후속 프로젝트에서 재사용 가능한 분석 입력 구조

## 이 프로젝트의 강한 제약

- `terraform apply`는 범위 밖입니다.
- AWS API 호출 없이 `init -> validate -> plan -> show -json` 흐름만 재현합니다.
- Terraform provider는 더미 credential과 skip 옵션으로 로컬 재현성을 우선합니다.

## 완료로 보는 기준

- insecure와 secure 예제의 차이를 필드 단위로 설명할 수 있어야 합니다.
- `planned_values.root_module.resources` 구조를 읽고 후속 규칙 엔진으로 연결할 수 있어야 합니다.
- 테스트 두 개가 모두 의미 있는 plan JSON을 생성해야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_terraform_lab.py](../python/tests/test_terraform_lab.py)
- 이전 배경 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
