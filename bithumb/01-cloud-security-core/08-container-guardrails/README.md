# 08 Container Guardrails

## Status

`verified`

## Problem Scope

- Kubernetes manifest와 Docker metadata 위험 설정 탐지
- privileged, hostPath, latest tag, runAsRoot, capabilities 검사

## Build

```bash
cd python
PYTHONPATH=src python -m container_guardrails.cli ../problem/data/insecure_k8s.yaml ../problem/data/insecure_image.json
```

## Test

```bash
cd study2
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```
