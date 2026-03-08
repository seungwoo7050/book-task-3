# 01 AWS Security Primitives

## Status

`verified`

## Problem Scope

- IAM policy의 allow/deny precedence
- wildcard action/resource matching
- explicit deny override
- least privilege 사고방식의 기본기

## Build

```bash
cd python
PYTHONPATH=src python -m aws_security_primitives.cli explain ../problem/data/policy_allow_read.json ../problem/data/request_read.json
```

## Test

```bash
cd study2
PYTHONPATH=00-aws-security-foundations/01-aws-security-primitives/python/src .venv/bin/python -m pytest 00-aws-security-foundations/01-aws-security-primitives/python/tests
```

## Learned

정책 문법을 외우는 것보다, 실제 요청이 어떻게 statement에 걸리고 왜 최종 허용/거부가 되는지
코드로 설명할 수 있어야 이후 IAM analyzer와 control plane이 자연스럽다.
