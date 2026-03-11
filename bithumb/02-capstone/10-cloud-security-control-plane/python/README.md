# Python 구현

아래 내용은 모두 레포 루트 기준입니다.

## 구현한 답의 범위

- Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 수집합니다.
- FastAPI API, scan worker, remediation worker, PostgreSQL/SQLite 상태 저장소를 운영합니다.
- finding, exception, remediation, markdown report 흐름을 한 곳에서 통합합니다.

## 핵심 엔트리포인트

- `python/src/cloud_security_control_plane/app.py`
- `python/src/cloud_security_control_plane/cli.py`
- `python/src/cloud_security_control_plane/workers.py`
- `python/src/cloud_security_control_plane/demo_capture.py`

## 실행

```bash
make venv
PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json
```

## 테스트

```bash
make test-capstone
make demo-capstone
```

## 대표 출력 예시

```json
[
  {
    "id": "f96987c43e4a82dc",
    "source": "terraform-plan",
    "control_id": "CSPM-001",
    "severity": "HIGH",
    "resource_type": "aws_s3_bucket_public_access_block",
    "resource_id": "study2-public-logs",
    "title": "S3 bucket does not fully block public access",
    "status": "open",
    "evidence_ref": "public_logs"
  }
]
```

## 구현 메모

캡스톤 구현은 각 프로젝트의 스캐너를 재사용할 수 있도록 얇은 통합 계층에 집중합니다.
