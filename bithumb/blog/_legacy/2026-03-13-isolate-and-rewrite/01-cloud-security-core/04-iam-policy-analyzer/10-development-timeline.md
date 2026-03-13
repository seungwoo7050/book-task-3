# 10 Development Timeline

이 문서는 `IAM Policy Analyzer`를 현재 policy fixture와 테스트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 01번 프로젝트의 allow/deny 감각이 여기서 어떻게 위험 finding으로 바뀌는지 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `test_analyzer.py`, `analyzer.py`를 같이 읽었다.
- 이슈: 처음엔 전체 policy evaluator를 그대로 재사용하는 프로젝트라고 생각했는데, 실제 코드는 훨씬 더 좁게 `Allow` statement와 위험 패턴 몇 가지에만 집중하고 있었다.
- 판단: 이 프로젝트의 역할은 완전한 권한 추론이 아니라, 운영자가 바로 triage할 수 있는 high-signal finding을 빠르게 만드는 데 있다.

CLI:

```bash
$ sed -n '1,120p' 01-cloud-security-core/04-iam-policy-analyzer/problem/README.md
$ sed -n '1,220p' 01-cloud-security-core/04-iam-policy-analyzer/python/src/iam_policy_analyzer/analyzer.py
$ sed -n '1,200p' 01-cloud-security-core/04-iam-policy-analyzer/python/tests/test_analyzer.py
```

이 시점의 핵심 코드는 broad admin과 resource scope를 별도 finding으로 나누는 부분이었다.

```python
        if "*" in actions:
            findings.append(Finding(... control_id="IAM-001", title="Policy allows every action", ...))

        if "*" in resources and any(not action.startswith(READ_ONLY_PREFIXES) for action in actions):
            findings.append(Finding(... control_id="IAM-002", title="Policy applies to every resource", ...))
```

처음엔 `* action` 하나만 잡아도 충분하다고 생각했지만, 실제로는 `* resource`를 별도 finding으로 분리해야 remediation 우선순위와 설명 문장이 훨씬 자연스러워진다. 이 구분 덕분에 같은 policy에서도 위험의 종류를 다른 control ID로 말할 수 있다.

### Session 2

- 진행: CLI와 pytest를 돌려 broad admin, passrole, scoped policy 세 기준선이 현재도 유지되는지 확인했다.
- 검증: broad admin CLI는 `IAM-001`, `IAM-002` 두 finding을 반환했고, 테스트는 `IAM-003` escalation과 0건 policy까지 포함해 3개를 모두 통과했다.
- 판단: 처음 가설은 `iam:PassRole`도 broad admin의 일부라고 보는 쪽이었지만, 별도 테스트가 있어서 privilege escalation 성격을 따로 설명해야 한다는 점이 분명해졌다.
- 다음: 10번 capstone은 여기서 만든 finding 모양을 거의 그대로 받아서 scan worker 결과로 저장한다.

CLI:

```bash
$ make venv
$ PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m iam_policy_analyzer.cli 01-cloud-security-core/04-iam-policy-analyzer/problem/data/broad_admin_policy.json
$ PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

출력:

```text
"control_id": "IAM-001"
"control_id": "IAM-002"
3 passed in 0.01s
```
