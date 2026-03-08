# Python Implementation

- Scope: IAM policy를 읽고 broad permission과 escalation 패턴을 finding으로 바꾼다.
- Build: `PYTHONPATH=src python -m iam_policy_analyzer.cli <policy.json>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: SCP, permission boundary, condition-based privilege narrowing은 v1 범위 밖이다.

