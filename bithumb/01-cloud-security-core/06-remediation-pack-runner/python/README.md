# Python Implementation

- Scope: finding을 remediation dry-run 계획으로 바꾼다.
- Build: `PYTHONPATH=src python -m remediation_pack_runner.cli <finding.json>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: 실제 apply는 하지 않는다.

