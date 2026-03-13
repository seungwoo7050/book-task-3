# 05 CSPM Rule Engine: plan과 snapshot에서 triage finding 뽑기

Terraform plan과 운영 snapshot을 함께 읽어 triage 가능한 misconfiguration finding으로 바꾸는 규칙 엔진이다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "Terraform plan에서 어떤 resource-level 규칙을 먼저 고정했는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. Terraform plan의 resource 목록을 기준으로 S3 public access, open ingress, encryption 규칙을 구현했다.
2. 운영 snapshot 쪽에서는 access key age 규칙을 별도로 추가해 plan-only 스캐너를 넘어서게 했다.
3. secure fixture 0건과 output schema를 테스트로 잠가 triage 가능한 engine으로 마감했다.

## Phase 1. Terraform plan 규칙부터 세웠다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `Terraform plan 규칙부터 세웠다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 정적 plan JSON만으로 설명 가능한 misconfiguration을 먼저 잡는다.
- 변경 단위: `python/src/cspm_rule_engine/scanner.py`의 `_resources`, `scan_plan`
- 처음 가설: 좋은 CSPM v1은 규칙 수를 늘리기보다 입력 스키마가 선명한 몇 개 규칙을 정확히 잡는 쪽이 낫다.
- 실제 진행: `planned_values.root_module.resources`를 읽는 helper를 만들고, S3 public access block 플래그, SSH/RDP 0.0.0.0/0 ingress, storage encryption 비활성화를 각각 다른 control로 매핑했다. 각 finding에는 `evidence_ref`와 `resource_id`를 남겨 triage를 바로 이어갈 수 있게 했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
```

검증 신호:
- CLI 출력에 `CSPM-001`, `CSPM-002`, `CSPM-003`이 한 번에 나타났다.
- `study2-public-logs`, `ssh_open`, `study2-analytics`처럼 remediation에 바로 쓸 resource_id가 남았다.

핵심 코드:

```python
def scan_plan(plan_payload: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for resource in _resources(plan_payload):
        resource_type = str(resource["type"])
        name = str(resource["name"])
        values = dict(resource.get("values", {}))

        if resource_type == "aws_s3_bucket_public_access_block":
            flags = (
                values.get("block_public_acls"),
                values.get("block_public_policy"),
                values.get("ignore_public_acls"),
                values.get("restrict_public_buckets"),
            )
            if not all(flags):
                findings.append(
                    Finding(
                        source="terraform-plan",
                        control_id="CSPM-001",
                        severity="HIGH",
                        resource_type=resource_type,
                        resource_id=str(values.get("bucket", name)),
                        title="S3 bucket does not fully block public access",
                        evidence_ref=name,
                    )
                )

        if resource_type == "aws_security_group":
            for ingress in values.get("ingress", []):
                port = int(ingress.get("from_port", -1))
                cidrs = ingress.get("cidr_blocks", [])
                if port in {22, 3389} and "0.0.0.0/0" in cidrs:
                    findings.append(
                        Finding(
                            source="terraform-plan",
                            control_id="CSPM-002",
                            severity="HIGH",
                            resource_type=resource_type,
                            resource_id=name,
                            title="Security group exposes SSH or RDP to the internet",
                            evidence_ref=name,
                        )
                    )

        if resource_type in {"aws_db_instance", "aws_ebs_volume"} and values.get("storage_encrypted") is False:
            findings.append(
                Finding(
                    source="terraform-plan",
                    control_id="CSPM-003",
                    severity="MEDIUM",
                    resource_type=resource_type,
                    resource_id=str(values.get("identifier", name)),
                    title="Resource encryption is disabled",
                    evidence_ref=name,
                )
            )
    return findings
```

왜 이 코드가 중요했는가: 이 루프가 프로젝트의 핵심이었다. plan JSON에서 resource type을 읽고 control을 붙이는 패턴이 생기면서, CSPM이 “제품”이 아니라 “설명 가능한 rule 묶음”으로 보이기 시작했다.

새로 배운 것: 좋은 rule은 왜 발동했는지를 운영자가 바로 이해할 수 있어야 한다. input schema가 명확해야 false positive도 줄어든다.

다음: 이제 CSPM을 static plan에만 가두지 않고, 운영 snapshot까지 확장해 볼 차례였다.

## Phase 2. access key snapshot으로 입력 범위를 넓혔다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `access key snapshot으로 입력 범위를 넓혔다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: CSPM이 선언형 plan만 읽는 정적 분석에 머무르지 않도록 한다.
- 변경 단위: `python/src/cspm_rule_engine/scanner.py`의 `scan_access_keys`
- 처음 가설: 실무의 CSPM은 plan만으로 끝나지 않는다. 계정 상태 snapshot 같은 운영 데이터도 같은 finding shape로 묶어야 한다.
- 실제 진행: snapshot payload의 `access_keys`를 순회하면서 age가 90일을 넘으면 `CSPM-004`를 추가했다. source만 `access-key-snapshot`으로 다르게 주고, 나머지 필드는 plan findings와 같은 구조를 유지했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
```

검증 신호:
- CLI 출력 마지막에 `CSPM-004`와 `AKIAOLD123`가 나타났다.
- 같은 JSON 배열 안에 `terraform-plan` source와 `access-key-snapshot` source가 함께 들어갔다.

핵심 코드:

```python
def scan_access_keys(snapshot_payload: dict[str, Any], max_age_days: int = 90) -> list[Finding]:
    findings: list[Finding] = []
    for entry in snapshot_payload.get("access_keys", []):
        if int(entry["age_days"]) > max_age_days:
            findings.append(
                Finding(
                    source="access-key-snapshot",
                    control_id="CSPM-004",
                    severity="MEDIUM",
                    resource_type="iam-access-key",
                    resource_id=str(entry["access_key_id"]),
                    title="IAM access key age exceeds threshold",
                    evidence_ref=str(entry["user"]),
                )
            )
    return findings
```

왜 이 코드가 중요했는가: 이 함수가 생기면서 engine은 단일 parser가 아니라 multi-source scanner가 됐다. source가 달라도 결과 shape가 같다는 점이 중요했다.

새로 배운 것: CSPM의 가치는 입력 종류를 늘리는 데 있는 게 아니라, 서로 다른 입력을 같은 triage 언어로 묶는 데 있다.

다음: 이제 secure fixture 0건과 output consistency를 테스트로 잠가 rule 품질을 고정해야 했다.

## Phase 3. secure fixture 0건을 품질 기준으로 삼았다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `secure fixture 0건을 품질 기준으로 삼았다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 불필요한 finding이 나오지 않는 기준선을 만든다.
- 변경 단위: `python/tests/test_scanner.py`
- 처음 가설: insecure fixture에서 많이 잡는 것보다 secure fixture에서 조용해야 rule engine이 실제로 쓸 만하다.
- 실제 진행: 테스트는 insecure plan에서 세 control이 모두 나오는지, secure plan에서는 0건인지, access key snapshot에서는 오래된 키 한 건만 잡히는지 확인했다. 이 세 축이 있어야 ruleset이 과하게 noisy해지지 않는다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

검증 신호:
- pytest가 `3 passed in 0.01s`로 통과했다.
- `test_secure_plan_reports_no_findings`가 ruleset의 상한선을 정했다.

핵심 코드:

```python
def test_insecure_plan_reports_expected_findings() -> None:
    findings = scan_plan(_data("insecure_plan.json"))
    controls = {finding.control_id for finding in findings}
    assert controls == {"CSPM-001", "CSPM-002", "CSPM-003"}


def test_secure_plan_reports_no_findings() -> None:
    findings = scan_plan(_data("secure_plan.json"))
    assert findings == []


def test_access_key_snapshot_reports_old_key() -> None:
    findings = scan_access_keys(_data("access_keys_snapshot.json"))
    assert len(findings) == 1
    assert findings[0].control_id == "CSPM-004"
```

왜 이 코드가 중요했는가: 규칙 엔진의 설득력은 여기서 결정됐다. secure fixture를 통과하지 못하면 rule이 아무리 많아도 운영에선 쓰기 어렵다.

새로 배운 것: false positive는 rule 수보다 input 경계가 흐릴 때 생기기 쉽다. secure fixture는 그 경계를 테스트 코드로 고정하는 장치다.

다음: 다음 프로젝트는 이 finding을 바로 실행하지 않고, review 가능한 remediation plan으로 바꾼다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 엔진은 plan parser를 늘어놓는 데서 멈추지 않고, 서로 다른 입력을 같은 finding 언어로 묶었다. 그래서 다음 remediation runner와 capstone이 source가 다른 finding도 같은 절차로 다룰 수 있었다.
