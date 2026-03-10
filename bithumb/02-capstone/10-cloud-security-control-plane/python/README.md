# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 다루는 범위

- Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 수집합니다.
- FastAPI API, scan worker, remediation worker, PostgreSQL/SQLite 상태 저장소를 운영합니다.
- finding, exception, remediation, markdown report 흐름을 한 곳에서 통합합니다.

## 실행 예시

```bash
make venv
PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli findings list
```

## 테스트와 데모

```bash
make test-capstone
make demo-capstone
```

## 상태

`verified`

## 구현 메모

캡스톤 구현은 각 프로젝트의 스캐너를 재사용할 수 있도록 얇은 통합 계층에 집중합니다.
