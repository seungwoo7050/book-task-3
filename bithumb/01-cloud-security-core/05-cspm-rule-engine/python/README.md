# Python Implementation

- Scope: Terraform plan JSON과 access key snapshot을 읽고 CSPM finding을 생성한다.
- Build: `PYTHONPATH=src python -m cspm_rule_engine.cli <plan.json> <access_keys.json>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: v1 rule set은 S3/SG/encryption/access key age로 제한한다.

