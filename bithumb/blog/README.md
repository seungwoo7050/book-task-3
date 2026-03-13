# Bithumb Cloud Security Blog 읽기 안내

이 디렉터리는 AWS-first cloud security track을 프로젝트 단위로 다시 읽는 blog 모음이다. 결과만 훑는 회고가 아니라, 어떤 입력을 먼저 고정하고 어떤 검증으로 다음 단계로 넘어갔는지를 차례대로 따라가게 만드는 것이 목표다.

이번 리라이트에서는 문장을 조금 더 부드럽게 다듬고, legacy 격리 같은 메타 설명은 여기와 트랙 README에 모아 두었다. 예전 초안은 [`_legacy/2026-03-13-isolate-and-rewrite`](_legacy/2026-03-13-isolate-and-rewrite)에 보관해 두었고, 현재 활성 문서는 소스코드, README, docs, 테스트, CLI를 중심으로 읽는다.

## 이렇게 읽으면 덜 막힌다

1. 루트에서 트랙을 고른 뒤, 해당 트랙 README로 들어가 프로젝트 순서를 먼저 잡는다.
2. 각 프로젝트에서는 `00-series-map.md`를 먼저 열어 어떤 질문을 들고 읽으면 좋은지 확인한다.
3. `05-evidence-ledger.md`와 `_structure-outline.md`로 근거와 서사 배치를 짧게 훑는다.
4. 마지막으로 `10-development-timeline.md`를 읽으면 phase별 판단 이동이 훨씬 자연스럽게 들어온다.

## 트랙별 입구

| 트랙 | 설명 | 프로젝트 수 |
| --- | --- | --- |
| [00 AWS Security Foundations](00-aws-security-foundations/README.md) | IAM, Terraform, CloudTrail처럼 이후 스캐너가 기대는 입력 계약을 먼저 고정한다. | 3 |
| [01 Cloud Security Core](01-cloud-security-core/README.md) | finding, remediation, detection, governance를 서로 다른 작은 프로젝트로 확장한다. | 6 |
| [02 Capstone](02-capstone/README.md) | 앞선 판단 로직을 API, worker, report, demo asset까지 이어지는 control plane으로 묶는다. | 1 |

## 문서 역할

- `00-series-map.md`: 이 프로젝트를 왜 읽어야 하는지와 어떤 질문을 붙들어야 하는지 안내하는 입구
- `05-evidence-ledger.md`: 본문으로 들어가기 전에 phase별 근거를 빠르게 훑는 정리 문서
- `_structure-outline.md`: 최종 글이 어떤 순서와 강조점으로 배치됐는지 보여 주는 구조 메모
- `10-development-timeline.md`: 코드, CLI, 개념 설명을 묶어 실제 구현 흐름을 따라가는 본문
