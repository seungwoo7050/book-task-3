# 디버그 로그

## 실제로 자주 막히는 지점

- `Action=*`와 `Resource=*`는 같은 broadness가 아닙니다. 같은 policy에서 둘 다 동시에 걸릴 수 있습니다.
- `Resource=*`라도 읽기 전용 액션만 있으면 고위험으로 보지 않는 필터가 필요합니다.
- escalation action은 broadness와 별개의 축입니다. `iam:PassRole` 하나만 있어도 high-risk로 보는 이유를 설명할 수 있어야 합니다.

## 이미 확인된 테스트 시나리오

- `test_broad_admin_policy_reports_multiple_findings`: 하나의 policy에서 `IAM-001`, `IAM-002`가 동시에 나오는지 확인합니다.
- `test_passrole_policy_reports_escalation_risk`: escalation action이 별도 규칙으로 분리되는지 확인합니다.
- `test_scoped_policy_reports_no_findings`: 오탐 방지 기준이 실제로 작동하는지 검증합니다.

## 다시 검증할 명령

```bash
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## 실패하면 먼저 볼 곳

- 테스트 코드: [../python/tests/test_analyzer.py](../python/tests/test_analyzer.py)
- 구현 진입점: [../python/src/iam_policy_analyzer/analyzer.py](../python/src/iam_policy_analyzer/analyzer.py)
- 이전 설명: [../notion-archive/essay.md](../notion-archive/essay.md)
