# 10 Cloud Security Control Plane 구조 메모

## 이번 문서의 중심
- capstone을 "여러 scanner 모음"이 아니라 "하나의 운영 흐름 통합"으로 설명한다.
- 서사는 `공통 DB/API -> 서로 다른 처리 경로 -> exception/remediation/report -> demo asset` 순서로 둔다.
- 앞선 labs 대비 축약된 rule set과 현재 key semantics를 숨기지 않는다.

## 먼저 붙들 소스
- `../../../02-capstone/10-cloud-security-control-plane/README.md`
- `../../../02-capstone/10-cloud-security-control-plane/problem/README.md`
- `../../../02-capstone/10-cloud-security-control-plane/python/README.md`
- `../../../02-capstone/10-cloud-security-control-plane/docs/concepts/architecture.md`
- `../../../02-capstone/10-cloud-security-control-plane/docs/demo-walkthrough.md`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/cli.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/db.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/scanners.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/remediation.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/reporting.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/demo_capture.py`
- `../../../02-capstone/10-cloud-security-control-plane/python/tests/test_api.py`
- `../../../02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo/05-findings.json`
- `../../../02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo/08-report.md`

## 본문 배치
- 도입
  - 많은 scanner보다 공통 상태 저장과 운영 흐름이 capstone의 중심이라는 점을 먼저 둔다.
- Phase 1
  - DB 모델, FastAPI surface, deterministic finding ID를 설명한다.
- Phase 2
  - terraform/IAM queue worker와 cloudtrail/k8s synchronous ingestion의 차이를 분명히 적는다.
- Phase 3
  - 축약된 IAM/LAKE/K8S rule set을 보여 주며 통합 우선 설계를 설명한다.
- Phase 4
  - exception suppression과 remediation plan, markdown report가 한 흐름으로 이어지는 장면을 둔다.
- Phase 5
  - demo_capture와 Docker/SQLite fallback으로 재현성을 마감한다.

## 꼭 남길 검증 신호
- CLI terraform scan에서 3 findings 출력
- `make test-capstone` 통과
- `make demo-capstone`에서 `postgres healthy` 후 demo asset 생성
- demo findings 10건, remediation 1건, report에서 `CSPM-001` suppressed 확인

## 탈락 기준
- 모든 입력이 같은 worker를 탄다고 쓰면 안 된다.
- 앞선 labs의 full rule set이 그대로 들어왔다고 과장하면 안 된다.
- suppression key와 SQLite/Postgres fallback 같은 실제 seam을 빼먹으면 안 된다.
