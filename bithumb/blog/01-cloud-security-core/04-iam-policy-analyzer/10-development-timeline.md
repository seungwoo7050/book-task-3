# 04 IAM Policy Analyzer: allow/deny를 끝내지 않고 "왜 위험한가"를 control 단위로 잘라 낸 첫 analyzer

foundation 단계의 IAM 엔진은 "허용되었는가, 거부되었는가"를 설명하는 데 집중했다. 그런데 운영자가 실제로 궁금한 건 그다음 질문이다. 어떤 정책이 왜 위험하고, 무엇부터 고쳐야 하는가. `04-iam-policy-analyzer`는 바로 그 질문을 받는 첫 규칙 엔진이다. `2026-03-14`에 CLI와 pytest를 다시 돌려 보니, 이 프로젝트의 핵심은 많은 규칙을 넣은 데 있지 않고, broad permission과 escalation risk를 remediation-friendly finding 구조로 다시 자른 데 있었다.

## Step 1. 먼저 "분석 결과의 모양"부터 고정했다

이 analyzer가 가장 먼저 한 일은 위험 판단 로직이 아니라 결과 스키마를 정하는 것이었다. `Finding` dataclass는 아래 필드를 고정한다.

- `source`
- `control_id`
- `severity`
- `resource_type`
- `resource_id`
- `title`
- `evidence_ref`

이 순서가 중요한 이유는, 보안 analyzer는 한 번 탐지하고 끝나는 도구가 아니라 이후 remediation, 예외 관리, control plane까지 이어지는 중간 계층이기 때문이다. README가 "finding마다 `control_id`, `severity`, `resource_id`, `evidence_ref`를 반환"한다고 적는 말이 그냥 문서 주장인지 확인하려고 `2026-03-14`에 broad admin CLI를 다시 돌렸고, 실제 JSON 출력도 그 필드 집합을 그대로 내놨다.

```bash
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src \
  .venv/bin/python -m iam_policy_analyzer.cli \
  01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
```

즉 이 analyzer는 처음부터 "정책이 위험하다"는 문장형 보고서가 아니라, 다음 시스템이 재사용할 수 있는 구조화된 finding 배열을 목표로 삼는다.

## Step 2. broad admin을 하나의 문제로 뭉개지 않고 둘로 잘랐다

이 프로젝트의 가장 중요한 설계 선택은 broad permission을 한 control로 뭉개지 않았다는 점이다. `analyzer.py`는 broad admin을 최소 두 종류의 운영 질문으로 나눈다.

```python
if "*" in actions:
    findings.append(... control_id="IAM-001", title="Policy allows every action")

if "*" in resources and any(not action.startswith(READ_ONLY_PREFIXES) for action in actions):
    findings.append(... control_id="IAM-002", title="Policy applies to every resource")
```

이 분리는 `2026-03-14` broad admin fixture 재실행에서 그대로 확인됐다.

- broad admin CLI -> `IAM-001`
- broad admin CLI -> `IAM-002`

같은 `Sid=BroadAdmin`에서 두 finding이 같이 나오기 때문에, 운영자는 "모든 action 허용"을 줄일지, "모든 resource 적용"을 줄일지 두 방향의 remediation 질문을 따로 볼 수 있다. `docs/concepts/least-privilege-findings.md`가 broad admin을 `Action=*`와 `Resource=*`로 나눠 보는 편이 remediation에 유리하다고 적는 이유도 여기에 있다.

즉 이 analyzer의 첫 성취는 위험을 많이 잡아내는 것이 아니라, 위험을 고칠 수 있는 단위로 분해하는 데 있다.

## Step 3. escalation action은 broad permission과 별도 축으로 다뤘다

정책이 넓지 않아도 위험할 수 있다는 점을 보여 주는 게 세 번째 단계다. `HIGH_RISK_ACTIONS` 집합은 다음 action들을 escalation 후보로 고정한다.

- `iam:PassRole`
- `iam:CreatePolicyVersion`
- `iam:AttachUserPolicy`
- `iam:PutUserPolicy`
- `sts:AssumeRole`

그리고 action set이 이 집합과 교집합을 가지면 `IAM-003`을 만든다. `2026-03-14`에 `passrole_policy.json`을 다시 분석했을 때 실제 결과는 아래와 같았다.

- `IAM-002`
- `IAM-003`

즉 passrole fixture는 "모든 resource에 적용된다"는 broad resource 문제와, "권한 상승 경로를 포함한다"는 escalation 문제를 동시에 가진다. 이게 중요한 이유는 remediation 질문이 전혀 다르기 때문이다. resource scope를 좁히는 일과 `iam:PassRole` 자체를 제거하거나 제한하는 일은 서로 다른 작업이기 때문이다.

여기서 드러나는 현재 규칙의 한계도 있다. escalation 판정은 `HIGH_RISK_ACTIONS` 안의 exact action만 본다. 따라서 비슷한 맥락의 다른 위험 action이나 condition으로 좁혀진 위험은 아직 세밀하게 구분하지 않는다. 이 문장은 소스를 읽고 적은 source-based inference다.

## Step 4. safe policy에서 0건이 나오는 걸 품질 기준으로 삼았다

보안 규칙 엔진은 많이 잡는 것보다, 잡지 말아야 할 것을 얼마나 잘 지나치는지가 더 중요할 때가 많다. 이 프로젝트가 좋은 이유는 `scoped_policy.json`이 0건이어야 한다는 사실을 테스트에 포함했다는 점이다.

`2026-03-14` 재실행 결과는 명확했다.

- scoped CLI -> `[]`
- pytest -> `3 passed in 0.01s`

테스트는 세 축을 동시에 잠근다.

- broad admin -> `IAM-001`, `IAM-002`
- passrole -> `IAM-003`
- scoped read -> `[]`

즉 이 analyzer는 false positive를 줄이기 위해 최소한의 read-only prefix 개념(`s3:Get`, `s3:List`, `ec2:Describe`, `iam:Get`, `iam:List`)도 함께 둔다. broad resource 판정에서 이 prefix를 예외로 보는 것도 그래서다.

다만 이 경계 역시 아주 거칠다. 예를 들어 `s3:*`처럼 wildcard가 섞인 read-like family 전체를 읽기 전용으로 분류하지는 않는다. 지금은 exact prefix와 exact action set 중심의 v1 규칙 엔진이라고 보는 편이 맞다. 이것도 소스를 읽고 적은 source-based inference다.

## 정리

`04-iam-policy-analyzer`의 성취는 allow/deny를 더 복잡하게 만든 데 있지 않다. broad permission을 action breadth와 resource breadth로 나누고, escalation action을 별도 control로 떼고, safe policy 0건까지 품질 기준으로 묶어 "운영자가 바로 triage할 수 있는 finding 배열"로 바꿨다는 데 있다. 그래서 다음 remediation runner와 capstone은 정책 원문을 다시 해석하는 대신, 이미 잘린 finding 구조를 받아 후속 조치를 설계할 수 있다.
