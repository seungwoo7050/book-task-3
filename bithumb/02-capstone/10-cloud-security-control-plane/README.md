# 10 Cloud Security Control Plane

## Status

`verified`

## Problem Scope

- Terraform plan, IAM policy, CloudTrail logs, Kubernetes manifests 수집
- findings, exceptions, remediation, audit trail 관리
- FastAPI API + worker + PostgreSQL state DB + DuckDB lake + markdown report

## Build

```bash
cd python
PYTHONPATH=src python -m cloud_security_control_plane.cli findings list
```

## Test

```bash
cd study2
make test-capstone
make demo-capstone
```

## Verification

- `make test-capstone`
- `make demo-capstone`
  - Docker daemon이 있으면 PostgreSQL 경로로 실행한다.
  - Docker daemon이 없으면 SQLite fallback으로 같은 demo flow를 재현한다.
- 공개용 데모 요약: [docs/demo-walkthrough.md](docs/demo-walkthrough.md)
- 공개용 아키텍처 다이어그램: [docs/concepts/architecture.md](docs/concepts/architecture.md)

## Known Gaps

- 실제 AWS 계정과 연동하지 않는다.
- 큐 시스템과 비동기 브로커는 넣지 않고, worker는 DB polling 형태로 단순화했다.
