# 10 Cloud Security Control Plane

## 풀려는 문제

앞선 아홉 개 프로젝트는 각각의 판단 로직을 보여 주지만, 실무의 보안 플랫폼은 이 로직들을 하나의 운영 흐름으로 묶어야 합니다.
이 캡스톤은 scan 요청, ingestion, finding 저장, exception, remediation, report를 local 환경에서 통합하는 것을 목표로 합니다.

## 내가 낸 답

- Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 공통 finding 흐름으로 통합합니다.
- FastAPI API, scan worker, remediation worker, PostgreSQL/SQLite 상태 저장소를 분리합니다.
- finding, exception, remediation dry-run, markdown report를 한 서비스 레이어에서 연결합니다.
- Docker daemon이 없을 때도 SQLite fallback으로 demo를 재현할 수 있게 했습니다.

## 입력과 출력

- 입력: `problem/data/insecure_plan.json`, `broad_admin_policy.json`, `cloudtrail_suspicious.json`, `insecure_k8s.yaml`
- 출력: finding 목록, exception 상태, remediation dry-run 결과, markdown report, audit event

## 검증 방법

```bash
make venv
PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json
make test-capstone
make demo-capstone
```

## 현재 상태

- `verified`
- `make demo-capstone`으로 end-to-end 데모 산출물을 재현할 수 있습니다.
- PostgreSQL과 SQLite fallback 경로를 모두 지원합니다.

## 한계와 다음 단계

- 실제 AWS 계정 연동, 외부 큐 시스템, 운영용 인증과 멀티테넌시는 다루지 않습니다.
- 학습용 캡스톤이므로 로컬 재현성과 구조 설명에 집중하고, 운영 스케일의 분산 아키텍처는 의도적으로 비워 둡니다.

## 더 깊게 읽을 문서

- [problem/README.md](problem/README.md)
- [python/README.md](python/README.md)
- [docs/README.md](docs/README.md)
- [docs/demo-walkthrough.md](docs/demo-walkthrough.md)
- [notion/README.md](notion/README.md)
