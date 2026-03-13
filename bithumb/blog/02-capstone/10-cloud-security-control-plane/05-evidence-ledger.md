# 10 Cloud Security Control Plane 근거 정리

앞선 아홉 개 프로젝트의 판단 로직을 scan, ingestion, exception, remediation, report 흐름으로 묶어 내는 통합 capstone이다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. API 표면과 상태 저장소 경계를 먼저 세웠다

이 구간에서는 `API 표면과 상태 저장소 경계를 먼저 세웠다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: 여러 보안 입력이 한 서비스 안으로 들어오는 기본 통로를 만든다.
- 변경 단위: `python/src/cloud_security_control_plane/app.py`의 `create_app`, `python/src/cloud_security_control_plane/db.py`의 session factory
- 처음 가설: 통합 프로젝트일수록 새 로직을 많이 쓰기보다, 기존 스캐너를 얇게 감싸는 API/DB 경계를 먼저 세우는 편이 안전하다.
- 실제 조치: `create_app`은 database URL과 lake 디렉터리를 app state에 저장하고, `session_factory`와 `metrics`를 함께 묶었다. 동시에 `/v1/scans`, `/v1/ingestions/*`, `/v1/findings`, `/v1/exceptions`, `/v1/remediations/*`, `/v1/reports/latest` 라우트를 한곳에 올려 control plane의 외형을 만들었다.
- CLI:
  - `PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json`
- 검증 신호:
  - CLI가 `CSPM-001`, `CSPM-002`, `CSPM-003` 세 finding을 JSON으로 출력했다.
  - `db.default_database_url()`은 기본적으로 SQLite fallback 경로를 가리키고, `normalize_database_url()`은 postgres URL을 psycopg 형태로 맞춘다.
- 핵심 코드 앵커: `02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/app.py:22-43`
- 새로 배운 것: 통합 레이어의 핵심은 비즈니스 로직을 다시 쓰는 게 아니라, 기존 판단 로직이 같은 저장소와 같은 인터페이스를 공유하게 만드는 것이다.
- 다음: 이제 pending scan/remediation 요청을 실제 처리하는 worker 계층을 붙여야 했다.

## Phase 2. worker가 scanner와 저장소를 연결했다

이 구간에서는 `worker가 scanner와 저장소를 연결했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: scan 요청과 remediation 요청이 상태 전이를 거쳐 결과를 저장하게 만든다.
- 변경 단위: `python/src/cloud_security_control_plane/workers.py`, `python/src/cloud_security_control_plane/db.py`의 `save_findings`, `create_scan_job`, `list_findings`
- 처음 가설: 요청을 받는 API와 실제 처리를 섞으면 capstone이 금방 커진다. worker로 분리하면 pending/completed 상태를 설명하기 쉬워진다.
- 실제 조치: `process_pending_scans`는 source에 따라 Terraform/IAM scanner를 호출하고 finding 저장과 metrics 증가를 맡았다. `ingest_cloudtrail_and_save`, `ingest_k8s_and_save`는 각각 lake 적재나 manifest scanning을 수행한 뒤 finding과 audit event를 저장하게 했다. DB 레이어는 findings, exceptions, remediation requests/plans, scan jobs를 같은 SQLAlchemy 모델로 관리한다.
- CLI:
  - `make test-capstone`
- 검증 신호:
  - `make test-capstone`이 `1 passed in 0.64s`로 end-to-end 테스트를 통과했다.
  - 테스트는 scan request 두 건 처리 후 `processed_jobs == 2`, findings 6건 이상, suppression 반영, remediation dry-run 생성까지 확인한다.
- 핵심 코드 앵커: `02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/workers.py:12-42`
- 새로 배운 것: control plane에서 중요한 분리는 sync API와 async-like worker의 역할 분담이다. 그래야 pending/completed, metrics, audit가 자연스럽게 붙는다.
- 다음: 이제 remediation과 report를 붙여 전체 운영 흐름을 끝까지 닫아야 했다.

## Phase 3. remediation과 report로 운영 흐름을 닫았다

이 구간에서는 `remediation과 report로 운영 흐름을 닫았다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: finding이 예외와 조치안과 보고서까지 이어지는 마지막 경로를 만든다.
- 변경 단위: `python/src/cloud_security_control_plane/reporting.py`, `python/src/cloud_security_control_plane/remediation.py`, `/v1/remediations/*`, `/v1/reports/latest`
- 처음 가설: capstone이 포트폴리오처럼 보이려면 탐지에서 끝나지 않고, suppressed finding과 dry-run plan이 같은 보고서에 보여야 한다.
- 실제 조치: remediation builder는 CSPM control에 따라 auto/manual mode를 선택하고, report generator는 findings, exceptions, remediation plans를 한 Markdown 문서로 합쳤다. DB 레이어는 active exception scope를 읽어 finding status를 `suppressed`로 바꿔 report에 반영한다.
- CLI:
  - `make demo-capstone`
- 검증 신호:
  - `make demo-capstone` 실행이 `demo assets written to .../.artifacts/capstone/demo`로 끝났다.
  - 생성된 demo asset에서 scan worker는 `processed_jobs: 2`, CloudTrail은 `finding_count: 2`, k8s ingest는 `finding_count: 3`을 기록했다.
  - 최종 report에는 suppressed `CSPM-001`, open `CSPM-002`, `IAM-*`, `LAKE-*`, `K8S-*` findings와 예외 1건, remediation plan 1건이 함께 들어갔다.
- 핵심 코드 앵커: `02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/reporting.py:6-39`
- 새로 배운 것: 보안 플랫폼의 가치는 finding 개수보다 흐름을 연결하는 데 있다. suppressed status와 remediation mode가 같은 report에 들어갈 때 비로소 운영 맥락이 보인다.
- 다음: 마지막으로 이 모든 흐름을 한 번의 demo capture로 남겨야 했다.

## Phase 4. demo capture와 fallback으로 재현성을 마감했다

이 구간에서는 `demo capture와 fallback으로 재현성을 마감했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 4
- 당시 목표: 사람이 수동으로 API를 두드리지 않아도 end-to-end 시나리오를 다시 만들 수 있게 한다.
- 변경 단위: `python/src/cloud_security_control_plane/demo_capture.py`, `docs/demo-walkthrough.md`, `.artifacts/capstone/demo/*`
- 처음 가설: 캡스톤은 설명할 게 많아서, 문서만으로는 재현성이 약하다. demo asset을 파일로 남겨야 결과를 나중에 다시 확인할 수 있다.
- 실제 조치: `demo_capture.py`는 scan request, worker run, cloudtrail/k8s ingestion, exception 생성, remediation dry-run, report export를 순서대로 실행한 뒤 결과를 `01`~`08` 파일로 남겼다. Makefile은 Docker daemon이 있으면 PostgreSQL 경로를, 없으면 SQLite 경로를 택해 같은 시나리오를 재현한다.
- CLI:
  - `make demo-capstone`
  - `PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json`
- 검증 신호:
  - 실제 실행에서는 Docker 경로로 올라가 `postgres healthy` 뒤 demo asset이 생성됐다.
  - 문서 `docs/demo-walkthrough.md`와 실제 demo JSON이 같은 숫자들(`processed_jobs 2`, `cloudtrail 2`, `k8s 3`)을 가리킨다.
- 핵심 코드 앵커: `02-capstone/10-cloud-security-control-plane/python/src/cloud_security_control_plane/demo_capture.py:32-66`
- 새로 배운 것: 통합 프로젝트일수록 재현성은 테스트 한 줄보다 demo artifact에 더 잘 남는다. 구조와 결과를 함께 보존하기 때문이다.
- 다음: 이제 control plane은 로컬 학습용 capstone으로는 충분히 닫혔다. 남은 확장은 외부 큐, 실제 AWS 연동, 인증/멀티테넌시 쪽이다.
