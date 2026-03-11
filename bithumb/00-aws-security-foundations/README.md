# 00 AWS Security Foundations

이 트랙은 이후 보안 도구들이 공통으로 기대하는 가장 작은 판단 규칙과 입력 구조를 만드는 단계입니다.

## 이 트랙이 답하려는 큰 질문

클라우드 보안 도구를 만들기 전에, 무엇을 어떤 입력으로 읽고 어떤 기준으로 설명해야 하는가?

## 프로젝트 맵

| ID | 프로젝트 | 문제 | 답 | 검증 | 다음 단계 연결 |
| --- | --- | --- | --- | --- | --- |
| 01 | [AWS Security Primitives](01-aws-security-primitives/README.md)<br>[문제](01-aws-security-primitives/problem/README.md) | IAM policy가 왜 allow 또는 deny 되는가 | statement match와 `explicit deny` 우선순위를 갖는 평가 엔진 구현 | `pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests` | 04번에서 위험 finding을 만들 때 평가 감각을 재사용 |
| 02 | [Terraform AWS Lab](02-terraform-aws-lab/README.md)<br>[문제](02-terraform-aws-lab/problem/README.md) | Terraform을 어떻게 보안 분석 입력으로 읽을 것인가 | insecure/secure 실습 쌍과 plan JSON 생성 흐름을 고정 | `pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests` | 05번 CSPM 규칙 엔진의 직접 입력 준비 |
| 03 | [CloudTrail Log Basics](03-cloudtrail-log-basics/README.md)<br>[문제](03-cloudtrail-log-basics/problem/README.md) | 원본 로그를 어떻게 queryable하게 바꿀 것인가 | 공통 이벤트 모델, DuckDB, Parquet로 정규화 | `pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests` | 07번 security lake와 10번 캡스톤 적재 흐름 준비 |

## 추천 읽기 순서

1. 01에서 정책 판단 규칙을 익힙니다.
2. 02에서 선언형 인프라 입력을 보안 분석 관점으로 읽습니다.
3. 03에서 로그를 이후 탐지에 재사용 가능한 구조로 바꿉니다.

## 이 트랙을 끝내면 설명할 수 있어야 하는 것

- IAM 평가 규칙을 코드와 테스트로 설명할 수 있어야 합니다.
- Terraform plan JSON과 CloudTrail fixture를 “후속 분석 입력”으로 읽을 수 있어야 합니다.
- 이후 트랙의 finding, detection, remediation이 어떤 기반 위에서 동작하는지 설명할 수 있어야 합니다.
