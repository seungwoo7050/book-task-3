# 04 IAM Policy Analyzer

## Status

`verified`

## Problem Scope

- wildcard action/resource 탐지
- privilege escalation 가능성이 큰 action set 탐지
- 공통 `Finding` 포맷 출력

## Build

```bash
cd python
PYTHONPATH=src python -m iam_policy_analyzer.cli ../problem/data/broad_admin_policy.json
```

## Test

```bash
cd study2
PYTHONPATH=01-cloud-security-core/04-iam-policy-analyzer/python/src .venv/bin/python -m pytest 01-cloud-security-core/04-iam-policy-analyzer/python/tests
```

## Learned

IAM policy의 위험성은 “문법이 맞냐”보다 “권한 범위가 얼마나 넓고 위험하냐”로 읽어야 한다.
