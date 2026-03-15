# 10 Cloud Security Control Plane 근거 정리

이 문서는 capstone을 "큰 프로젝트"로 뭉개지 않고, 어떤 입력이 어떤 저장 경로와 어떤 축약 rule set을 타는지 고정하는 메모다. 이번 Todo에서는 demo와 테스트를 다시 돌리면서, README가 암시하는 통합 흐름과 실제 구현 경계를 나란히 확인했다.

## Phase 1. 공통 DB와 API 표면이 먼저 capstone을 만든다

- 당시 목표: 여러 scanner보다 먼저, findings/exception/remediation/report가 한 저장소를 공유하게 만든다.
- 핵심 근거:
  - `create_app()`는 `database_url`, `lake_dir`, `metrics`, `session_factory`를 app state에 올린다.
  - `db.make_session_factory()`는 PostgreSQL URL normalizing과 SQLite fallback을 모두 지원한다.
  - SQLAlchemy 모델은 findings, exceptions, audit_events, remediation_requests, remediation_plans, scan_jobs를 같은 DB에 둔다.
- 재실행:
  - `cd /Users/woopinbell/work/book-task-3/bithumb && PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src .venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan 02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json`
- 검증 신호:
  - CLI는 `CSPM-001`, `CSPM-002`, `CSPM-003` 세 finding을 출력했다.
  - `id`는 source/control/resource 기반 SHA-1 prefix라 rerun에도 같은 finding identity를 유지한다.
- 해석:
  - 이 capstone의 핵심은 새로운 탐지보다, 서로 다른 판단 결과가 한 persistence 모델과 한 API surface로 모이는 데 있다.

## Phase 2. 입력 경로는 통합되지만, 처리 방식은 일부러 다르다

- 당시 목표: 모든 입력을 같은 worker로 뭉개지 않고, 현실적인 처리 경로 차이를 남긴다.
- 핵심 근거:
  - `process_pending_scans()`는 `terraform-plan`, `iam-policy` scan job만 처리한다.
  - `ingest_cloudtrail_and_save()`와 `ingest_k8s_and_save()`는 job queue 없이 동기 endpoint에서 바로 findings를 저장한다.
  - `test_api.py`도 `/v1/scans` 두 건을 만든 뒤 worker를 한 번 돌리고, cloudtrail/k8s는 별도 ingestion endpoint로 호출한다.
- 재실행:
  - `cd /Users/woopinbell/work/book-task-3/bithumb && make test-capstone`
- 검증 신호:
  - `1 passed in 0.54s`
  - test는 `processed_jobs == 2`를 요구한다
  - 이후 cloudtrail과 k8s finding count는 별도 endpoint 응답으로 검증한다
- 해석:
  - capstone은 "모든 입력이 같은 async worker를 탄다"는 구조가 아니다. scan job queue와 동기 ingestion이 공존한다.

## Phase 3. 앞선 labs의 rule set은 그대로 들어오지 않고 축약된다

- 당시 목표: 모든 scanner를 완전 재현하기보다, control plane 데모에 필요한 핵심만 남긴다.
- 핵심 근거:
  - IAM scanner는 `IAM-001`, `IAM-002`만 만든다. 이전 lab의 escalation-style `IAM-003`은 여기 없다.
  - CloudTrail ingestion은 `CreateAccessKey -> LAKE-001`, `DeleteTrail -> LAKE-004`만 findings로 만든다.
  - k8s scanner는 `hostPath`, `latest`, `broad security context`만 보고 `K8S-001/002/003`만 만든다.
  - image metadata scanner는 capstone에 들어오지 않는다.
- 재실행:
  - demo output인 `.artifacts/capstone/demo/05-findings.json`을 다시 확인했다.
- 검증 신호:
  - demo findings는 정확히 10건이었다
  - source는 `terraform-plan`, `iam-policy`, `cloudtrail`, `k8s-manifest` 네 갈래였다
  - cloudtrail findings는 `LAKE-001`, `LAKE-004` 두 건뿐이었다
- 해석:
  - capstone은 앞선 lab들의 "대표 seam"만 골라 통합한다. rule coverage보다 control plane 흐름 설명이 우선이다.

## Phase 4. exception, remediation, report가 같은 운영 문서로 닫힌다

- 당시 목표: finding이 triage 문맥 안에서 suppressed, remediation, report로 이어지게 한다.
- 핵심 근거:
  - `active_exception_scope_ids()`는 approved + unexpired exception의 `scope_id` 집합을 만든다.
  - `list_findings()`는 row.id가 그 집합에 있으면 status를 `suppressed`로 바꾼다.
  - `build_remediation()`은 `CSPM-001`, `CSPM-002`, 나머지를 `auto_patch_available`, `manual_approval_required`, `manual_review`로 분기한다.
  - `generate_markdown_report()`는 findings, exceptions, remediations를 한 Markdown으로 합친다.
- 재실행:
  - `cd /Users/woopinbell/work/book-task-3/bithumb && make demo-capstone`
- 검증 신호:
  - 실제 실행에서는 Docker 경로가 선택되어 `postgres healthy` 뒤 demo asset이 생성됐다
  - `.artifacts/capstone/demo/08-report.md`에는 첫 finding `CSPM-001`이 `suppressed`로 표시됐다
  - `.artifacts/capstone/demo/07-remediation.json`에는 `CSPM-002`의 `manual_approval_required` plan이 기록됐다
- 해석:
  - 이 capstone이 증명하는 것은 탐지 엔진의 깊이보다, finding이 예외와 조치안과 보고서로 이어지는 운영 연결성이다.
- 추가 관찰:
  - exception API는 `scope_type`을 받지만 suppression 계산은 `scope_id` 집합만 쓴다. 따라서 findings suppression 관점에서는 사실상 `scope_id == finding.id`가 핵심 키다.

## Phase 5. demo capture가 테스트보다 넓은 재현성을 남긴다

- 당시 목표: 테스트 통과 외에 사람이 읽을 수 있는 실행 흔적을 파일로 남긴다.
- 핵심 근거:
  - `demo_capture.py`는 scan request, worker run, ingestion, exception, remediation, report를 차례대로 호출하고 `01`~`08` 파일을 쓴다.
  - `Makefile`의 `demo-capstone`은 Docker daemon이 있으면 Postgres, 없으면 SQLite fallback을 사용한다.
  - `demo_capture.py`는 DB reset뿐 아니라 기존 lake dir도 `shutil.rmtree()`로 지운다.
- 재실행:
  - 같은 `make demo-capstone` 실행에서 `demo assets written to .../.artifacts/capstone/demo`를 확인했다.
- 검증 신호:
  - demo 산출물 8개 파일이 실제로 생성됐다
  - 이번 실행 환경에서는 SQLite fallback이 아니라 Postgres 경로가 사용됐다
- 해석:
  - capstone에서 demo assets는 단순 홍보 자료가 아니라, 통합 흐름의 현재 상태를 고정하는 실행 산출물이다.

## 이번 Todo에서 남긴 한계

- cloudtrail/k8s는 queue형 worker가 아니라 동기 ingestion이다.
- 예외 suppression key는 사실상 finding ID 축에 묶여 있다.
- rule coverage는 앞선 lab 전체보다 작다.
- metrics endpoint는 구현돼 있지만 test coverage에는 직접 들어가지 않는다.
