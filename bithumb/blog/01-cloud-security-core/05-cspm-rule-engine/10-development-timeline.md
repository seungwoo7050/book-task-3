# 05 CSPM Rule Engine: plan과 snapshot을 같은 triage 언어로 묶은 첫 multi-source scanner

이 프로젝트가 의미 있는 이유는 CSPM을 막연한 제품명이 아니라, 입력이 다른 위험 신호들을 같은 finding 구조로 정리하는 규칙 엔진으로 보여 주기 때문이다. `problem/README.md`가 말하듯 핵심은 규칙 개수를 늘리는 것이 아니라 입력 스키마와 출력 구조를 분명하게 만드는 일이다. `2026-03-14`에 CLI와 pytest를 다시 돌려 보니, 이 engine은 plan misconfiguration과 aged access key를 같은 JSON 배열에 담는 순간부터 다음 remediation 단계와 자연스럽게 이어졌다.

## Step 1. 먼저 Terraform plan 안의 resource를 control 단위로 분기했다

`scan_plan()`은 복잡한 graph traversal부터 시작하지 않는다. `_resources()`로 `planned_values.root_module.resources`를 꺼내고, resource type 기준으로 rule을 분기한다. 이 단순한 구조 덕분에 왜 어떤 finding이 나왔는지 소스에서 바로 따라갈 수 있다.

`2026-03-14`에 insecure plan fixture를 다시 보면, rule이 보는 차이는 분명했다.

- S3 public access block 네 플래그 모두 `false`
- security group ingress가 `22`와 `0.0.0.0/0`
- DB `storage_encrypted = false`

`scan_plan()`은 이 세 경우를 각각 다른 control로 만든다.

- `CSPM-001`: S3 bucket does not fully block public access
- `CSPM-002`: Security group exposes SSH or RDP to the internet
- `CSPM-003`: Resource encryption is disabled

즉 이 엔진은 "이 plan이 안전한가?"를 한 번에 묻지 않고, 운영자가 따로 조치할 수 있는 세 질문으로 위험을 분해한다. broad finding을 잘게 쪼개 remediation-friendly하게 만든다는 점에서 앞선 IAM analyzer와 결이 같다.

## Step 2. 그리고 access key snapshot을 같은 finding 배열에 합쳤다

이 프로젝트가 plan parser를 넘어서 CSPM engine처럼 보이는 지점은 `scan_access_keys()`다. snapshot payload의 `access_keys`를 순회하면서 `age_days > 90`이면 `CSPM-004`를 추가한다.

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
```

`2026-03-14` CLI 재실행 결과는 이 multi-source 구조를 그대로 보여 줬다.

```bash
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src \
  .venv/bin/python -m cspm_rule_engine.cli \
  01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json \
  01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
```

출력에는 아래 네 control이 같이 들어 있었다.

- `CSPM-001`
- `CSPM-002`
- `CSPM-003`
- `CSPM-004`

그리고 마지막 finding은 `resource_id = AKIAOLD123`, `evidence_ref = devops`였다. 즉 source는 달라도 triage 언어는 하나로 유지된다. 이게 다음 remediation runner와 capstone이 이 출력을 그대로 재사용할 수 있는 이유다.

## Step 3. secure plan 0건을 품질 기준으로 삼되, combined CLI와 혼동하지 않았다

이 프로젝트에서 가장 헷갈리기 쉬운 부분은 "secure fixture에서 0건"이라는 말이 정확히 어디까지를 뜻하는가다. `test_scanner.py`는 세 가지를 따로 잠근다.

- insecure plan -> `CSPM-001`, `CSPM-002`, `CSPM-003`
- secure plan -> `[]`
- access key snapshot -> `CSPM-004` 한 건

즉 secure 0건은 `scan_plan(secure_plan)` 기준의 말이다. 반면 CLI는 항상 아래처럼 두 출력을 합친다.

```python
findings = scan_plan(plan) + scan_access_keys(snapshot)
```

그래서 secure plan에 같은 aged access key snapshot을 넣으면 plan layer는 깨끗해도 combined CLI 전체는 여전히 `CSPM-004`를 낸다. 이 차이는 `2026-03-14`에 소스와 테스트 구조를 같이 확인하면서 더 선명해졌다. 즉 "secure fixture 0건"은 전체 입력 묶음이 0건이라는 뜻이 아니라, plan rule set의 false positive 기준이라는 뜻이다. 이 문장은 테스트와 CLI 소스를 함께 본 source-based inference다.

이 구분을 문서에 남겨 두는 이유는, 그렇지 않으면 사용자가 secure plan CLI 결과에 aged key finding이 나왔을 때 engine이 모순된다고 오해하기 쉽기 때문이다.

## Step 4. v1의 입력 범위는 분명하지만 좁다

현재 scanner의 장점은 규칙이 설명 가능하다는 점이고, 동시에 한계도 선명하다.

- `_resources()`는 root module resource만 읽는다.
- nested module resource는 현재 ruleset 대상이 아니다.
- encryption 규칙은 `aws_db_instance`와 `aws_ebs_volume`만 본다.
- key-age는 single snapshot 기준으로만 판단한다.

즉 이 engine은 실제 CSPM 제품 전체를 흉내 내는 것이 아니라, local fixture에서 재현 가능한 위험 규칙 네 개를 같은 finding shape로 묶는 데 집중한다. `docs/concepts/rule-design.md`가 말하는 "좋은 rule은 설명 가능해야 하고 false positive를 줄여야 한다"는 기준을 충실히 따른 v1 규칙 세트라고 보는 편이 맞다.

## 정리

`05-cspm-rule-engine`의 성취는 rule을 많이 넣은 데 있지 않다. plan resource rule 세 개와 snapshot rule 하나를 같은 finding 배열에 묶고, secure plan 0건을 품질 기준으로 잠가 "multi-source triage engine"으로 성격을 바꿨다는 데 있다. 그래서 다음 remediation runner는 source가 Terraform이든 snapshot이든 상관없이 같은 control ID와 evidence shape를 받아 후속 조치를 설계할 수 있다.
