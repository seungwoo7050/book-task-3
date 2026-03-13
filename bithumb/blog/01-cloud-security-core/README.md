# 01 Cloud Security Core 읽기 안내

이 트랙은 foundation에서 만든 입력 계약을 실제 finding, remediation, detection, governance 흐름으로 확장하는 구간이다. 각 프로젝트는 독립적으로 작동하지만, 순서대로 읽으면 “설명 가능한 입력 -> triage finding -> 조치안 -> detection query -> governance state”가 하나의 언어로 묶이는 과정이 보인다.

특히 이 구간은 false positive를 줄이는 기준이 계속 반복해서 등장한다. broad permission 분해, secure fixture 0건, approval/expiry 판정 같은 장면을 이어서 읽으면 왜 작은 rule 하나도 테스트와 상태 모델 위에 서야 하는지 감이 빨리 잡힌다.

| 프로젝트 | 시리즈 지도 | evidence | outline | 최종 글 | 대표 검증 |
| --- | --- | --- | --- | --- | --- |
| 04 IAM Policy Analyzer | [00-series-map](04-iam-policy-analyzer/00-series-map.md) | [05-evidence-ledger](04-iam-policy-analyzer/05-evidence-ledger.md) | [_structure-outline](04-iam-policy-analyzer/_structure-outline.md) | [10-development-timeline](04-iam-policy-analyzer/10-development-timeline.md) | `pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests` |
| 05 CSPM Rule Engine | [00-series-map](05-cspm-rule-engine/00-series-map.md) | [05-evidence-ledger](05-cspm-rule-engine/05-evidence-ledger.md) | [_structure-outline](05-cspm-rule-engine/_structure-outline.md) | [10-development-timeline](05-cspm-rule-engine/10-development-timeline.md) | `pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests` |
| 06 Remediation Pack Runner | [00-series-map](06-remediation-pack-runner/00-series-map.md) | [05-evidence-ledger](06-remediation-pack-runner/05-evidence-ledger.md) | [_structure-outline](06-remediation-pack-runner/_structure-outline.md) | [10-development-timeline](06-remediation-pack-runner/10-development-timeline.md) | `pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests` |
| 07 Security Lake Mini | [00-series-map](07-security-lake-mini/00-series-map.md) | [05-evidence-ledger](07-security-lake-mini/05-evidence-ledger.md) | [_structure-outline](07-security-lake-mini/_structure-outline.md) | [10-development-timeline](07-security-lake-mini/10-development-timeline.md) | `pytest 01-cloud-security-core/07-security-lake-mini/python/tests` |
| 08 Container Guardrails | [00-series-map](08-container-guardrails/00-series-map.md) | [05-evidence-ledger](08-container-guardrails/05-evidence-ledger.md) | [_structure-outline](08-container-guardrails/_structure-outline.md) | [10-development-timeline](08-container-guardrails/10-development-timeline.md) | `pytest 01-cloud-security-core/08-container-guardrails/python/tests` |
| 09 Exception and Evidence Manager | [00-series-map](09-exception-and-evidence-manager/00-series-map.md) | [05-evidence-ledger](09-exception-and-evidence-manager/05-evidence-ledger.md) | [_structure-outline](09-exception-and-evidence-manager/_structure-outline.md) | [10-development-timeline](09-exception-and-evidence-manager/10-development-timeline.md) | `pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests` |

## 읽을 때 먼저 볼 포인트

- 04와 05에서는 finding을 잘 뽑는 기준이 무엇인지 본다.
- 06과 09에서는 finding 이후 상태를 어떻게 안전하게 다루는지 본다.
- 07과 08은 detection과 guardrail이 서로 다른 입력을 어떻게 같은 언어로 설명하는지 이어서 본다.

legacy 격리 원칙은 [`../_legacy/2026-03-13-isolate-and-rewrite/01-cloud-security-core`](../_legacy/2026-03-13-isolate-and-rewrite/01-cloud-security-core)에서 확인할 수 있다.
