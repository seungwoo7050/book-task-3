# 04 IAM Policy Analyzer: allow/deny를 risk finding으로 바꾸기

allow/deny 평가를 끝내지 않고, least privilege 관점의 triage 가능한 finding으로 바꾸는 단계다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "왜 allow/deny 결과 위에 finding 구조를 한 겹 더 얹어야 했는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. policy statement를 순회하면서 재사용 가능한 `Finding` 구조를 먼저 세웠다.
2. `Action=*`와 `Resource=*`를 서로 다른 control로 분리해 broad permission을 세분화했다.
3. `iam:PassRole` 같은 escalation action을 별도 control로 떼고, scoped policy 0건 테스트로 false positive를 막았다.

## Phase 1. finding 스키마를 먼저 고정했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `finding 스키마를 먼저 고정했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 정책 위험을 remediation과 이어질 수 있는 구조화된 finding으로 표현한다.
- 변경 단위: `python/src/iam_policy_analyzer/analyzer.py`의 `Finding` dataclass와 statement 순회
- 처음 가설: least privilege 분석은 “위험하다”는 말보다 `control_id`, `severity`, `resource_id`, `evidence_ref`를 먼저 정해야 나중 작업이 연결된다.
- 실제 진행: `Finding` dataclass를 도입하고, statement가 단일 dict이어도 list처럼 순회하게 정규화했다. 이 단계에서 이미 출력 shape가 remediation runner와 control plane이 재사용할 수 있는 수준으로 좁혀졌다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
```

검증 신호:
- CLI가 `source`, `control_id`, `severity`, `resource_id`, `evidence_ref`를 포함한 JSON 배열을 돌려줬다.
- README도 같은 필드 집합을 analyzer의 핵심 출력으로 설명한다.

핵심 코드:

```python
@dataclass(slots=True)
class Finding:
    source: str
    control_id: str
    severity: str
    resource_type: str
    resource_id: str
    title: str
    evidence_ref: str


def analyze_policy(policy: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    statements = policy.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]

    for index, statement in enumerate(statements, start=1):
        sid = str(statement.get("Sid", f"Statement{index}"))
        effect = str(statement.get("Effect", "Deny"))
        if effect != "Allow":
            continue
        actions = _as_list(statement.get("Action", []))
        resources = _as_list(statement.get("Resource", []))

```

왜 이 코드가 중요했는가: finding 구조를 먼저 정한 덕분에 이후 규칙 추가가 “이 action이 위험한가?”에 집중될 수 있었다. 출력 schema가 뒤늦게 흔들리지 않았다.

새로 배운 것: 보안 analyzer에서 중요한 것은 탐지 로직보다도 결과 shape다. 결과 shape가 triage와 remediation을 결정한다.

다음: 이제 broad permission을 한 덩어리로 보지 않고 서로 다른 control로 나눠야 했다.

## Phase 2. broad admin을 두 control로 분해했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `broad admin을 두 control로 분해했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: `Action=*`와 `Resource=*`가 남기는 운영 질문을 분리한다.
- 변경 단위: `python/src/iam_policy_analyzer/analyzer.py`의 `IAM-001`, `IAM-002` 생성 로직
- 처음 가설: “너무 넓다”는 한 문장만으로는 remediation이 모호하다. 모든 action 허용과 모든 resource 적용은 수정 지점이 다르다.
- 실제 진행: `* in actions`면 `IAM-001`, `* in resources`면서 read-only가 아니면 `IAM-002`를 별도로 만들었다. broad admin fixture를 넣었을 때 두 finding이 같이 나와야 비로소 이후 조치안이 구체화된다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
```

검증 신호:
- 실제 CLI 출력에 `IAM-001`, `IAM-002` 두 건이 동시에 나타났다.
- BroadAdmin statement 하나가 두 remediation 질문을 낳는 구조가 만들어졌다.

핵심 코드:

```python
        if "*" in actions:
            findings.append(
                Finding(
                    source="iam-policy",
                    control_id="IAM-001",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy allows every action",
                    evidence_ref=sid,
                )
            )

        if "*" in resources and any(not action.startswith(READ_ONLY_PREFIXES) for action in actions):
            findings.append(
                Finding(
                    source="iam-policy",
                    control_id="IAM-002",
                    severity="HIGH",
                    resource_type="iam-policy",
                    resource_id=sid,
                    title="Policy applies to every resource",
                    evidence_ref=sid,
                )
            )
```

왜 이 코드가 중요했는가: 이 분기가 들어가면서 analyzer는 단순 lint가 아니라 triage 도구가 됐다. 무엇이 넓은지 종류를 나눠야 조치 우선순위도 달라진다.

새로 배운 것: least privilege 위반은 하나의 범주가 아니다. action breadth와 resource breadth를 분리해야 실제 수정 전략이 보인다.

다음: 남은 문제는 `iam:PassRole` 같은 escalation action을 broad permission과 구분하는 일이었다.

## Phase 3. escalation action과 false positive 경계를 함께 고정했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `escalation action과 false positive 경계를 함께 고정했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 정책이 넓지 않더라도 privilege escalation 위험이 있는 경우를 별도 control로 잡고, safe fixture 0건도 확인한다.
- 변경 단위: `python/src/iam_policy_analyzer/analyzer.py`의 `HIGH_RISK_ACTIONS`, `python/tests/test_analyzer.py`
- 처음 가설: 정책이 `Action=*`가 아니어도 `iam:PassRole` 하나로 충분히 위험해질 수 있다. 반대로 scoped policy는 조용히 통과해야 한다.
- 실제 진행: `HIGH_RISK_ACTIONS` 집합을 두고 intersection이 있으면 `IAM-003`을 생성하게 했다. 테스트는 broad admin, passrole, scoped policy 0건 세 축을 동시에 고정해 analyzer의 경계를 명확히 했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

검증 신호:
- pytest가 `3 passed in 0.02s`로 통과했다.
- `test_scoped_policy_reports_no_findings`가 false positive를 막는 마지막 울타리가 됐다.

핵심 코드:

```python
def test_broad_admin_policy_reports_multiple_findings() -> None:
    findings = analyze_policy(_policy("broad_admin_policy.json"))
    controls = {finding.control_id for finding in findings}
    assert controls == {"IAM-001", "IAM-002"}


def test_passrole_policy_reports_escalation_risk() -> None:
    findings = analyze_policy(_policy("passrole_policy.json"))
    assert any(finding.control_id == "IAM-003" for finding in findings)


def test_scoped_policy_reports_no_findings() -> None:
    findings = analyze_policy(_policy("scoped_policy.json"))
    assert findings == []
```

왜 이 코드가 중요했는가: 위험 탐지는 많이 잡는 것보다, 어떤 경우엔 조용히 지나가야 하는지까지 코드로 남길 때 비로소 믿을 수 있다. 이 테스트가 analyzer의 성격을 정했다.

새로 배운 것: 보안 rule의 품질은 탐지 개수보다 false positive 관리에 더 크게 좌우된다. 0건 fixture가 있어야 rule이 현실적이다.

다음: 이 finding 구조는 다음 프로젝트에서 multi-source CSPM rule engine과 remediation runner로 그대로 넘어간다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 analyzer는 policy 평가를 더 복잡하게 만든 것이 아니라, remediation과 연결될 수 있는 단위로 다시 잘랐다. broad permission의 종류를 나누고, escalation action을 따로 떼고, safe fixture 0건을 지키는 순서가 있었기 때문에 이후 프로젝트들이 이 출력을 그대로 재사용할 수 있었다.
