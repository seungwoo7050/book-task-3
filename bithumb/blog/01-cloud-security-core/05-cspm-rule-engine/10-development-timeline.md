# 10 Development Timeline

이 문서는 `CSPM Rule Engine`을 현재 plan fixture, snapshot fixture, 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 Terraform 정적 분석만 하는지, 아니면 운영 snapshot까지 같이 보는지 실제 소스에서 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `scanner.py`, `test_scanner.py`를 함께 읽었다.
- 이슈: 처음엔 plan JSON 규칙만 있을 거라 생각했는데, `scan_access_keys()`가 따로 있어서 계정 수명주기까지 같은 finding 구조로 묶고 있었다.
- 판단: 이 프로젝트의 중심은 규칙 수를 늘리는 게 아니라, 서로 다른 입력 소스를 `Finding` 하나로 정규화해 후속 remediation과 capstone이 쉽게 재사용하도록 만드는 데 있다.

CLI:

```bash
$ sed -n '1,120p' 01-cloud-security-core/05-cspm-rule-engine/problem/README.md
$ sed -n '1,260p' 01-cloud-security-core/05-cspm-rule-engine/python/src/cspm_rule_engine/scanner.py
$ sed -n '1,200p' 01-cloud-security-core/05-cspm-rule-engine/python/tests/test_scanner.py
```

이 시점의 핵심 코드는 public access block 플래그 네 개를 한 번에 묶어 보는 부분이었다.

```python
            flags = (
                values.get("block_public_acls"),
                values.get("block_public_policy"),
                values.get("ignore_public_acls"),
                values.get("restrict_public_buckets"),
            )
            if not all(flags):
                findings.append(Finding(... control_id="CSPM-001", ...))
```

처음엔 S3 public access를 ACL 하나만 보면 된다고 생각했지만, 실제 코드와 fixture를 대조해 보니 네 플래그를 모두 묶어야 `study2-public-logs` 버킷을 안전하다고 말할 수 있다. 이 조각이 중요한 이유는 “하나라도 빠지면 위험”이라는 기준을 가장 짧게 보여 주기 때문이다.

### Session 2

- 진행: insecure plan + access key snapshot CLI, pytest를 다시 돌려 current output을 확인했다.
- 검증: CLI는 `CSPM-001`, `CSPM-002`, `CSPM-003`, `CSPM-004` 네 finding을 반환했고, 테스트는 insecure/secure/snapshot 세 경로를 모두 통과했다.
- 판단: 처음 가설은 secure fixture 검증이 부가적이라는 쪽이었지만, `test_secure_plan_reports_no_findings()`가 있어야 규칙 엔진이 데모용 과탐지기로 기울지 않는다.
- 다음: 06번 runner는 여기서 나온 `control_id`를 기준으로 auto patch, manual approval, manual review를 나눈다.

CLI:

```bash
$ make venv
$ PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m cspm_rule_engine.cli 01-cloud-security-core/05-cspm-rule-engine/problem/data/insecure_plan.json 01-cloud-security-core/05-cspm-rule-engine/problem/data/access_keys_snapshot.json
$ PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

출력:

```text
"control_id": "CSPM-001"
"control_id": "CSPM-004"
3 passed in 0.01s
```
