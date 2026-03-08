# 05 CSPM Rule Engine

## Status

`verified`

## Problem Scope

- Terraform plan JSON misconfiguration 탐지
- selected resources encryption/KMS 검사
- access key age snapshot 검사

## Build

```bash
cd python
PYTHONPATH=src python -m cspm_rule_engine.cli ../problem/data/insecure_plan.json ../problem/data/access_keys_snapshot.json
```

## Test

```bash
cd study2
PYTHONPATH=01-cloud-security-core/05-cspm-rule-engine/python/src .venv/bin/python -m pytest 01-cloud-security-core/05-cspm-rule-engine/python/tests
```

## Learned

좋은 CSPM rule은 화려한 DSL보다 “입력 스키마가 명확하고 false positive가 적은가”가 더 중요하다.
