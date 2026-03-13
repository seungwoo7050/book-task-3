# 00 AWS Security Foundations 읽기 안내

이 트랙은 나중에 나오는 analyzer, CSPM, lake, control plane이 기대는 입력 계약을 먼저 세우는 구간이다. 한마디로 “무엇을 탐지할까”보다 “무엇을 같은 모양으로 읽을 수 있게 만들까”에 더 집중한다.

읽는 순서는 IAM decision에서 시작해 Terraform plan 입력으로 넘어가고, 마지막에 raw log를 queryable event로 바꾸는 흐름이 가장 자연스럽다. 세 프로젝트를 차례로 읽으면 policy, infra declaration, log가 모두 설명 가능한 입력으로 바뀌는 과정을 한 번에 볼 수 있다.

| 프로젝트 | 시리즈 지도 | evidence | outline | 최종 글 | 대표 검증 |
| --- | --- | --- | --- | --- | --- |
| 01 AWS Security Primitives | [00-series-map](01-aws-security-primitives/00-series-map.md) | [05-evidence-ledger](01-aws-security-primitives/05-evidence-ledger.md) | [_structure-outline](01-aws-security-primitives/_structure-outline.md) | [10-development-timeline](01-aws-security-primitives/10-development-timeline.md) | `pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests` |
| 02 Terraform AWS Lab | [00-series-map](02-terraform-aws-lab/00-series-map.md) | [05-evidence-ledger](02-terraform-aws-lab/05-evidence-ledger.md) | [_structure-outline](02-terraform-aws-lab/_structure-outline.md) | [10-development-timeline](02-terraform-aws-lab/10-development-timeline.md) | `pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests` |
| 03 CloudTrail Log Basics | [00-series-map](03-cloudtrail-log-basics/00-series-map.md) | [05-evidence-ledger](03-cloudtrail-log-basics/05-evidence-ledger.md) | [_structure-outline](03-cloudtrail-log-basics/_structure-outline.md) | [10-development-timeline](03-cloudtrail-log-basics/10-development-timeline.md) | `pytest 00-aws-security-foundations/03-cloudtrail-log-basics/python/tests` |

## 읽을 때 먼저 볼 포인트

- 첫 프로젝트에서는 “설명 가능한 decision”이 어떤 모양으로 남는지 본다.
- 두 번째 프로젝트에서는 plan JSON이 왜 후속 스캐너 입력으로 쓰이게 되는지 본다.
- 세 번째 프로젝트에서는 log를 저장하는 것과 queryable하게 만드는 것이 어떻게 다른지 본다.

legacy 격리 원칙은 [`../_legacy/2026-03-13-isolate-and-rewrite/00-aws-security-foundations`](../_legacy/2026-03-13-isolate-and-rewrite/00-aws-security-foundations)에서 확인할 수 있다.
