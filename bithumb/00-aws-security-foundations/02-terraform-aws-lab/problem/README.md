# 문제 정리

## 원래 문제

Terraform을 배포 성공 여부가 아니라 보안 분석 입력으로 읽는 실습입니다.
insecure 설정과 secure 설정을 plan JSON 기준으로 비교해, 다음 프로젝트가 읽을 입력 구조를 먼저 고정해야 합니다.

## 제공된 자료

- `terraform/insecure/main.tf`
- `terraform/secure/main.tf`
- lab별 `terraform init`, `validate`, `plan`, `show -json` 흐름

## 제약

- 실제 `terraform apply`는 하지 않습니다.
- AWS 계정 없이 로컬에서 plan JSON을 재현하는 데 집중합니다.

## 통과 기준

- insecure lab과 secure lab 모두 plan JSON을 생성할 수 있어야 합니다.
- 테스트가 대표 resource type 존재를 검증해야 합니다.
- 결과 plan이 다음 프로젝트 입력으로 재사용 가능해야 합니다.

## 이번 프로젝트에서 일부러 제외한 것

- 실제 리소스 배포
- drift detection
- misconfiguration 규칙 평가 자체
