# 재현 가이드

## 무엇을 재현하나

- scan request, worker 처리, CloudTrail/K8s ingestion, exception, remediation, report export까지 end-to-end로 재현되는지
- Docker/PostgreSQL 경로와 SQLite fallback 경로가 모두 문서와 일치하는지
- demo 산출물이 실제 파일로 남는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- Docker daemon이 있으면 PostgreSQL 경로를 사용하고, 없으면 `make demo-capstone`이 SQLite fallback으로 동작합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
make test-capstone
make demo-capstone
sed -n '1,80p' .artifacts/capstone/demo/08-report.md
```

## 기대 결과

- `make test-capstone`은 1개 end-to-end 테스트를 통과하면서 scan job 2건 처리, findings 6건 이상, suppression, remediation, report 생성을 검증해야 합니다.
- `make demo-capstone`은 `demo assets written to .../.artifacts/capstone/demo`를 출력해야 합니다.
- `.artifacts/capstone/demo/` 아래에는 `01-scan-requests.json`부터 `08-report.md`까지 여덟 개 파일이 생성돼야 합니다.
- `08-report.md`에는 `## Findings`, `## Exceptions`, `## Remediation Plans`가 모두 포함돼야 합니다.

## 결과가 다르면 먼저 볼 파일

- 앱 구성과 의존성 초기화를 다시 보려면: [../python/src/cloud_security_control_plane/app.py](../python/src/cloud_security_control_plane/app.py)
- CLI 명령 구성을 다시 보려면: [../python/src/cloud_security_control_plane/cli.py](../python/src/cloud_security_control_plane/cli.py)
- 데모 자산 생성 흐름을 다시 보려면: [../python/src/cloud_security_control_plane/demo_capture.py](../python/src/cloud_security_control_plane/demo_capture.py)
- 통합 검증 기준을 다시 보려면: [../python/tests/test_api.py](../python/tests/test_api.py)
- 데모 절차를 다시 보려면: [../docs/demo-walkthrough.md](../docs/demo-walkthrough.md)
- Docker/PostgreSQL 설정을 다시 보려면: [../../../docker-compose.yml](../../../docker-compose.yml)
- 루트 실행 규칙을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 앞선 프로젝트들의 결과물이 실제 서비스 흐름 안에서 함께 동작한다는 점을 가장 강하게 증명합니다.
- 학습자가 여기서 얻어야 할 핵심은 “캡스톤을 한 번 돌렸다”가 아니라, 어떤 작은 엔진이 어디서 재사용되는지 추적 가능한 상태로 남겼다는 점입니다.
