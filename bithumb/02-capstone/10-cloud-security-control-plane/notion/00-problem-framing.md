# 문제 프레이밍

## 이 프로젝트가 답하려는 질문

작은 스캐너와 로컬 도구들을 어떻게 하나의 운영 흐름으로 묶을 것인가? 이 캡스톤은 Terraform plan, IAM policy,
CloudTrail fixture, Kubernetes manifest를 받아 findings, exception, remediation plan, markdown report로 이어지는
최소 control plane을 만드는 것이 목표입니다.

## 실제 입력과 출력

입력:
- Terraform plan JSON
- IAM policy JSON
- CloudTrail fixture
- Kubernetes manifest

출력:
- `/v1/findings`에서 읽는 finding 목록
- `/v1/exceptions`를 통한 suppression 상태
- `/v1/remediations/{finding_id}/dry-run` 결과
- `/v1/reports/latest` markdown report

## 강한 제약

- 실제 AWS 계정 연동은 하지 않습니다.
- worker는 외부 큐가 아니라 DB polling 형태입니다.
- PostgreSQL이 없으면 SQLite fallback으로 데모를 계속할 수 있어야 합니다.

## 완료로 보는 기준

- end-to-end 테스트가 scan -> worker -> ingestion -> exception -> remediation -> report 흐름을 재현해야 합니다.
- 현재 문서는 Docker 사용 시 기본 DB 이름이 `study2_control_plane`임을 코드와 일치하게 설명해야 합니다.
- 이전 01~09 프로젝트의 로직 재사용 지점을 말로 연결할 수 있어야 합니다.

## 확인에 쓰는 근거

- 문제 설명: [../problem/README.md](../problem/README.md)
- 핵심 테스트: [../python/tests/test_api.py](../python/tests/test_api.py)
- 현재 엔드포인트 구현: [../python/src/cloud_security_control_plane/app.py](../python/src/cloud_security_control_plane/app.py)
