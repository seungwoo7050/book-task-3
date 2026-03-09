# Python Implementation

- Scope: policy JSON과 request JSON을 읽고 IAM-style allow/deny decision을 설명한다.
- Build: `PYTHONPATH=src python -m aws_security_primitives.cli explain <policy> <request>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: condition keys, principal evaluation, policy variables는 v1 범위 밖이다.

