# 문제 정리

## 문제 요약

Terraform plan JSON과 리소스 snapshot을 읽어, 보안 운영자가 바로 triage할 수 있는 finding을 생성합니다.

## 입력

- Terraform plan JSON
- access key snapshot JSON

## 출력

- finding 목록
- severity와 remediation 힌트

## 학습 포인트

규칙 자체의 화려함보다 입력 스키마와 설명 가능성을 우선합니다.
