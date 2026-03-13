# 10 Cloud Security Control Plane - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `docs/concepts/architecture.md`, `docs/demo-walkthrough.md`, `app.py`, `workers.py`, `db.py`, `scanners.py`, `reporting.py`, `remediation.py`, `demo_capture.py`, `test_api.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- Terraform, IAM, CloudTrail, Kubernetes 입력을 어떤 API와 worker 경계로 통합해야 하는가
- finding, exception, remediation, report를 어떤 상태 저장소 위에 올려야 local control plane으로 설명할 수 있는가
- end-to-end demo가 어디까지 실제 운영 흐름을 대체하고 무엇을 일부러 비워 두는가

## 실제 구현 표면

- `/v1/scans`, `/v1/ingestions/cloudtrail`, `/v1/ingestions/k8s`, `/v1/findings`, `/v1/exceptions`, `/v1/remediations/{finding_id}/dry-run`, `/v1/reports/latest`, `/v1/workers/scans/run` API를 제공합니다.
- SQLAlchemy 기반 `findings`, `exceptions`, `audit_events`, `scan_jobs`, `remediation_requests`, `remediation_plans` 테이블을 사용합니다.
- CloudTrail은 DuckDB + Parquet lake에 적재하고, findings는 별도 상태 DB에 저장합니다.
- `make demo-capstone`은 demo JSON/Markdown 산출물을 `.artifacts/capstone/demo`에 남깁니다.

## 대표 검증 엔트리

- `PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json`
- `make test-capstone`
- `make demo-capstone`

## 읽는 순서

1. [프로젝트 README](../../../02-capstone/10-cloud-security-control-plane/README.md)
2. [문제 정의](../../../02-capstone/10-cloud-security-control-plane/problem/README.md)
3. [실행 진입점](../../../02-capstone/10-cloud-security-control-plane/python/README.md)
4. [아키텍처 개요](../../../02-capstone/10-cloud-security-control-plane/docs/concepts/architecture.md)
5. [대표 테스트](../../../02-capstone/10-cloud-security-control-plane/python/tests/test_api.py)
6. [입력과 API chronology](10-chronology-inputs-and-api-surface.md)
7. [worker와 상태 chronology](20-chronology-workers-state-and-reporting.md)
8. [demo와 검증 chronology](30-chronology-demo-verification-and-boundaries.md)

## 근거 파일

- [README.md](../../../02-capstone/10-cloud-security-control-plane/README.md)
- [problem/README.md](../../../02-capstone/10-cloud-security-control-plane/problem/README.md)
- [python/README.md](../../../02-capstone/10-cloud-security-control-plane/python/README.md)
- [architecture.md](../../../02-capstone/10-cloud-security-control-plane/docs/concepts/architecture.md)
- [demo-walkthrough.md](../../../02-capstone/10-cloud-security-control-plane/docs/demo-walkthrough.md)
- [app.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py)
- [workers.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py)
- [db.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/db.py)
- [scanners.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/scanners.py)
- [reporting.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/reporting.py)
- [remediation.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/remediation.py)
- [demo_capture.py](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/demo_capture.py)
- [test_api.py](../../../02-capstone/10-cloud-security-control-plane/python/tests/test_api.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
