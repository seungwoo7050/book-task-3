# 06 Remediation Pack Runner

## Status

`verified`

## Problem Scope

- finding에 대한 dry-run remediation 생성
- manual approval required 여부 표시
- Terraform patch / AWS CLI manual command 제안

## Build

```bash
cd python
PYTHONPATH=src python -m remediation_pack_runner.cli ../problem/data/sample_finding.json
```

## Test

```bash
cd study2
PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```
