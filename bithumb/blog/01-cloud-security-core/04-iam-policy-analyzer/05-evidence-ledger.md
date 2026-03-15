# 04 IAM Policy Analyzer evidence ledger

- 복원 원칙: 기존 blog 본문은 제외하고 `README/problem/docs`, analyzer 소스, fixture policy, CLI, pytest 재실행 결과만 근거로 썼다.
- 날짜 고정: 아래 실행 결과는 `2026-03-14` 기준이다.
- 프로젝트 성격: 이 analyzer의 출력은 remediation runner와 capstone이 그대로 재사용할 수 있는 finding 배열이다.

## 사용한 입력 근거

- 설명 문서
  - `README.md`
  - `problem/README.md`
  - `python/README.md`
  - `docs/concepts/least-privilege-findings.md`
- 구현
  - `python/src/iam_policy_analyzer/analyzer.py`
  - `python/src/iam_policy_analyzer/cli.py`
  - `problem/data/broad_admin_policy.json`
  - `problem/data/passrole_policy.json`
  - `problem/data/scoped_policy.json`
- 테스트
  - `python/tests/test_analyzer.py`

## 다시 실행한 명령

```bash
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src \
  .venv/bin/python -m iam_policy_analyzer.cli \
  01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json

PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src \
  .venv/bin/python -m iam_policy_analyzer.cli \
  01-cloud-security-core/04-iam-policy-analyzer/problem/data/passrole_policy.json

PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src \
  .venv/bin/python -m iam_policy_analyzer.cli \
  01-cloud-security-core/04-iam-policy-analyzer/problem/data/scoped_policy.json

PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src \
  .venv/bin/python -m pytest \
  01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## 재실행 결과

- broad admin CLI -> `IAM-001`, `IAM-002`
- passrole CLI -> `IAM-002`, `IAM-003`
- scoped CLI -> `[]`
- pytest -> `3 passed in 0.01s`

## 단계별 근거

### 1. finding shape를 먼저 고정했다

- 근거 소스: `analyzer.py`
- 확인한 사실:
  - 출력은 `source`, `control_id`, `severity`, `resource_type`, `resource_id`, `title`, `evidence_ref` 필드로 고정된다.
  - `Statement`가 dict이어도 list처럼 순회한다.
  - `Effect != Allow`면 해당 statement는 즉시 건너뛴다.

### 2. broad permission을 두 종류로 분해했다

- 근거 소스: `analyzer.py`, `broad_admin_policy.json`, broad admin CLI 출력
- 확인한 사실:
  - `Action == "*"`이면 `IAM-001`이 생긴다.
  - `Resource == "*"`이면서 action이 read-only prefix가 아니면 `IAM-002`가 생긴다.
  - broad admin fixture는 같은 `Sid=BroadAdmin`에서 두 finding을 동시에 낸다.

### 3. escalation을 별도 control로 분리하고 false positive 0건을 유지했다

- 근거 소스: `HIGH_RISK_ACTIONS`, `passrole_policy.json`, `scoped_policy.json`, pytest
- 확인한 사실:
  - `iam:PassRole`, `iam:CreatePolicyVersion`, `iam:AttachUserPolicy`, `iam:PutUserPolicy`, `sts:AssumeRole`는 `IAM-003` 대상이다.
  - passrole fixture는 resource가 `*`라서 `IAM-002`와 `IAM-003`가 같이 나온다.
  - scoped read fixture는 finding이 0건이다.

## 남은 한계

- `problem/README.md`가 명시한 대로 SCP, permission boundary, condition-based narrowing은 다루지 않는다.
- broad action 판정은 exact `"*"`만 본다. 예를 들어 `s3:*` 같은 wildcard family 전체를 별도 broad action으로 분류하지는 않는다. 이 문장은 `analyzer.py` 소스를 읽고 적은 source-based inference다.
- high-risk escalation 판정도 `HIGH_RISK_ACTIONS`에 있는 exact action 집합 기준이다.
