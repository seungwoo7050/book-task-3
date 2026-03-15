# bithumb 서버 개발 비필수 답안지

이 문서는 각 비필수 실습의 해답을 실제 Python 소스와 테스트만으로 읽히게 정리한 답안지다. 핵심은 각 패키지가 "어떤 보안 판단을 자동화하는가"와 "그 판단을 어떤 테스트로 다시 확인하는가"를 한 번에 보여 주는 것이다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-aws-security-primitives-python](01-aws-security-primitives-python_answer.md) | 시작 위치의 구현을 완성해 실제 AWS API나 계정 상태를 조회하지 않습니다와 학습 범위는 statement 단위 match와 우선순위 설명까지로 제한합니다를 한 흐름으로 설명하고 검증한다. 핵심은 explain와 _as_list, StatementResult 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/01-aws-security-primitives/python && PYTHONPATH=src python3 -m pytest` |
| [02-terraform-aws-lab-python](02-terraform-aws-lab-python_answer.md) | 시작 위치의 구현을 완성해 실제 terraform apply는 하지 않습니다와 AWS 계정 없이 로컬에서 plan JSON을 재현하는 데 집중합니다를 한 흐름으로 설명하고 검증한다. 핵심은 terraform_available와 run_lab, default_labs_root 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/02-terraform-aws-lab/python && PYTHONPATH=src python3 -m pytest` |
| [03-cloudtrail-log-basics-python](03-cloudtrail-log-basics-python_answer.md) | 시작 위치의 구현을 완성해 실제 운영 규모의 대용량 적재는 다루지 않습니다와 정규화 필드는 이후 프로젝트가 쓰는 최소 공통 필드로 제한합니다를 한 흐름으로 설명하고 검증한다. 핵심은 EventRecord와 normalize_cloudtrail_events, normalize_vpc_flow_logs 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/00-aws-security-foundations/03-cloudtrail-log-basics/python && PYTHONPATH=src python3 -m pytest` |
| [04-iam-policy-analyzer-python](04-iam-policy-analyzer-python_answer.md) | 시작 위치의 구현을 완성해 조직 전체 권한 그래프는 추적하지 않습니다와 policy analyzer는 단일 policy 문서 기준의 위험 판단까지만 담당합니다를 한 흐름으로 설명하고 검증한다. 핵심은 _as_list와 Finding, analyze_policy 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/04-iam-policy-analyzer/python && PYTHONPATH=src python3 -m pytest` |
| [05-cspm-rule-engine-python](05-cspm-rule-engine-python_answer.md) | 시작 위치의 구현을 완성해 실제 배포 환경 전체를 스캔하지 않습니다와 local fixture 기준으로 재현 가능한 규칙만 다룹니다를 한 흐름으로 설명하고 검증한다. 핵심은 scan와 Finding, _resources 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/05-cspm-rule-engine/python && PYTHONPATH=src python3 -m pytest` |
| [06-remediation-pack-runner-python](06-remediation-pack-runner-python_answer.md) | 시작 위치의 구현을 완성해 실제 patch 적용은 하지 않습니다와 외부 승인 시스템이나 rollback orchestration은 연결하지 않습니다를 한 흐름으로 설명하고 검증한다. 핵심은 dry_run와 RemediationPlan, build_dry_run 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python && PYTHONPATH=src python3 -m pytest` |
| [07-security-lake-mini-python](07-security-lake-mini-python_answer.md) | 시작 위치의 구현을 완성해 로컬 단일 테이블 흐름에 집중합니다와 분산 저장소나 대용량 최적화는 다루지 않습니다를 한 흐름으로 설명하고 검증한다. 핵심은 ingest와 Alert, _normalize 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/07-security-lake-mini/python && PYTHONPATH=src python3 -m pytest` |
| [08-container-guardrails-python](08-container-guardrails-python_answer.md) | 시작 위치의 구현을 완성해 실제 클러스터, admission controller, 런타임 이벤트는 다루지 않습니다와 manifest와 image metadata에서 설명 가능한 규칙만 다룹니다를 한 흐름으로 설명하고 검증한다. 핵심은 scan와 Finding, scan_manifest 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/08-container-guardrails/python && PYTHONPATH=src python3 -m pytest` |
| [09-exception-and-evidence-manager-python](09-exception-and-evidence-manager-python_answer.md) | 시작 위치의 구현을 완성해 영속 저장소는 사용하지 않습니다와 외부 티켓 시스템이나 승인 워크플로와 연동하지 않습니다를 한 흐름으로 설명하고 검증한다. 핵심은 demo와 ExceptionRecord, Evidence 흐름을 구현하고 테스트를 통과시키는 것이다. | `cd /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/09-exception-and-evidence-manager/python && PYTHONPATH=src python3 -m pytest` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
