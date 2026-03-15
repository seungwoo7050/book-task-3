# 10 Cloud Security Control Plane 읽기 지도

이 capstone은 앞선 bithumb labs를 한 서비스 안에 묶지만, 모든 로직을 그대로 복제하지는 않는다. 읽을 때도 "많은 scanner가 있다"보다 `어떤 입력이 어떤 경로로 들어와 같은 DB와 report로 합쳐지는가`를 먼저 붙드는 편이 정확하다.

## 먼저 붙들 질문
- 이 capstone의 진짜 중심은 scanner 추가인가, 아니면 상태 저장소와 운영 흐름 통합인가?
- scan job queue를 타는 입력과 동기 ingestion으로 바로 저장되는 입력은 어떻게 나뉘는가?
- 앞선 labs의 rule set이 여기서 어떻게 축약되거나 변형되는가?

## 이 글은 이렇게 읽으면 된다
1. `create_app()`와 `db.py`를 먼저 본다. FastAPI, session factory, SQLite/Postgres 경계를 확인한다.
2. `workers.py`와 `scanners.py`를 본다. terraform/IAM scan job, cloudtrail/k8s ingestion, remediation worker가 어떻게 다르게 움직이는지 본다.
3. 마지막으로 `reporting.py`, `demo_capture.py`, `Makefile`을 본다. 실제 demo가 무엇을 남기고 어떤 fallback을 쓰는지 확인한다.

## 특히 눈여겨볼 장면
- scan job queue는 현재 `terraform-plan`, `iam-policy`만 처리한다.
- cloudtrail과 k8s는 worker queue를 거치지 않고 동기 ingestion endpoint에서 바로 findings를 저장한다.
- capstone의 rule set은 앞선 labs보다 작다. IAM은 `IAM-001/002`만, CloudTrail은 `LAKE-001/004`만, k8s는 `K8S-001/002/003`만 생성한다.
- exception API는 `scope_type`을 받지만, findings suppression은 사실상 `scope_id == finding.id`일 때만 반영된다.

## 먼저 열 문서
- [10-development-timeline.md](10-development-timeline.md)

## 이번 문서의 근거
- `README.md`
- `problem/README.md`
- `python/README.md`
- `docs/concepts/architecture.md`
- `docs/demo-walkthrough.md`
- `python/src/cloud_security_control_plane/app.py`
- `python/src/cloud_security_control_plane/cli.py`
- `python/src/cloud_security_control_plane/db.py`
- `python/src/cloud_security_control_plane/scanners.py`
- `python/src/cloud_security_control_plane/workers.py`
- `python/src/cloud_security_control_plane/remediation.py`
- `python/src/cloud_security_control_plane/reporting.py`
- `python/src/cloud_security_control_plane/demo_capture.py`
- `python/tests/test_api.py`
- `.artifacts/capstone/demo/05-findings.json`
- `.artifacts/capstone/demo/07-remediation.json`
- `.artifacts/capstone/demo/08-report.md`
