# 04 IAM Policy Analyzer 근거 정리

allow/deny 평가를 끝내지 않고, least privilege 관점의 triage 가능한 finding으로 바꾸는 단계다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. finding 스키마를 먼저 고정했다

이 구간에서는 `finding 스키마를 먼저 고정했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: 정책 위험을 remediation과 이어질 수 있는 구조화된 finding으로 표현한다.
- 변경 단위: `python/src/iam_policy_analyzer/analyzer.py`의 `Finding` dataclass와 statement 순회
- 처음 가설: least privilege 분석은 “위험하다”는 말보다 `control_id`, `severity`, `resource_id`, `evidence_ref`를 먼저 정해야 나중 작업이 연결된다.
- 실제 조치: `Finding` dataclass를 도입하고, statement가 단일 dict이어도 list처럼 순회하게 정규화했다. 이 단계에서 이미 출력 shape가 remediation runner와 control plane이 재사용할 수 있는 수준으로 좁혀졌다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json`
- 검증 신호:
  - CLI가 `source`, `control_id`, `severity`, `resource_id`, `evidence_ref`를 포함한 JSON 배열을 돌려줬다.
  - README도 같은 필드 집합을 analyzer의 핵심 출력으로 설명한다.
- 핵심 코드 앵커: `01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py:23-47`
- 새로 배운 것: 보안 analyzer에서 중요한 것은 탐지 로직보다도 결과 shape다. 결과 shape가 triage와 remediation을 결정한다.
- 다음: 이제 broad permission을 한 덩어리로 보지 않고 서로 다른 control로 나눠야 했다.

## Phase 2. broad admin을 두 control로 분해했다

이 구간에서는 `broad admin을 두 control로 분해했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: `Action=*`와 `Resource=*`가 남기는 운영 질문을 분리한다.
- 변경 단위: `python/src/iam_policy_analyzer/analyzer.py`의 `IAM-001`, `IAM-002` 생성 로직
- 처음 가설: “너무 넓다”는 한 문장만으로는 remediation이 모호하다. 모든 action 허용과 모든 resource 적용은 수정 지점이 다르다.
- 실제 조치: `* in actions`면 `IAM-001`, `* in resources`면서 read-only가 아니면 `IAM-002`를 별도로 만들었다. broad admin fixture를 넣었을 때 두 finding이 같이 나와야 비로소 이후 조치안이 구체화된다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json`
- 검증 신호:
  - 실제 CLI 출력에 `IAM-001`, `IAM-002` 두 건이 동시에 나타났다.
  - BroadAdmin statement 하나가 두 remediation 질문을 낳는 구조가 만들어졌다.
- 핵심 코드 앵커: `01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py:48-72`
- 새로 배운 것: least privilege 위반은 하나의 범주가 아니다. action breadth와 resource breadth를 분리해야 실제 수정 전략이 보인다.
- 다음: 남은 문제는 `iam:PassRole` 같은 escalation action을 broad permission과 구분하는 일이었다.

## Phase 3. escalation action과 false positive 경계를 함께 고정했다

이 구간에서는 `escalation action과 false positive 경계를 함께 고정했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: 정책이 넓지 않더라도 privilege escalation 위험이 있는 경우를 별도 control로 잡고, safe fixture 0건도 확인한다.
- 변경 단위: `python/src/iam_policy_analyzer/analyzer.py`의 `HIGH_RISK_ACTIONS`, `python/tests/test_analyzer.py`
- 처음 가설: 정책이 `Action=*`가 아니어도 `iam:PassRole` 하나로 충분히 위험해질 수 있다. 반대로 scoped policy는 조용히 통과해야 한다.
- 실제 조치: `HIGH_RISK_ACTIONS` 집합을 두고 intersection이 있으면 `IAM-003`을 생성하게 했다. 테스트는 broad admin, passrole, scoped policy 0건 세 축을 동시에 고정해 analyzer의 경계를 명확히 했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests`
- 검증 신호:
  - pytest가 `3 passed in 0.02s`로 통과했다.
  - `test_scoped_policy_reports_no_findings`가 false positive를 막는 마지막 울타리가 됐다.
- 핵심 코드 앵커: `01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py:12-25`
- 새로 배운 것: 보안 rule의 품질은 탐지 개수보다 false positive 관리에 더 크게 좌우된다. 0건 fixture가 있어야 rule이 현실적이다.
- 다음: 이 finding 구조는 다음 프로젝트에서 multi-source CSPM rule engine과 remediation runner로 그대로 넘어간다.
