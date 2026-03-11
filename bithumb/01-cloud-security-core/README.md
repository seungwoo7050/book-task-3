# 01 Cloud Security Core

이 트랙은 기초 입력 위에서 실제 운영자가 읽을 수 있는 finding, remediation, detection, governance 흐름을 쌓는 단계입니다.

## 이 트랙이 답하려는 큰 질문

기초 입력을 읽는 수준을 넘어, 위험 판단과 조치 흐름을 어떻게 설명 가능한 보안 도구로 만들 것인가?

## 프로젝트 맵

| ID | 프로젝트 | 문제 | 답 | 검증 | 다음 단계 연결 |
| --- | --- | --- | --- | --- | --- |
| 04 | [IAM Policy Analyzer](04-iam-policy-analyzer/README.md)<br>[문제](04-iam-policy-analyzer/problem/README.md) | 정책 평가 결과를 least privilege finding으로 바꾸기 | broad permission과 escalation 패턴을 severity 있는 finding으로 변환 | `pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests` | 06번 remediation과 10번 캡스톤의 IAM finding 입력 |
| 05 | [CSPM Rule Engine](05-cspm-rule-engine/README.md)<br>[문제](05-cspm-rule-engine/problem/README.md) | plan JSON과 snapshot에서 triage 가능한 misconfiguration 찾기 | Terraform plan과 access key snapshot을 함께 읽는 규칙 엔진 구현 | `pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests` | 06번 remediation과 10번 캡스톤의 인프라 finding 입력 |
| 06 | [Remediation Pack Runner](06-remediation-pack-runner/README.md)<br>[문제](06-remediation-pack-runner/problem/README.md) | finding 이후 조치안을 어떻게 제안할 것인가 | dry-run remediation과 승인 필요 여부를 분리하는 runner 구현 | `pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests` | 10번 캡스톤의 remediation worker 모델 |
| 07 | [Security Lake Mini](07-security-lake-mini/README.md)<br>[문제](07-security-lake-mini/problem/README.md) | 적재된 로그에서 어떤 detection query를 반복 실행할 것인가 | local lake 적재와 preset detection query 실행 흐름 구현 | `pytest 01-cloud-security-core/07-security-lake-mini/python/tests` | 10번 캡스톤의 CloudTrail 적재와 alert성 finding |
| 08 | [Container Guardrails](08-container-guardrails/README.md)<br>[문제](08-container-guardrails/problem/README.md) | manifest와 image metadata에서 위험 설정 찾기 | Kubernetes manifest와 image metadata scanner 구현 | `pytest 01-cloud-security-core/08-container-guardrails/python/tests` | 10번 캡스톤의 k8s 입력 처리 |
| 09 | [Exception and Evidence Manager](09-exception-and-evidence-manager/README.md)<br>[문제](09-exception-and-evidence-manager/problem/README.md) | finding, exception, evidence, audit를 어떻게 연결할 것인가 | 승인, 만료, 증적, audit trail을 나눈 거버넌스 모델 구현 | `pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests` | 10번 캡스톤의 예외와 감사 레코드 모델 |

## 추천 읽기 순서

1. 04와 05로 finding을 만드는 두 축을 먼저 봅니다.
2. 06에서 finding 이후 조치 흐름을 분리합니다.
3. 07과 08에서 로그와 컨테이너 입력을 각각 확장합니다.
4. 09에서 운영 거버넌스 모델을 붙입니다.

## 이 트랙을 끝내면 설명할 수 있어야 하는 것

- 보안 도구가 단순 판별기를 넘어 finding과 remediation으로 이어지려면 무엇이 필요한지 설명할 수 있어야 합니다.
- detection과 governance가 왜 별도 프로젝트로 분리되어야 하는지 설명할 수 있어야 합니다.
- 캡스톤에서 어떤 로직을 어떤 입력 경로로 재사용하는지 연결해서 설명할 수 있어야 합니다.
