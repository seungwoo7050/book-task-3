# 10 Cloud Security Control Plane 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- 앞선 아홉 개 프로젝트의 판단 로직이 하나의 API, DB, worker, remediation, report, demo 흐름으로 묶이는 과정을 복원한다.
- 본문은 작은 프로젝트처럼 세 phase로 압축하지 않고 `API -> worker -> report -> demo capture` 네 구간으로 나눈다.

## 먼저 붙들 소스 묶음
- [`../../../02-capstone/10-cloud-security-control-plane/README.md`](../../../02-capstone/10-cloud-security-control-plane/README.md)
- [`../../../02-capstone/10-cloud-security-control-plane/problem/README.md`](../../../02-capstone/10-cloud-security-control-plane/problem/README.md)
- [`../../../02-capstone/10-cloud-security-control-plane/docs/concepts/architecture.md`](../../../02-capstone/10-cloud-security-control-plane/docs/concepts/architecture.md)
- [`../../../02-capstone/10-cloud-security-control-plane/docs/demo-walkthrough.md`](../../../02-capstone/10-cloud-security-control-plane/docs/demo-walkthrough.md)
- [`../../../02-capstone/10-cloud-security-control-plane/python/README.md`](../../../02-capstone/10-cloud-security-control-plane/python/README.md)
- [`../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py`](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py)
- [`../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/db.py`](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/db.py)
- [`../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py`](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py)
- [`../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/remediation.py`](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/remediation.py)
- [`../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/reporting.py`](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/reporting.py)
- [`../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/demo_capture.py`](../../../02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/demo_capture.py)
- [`../../../02-capstone/10-cloud-security-control-plane/python/tests/test_api.py`](../../../02-capstone/10-cloud-security-control-plane/python/tests/test_api.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - control plane이 어떤 입력과 어떤 verify 경로를 공식 입구로 삼는지 먼저 고정한다.
- `10-development-timeline.md`
  - 도입: 왜 capstone의 핵심이 새 스캐너 추가가 아니라 통합 흐름 설계인지 설명한다.
  - Phase 1. API 표면과 상태 저장소 경계를 먼저 세웠다.
  - Phase 2. worker가 scanner와 저장소를 연결했다.
  - Phase 3. remediation과 report로 운영 흐름을 닫았다.
  - Phase 4. demo capture와 fallback으로 재현성을 마감했다.
  - 마무리: 외부 queue, 실제 AWS 연동, 멀티테넌시처럼 남은 확장을 짧게 적는다.

## 강조할 코드와 CLI
- 코드 앵커: `create_app`, session factory, pending worker loop, report markdown builder, demo asset writer
- CLI 앵커: `python -m cloud_security_control_plane.cli scan ...`, `make test-capstone`, `make demo-capstone`
- 개념 훅: 통합 프로젝트에서 중요한 것은 scanner 추가보다 같은 상태 저장소와 같은 운영 흐름을 공유하게 만드는 일이라는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
