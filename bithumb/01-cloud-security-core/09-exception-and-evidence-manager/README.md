# 09 Exception and Evidence Manager

## Status

`verified`

## Problem Scope

- finding exception 생성/승인/만료
- evidence attachment metadata 저장
- immutable audit event append

## Build

```bash
cd python
PYTHONPATH=src python -m exception_evidence_manager.cli
```

## Test

```bash
cd study2
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```
