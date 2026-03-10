# 10 Cloud Security Control Plane

## 프로젝트 한줄 소개

앞선 프로젝트의 판단 로직을 하나의 API, worker, 상태 저장소, 보고 흐름으로 통합한 캡스톤입니다.

## 왜 배우는가

실무의 보안 플랫폼은 개별 스캐너를 따로 실행하는 데서 끝나지 않습니다. 스캔 요청, 상태 저장, 비동기 처리, 예외, 조치안, 보고까지 한 흐름으로 연결해야 하므로, 이 프로젝트는 그 최소 구조를 로컬에서 재현하는 데 집중합니다.

## 현재 구현 범위

- Terraform plan, IAM policy, CloudTrail fixture, Kubernetes manifest를 수집합니다.
- FastAPI API, scan worker, remediation worker, PostgreSQL/SQLite 상태 저장소를 운영합니다.
- finding, exception, remediation, markdown report 흐름을 한 곳에서 통합합니다.

## 빠른 시작

아래 명령은 레포 루트 기준입니다.

```bash
make venv
PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli findings list
```

## 검증 명령

```bash
make test-capstone
make demo-capstone
```

- `make test-capstone`: 캡스톤 테스트를 실행합니다.
- `make demo-capstone`: Docker daemon이 있으면 PostgreSQL, 없으면 SQLite fallback으로 데모 산출물을 만듭니다.

## 먼저 읽을 파일

- [problem/README.md](problem/README.md)
- [docs/README.md](docs/README.md)
- [docs/demo-walkthrough.md](docs/demo-walkthrough.md)
- [python/README.md](python/README.md)
- [notion/README.md](notion/README.md)

## 포트폴리오 확장 힌트

캡스톤 하나만 크게 포장하기보다, 앞선 01~09 프로젝트의 어떤 로직이 여기서 재사용되는지 연결해서 설명하는 편이 훨씬 강합니다.

## 알려진 한계

- 실제 AWS 계정과 연동하지 않습니다.
- 외부 큐 시스템 없이 DB polling worker로 단순화했습니다.
- 운영용 인증·권한 관리나 멀티테넌시는 다루지 않습니다.
