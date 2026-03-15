# 10 Cloud Security Control Plane: 많은 scanner보다 먼저 하나의 운영 흐름을 만든다

이 capstone을 처음 보면 Terraform, IAM, CloudTrail, Kubernetes를 모두 다루니까 "여러 탐지기를 합친 프로젝트"처럼 보인다. 그런데 실제 코드를 따라가면 더 중요한 건 scanner 수가 아니다. 앞선 labs의 판단 결과가 같은 DB에 저장되고, 예외와 remediation과 report까지 같은 흐름으로 이어지는가가 진짜 중심이다.

## 구현 순서 요약
1. 공통 DB와 FastAPI surface를 먼저 세웠다.
2. terraform/IAM scan job과 cloudtrail/k8s ingestion을 서로 다른 처리 경로로 연결했다.
3. exception, remediation, report, demo asset으로 운영 흐름을 닫았다.

## Phase 1. 먼저 만든 것은 scanner가 아니라 공통 저장 경계였다

`db.py`와 `app.py`를 보면 이 capstone의 우선순위가 드러난다. SQLAlchemy 모델은 findings, exceptions, audit_events, remediation_requests, remediation_plans, scan_jobs를 한 DB에 둔다. `create_app()`는 여기에 FastAPI route와 metrics, lake_dir를 붙인다. 즉 이 프로젝트는 "많은 입력을 받는다"보다 "많은 입력이 같은 운영 상태 저장소를 공유한다"를 먼저 해결한다.

이 선택은 CLI에서도 보인다. Terraform plan을 직접 스캔하는 커맨드를 다시 돌리면 세 finding이 나온다.

```bash
cd /Users/woopinbell/work/book-task-3/bithumb
PYTHONPATH=02-capstone/10-cloud-security-control-plane/python/src \
.venv/bin/python -m cloud_security_control_plane.cli scan terraform-plan \
02-capstone/10-cloud-security-control-plane/problem/data/insecure_plan.json
```

출력 핵심:
- `CSPM-001` for `study2-public-logs`
- `CSPM-002` for `ssh_open`
- `CSPM-003` for `study2-analytics`

여기서 중요한 건 rule 자체보다 finding ID 생성 방식이다. `source:control_id:resource_id`를 SHA-1 prefix로 만들어서, 같은 input이면 같은 ID가 나오도록 해 둔다. 통합 저장소를 굴리려면 바로 이 재현 가능한 ID가 먼저 필요하다.

## Phase 2. 입력은 통합되지만 처리 경로는 일부러 다르게 남겼다

이 capstone이 흥미로운 이유 중 하나는 모든 입력을 같은 worker로 뭉개지 않는다는 점이다. `process_pending_scans()`는 오직 `terraform-plan`과 `iam-policy` scan job만 처리한다. 반면 CloudTrail과 k8s는 각각 `/v1/ingestions/cloudtrail`, `/v1/ingestions/k8s`에서 바로 저장된다.

즉 구조는 통합이지만, operational path는 다르다. scan job queue와 synchronous ingestion이 공존한다. `test_api.py`도 이 현실을 그대로 따른다. scan request 두 건을 만들고 worker를 한 번 돌린 다음, cloudtrail과 k8s는 별도 endpoint를 직접 호출한다.

이번 재실행에서도 그 차이는 그대로 확인됐다.

```bash
cd /Users/woopinbell/work/book-task-3/bithumb
make test-capstone
```

```text
1 passed in 0.54s
```

그리고 이 테스트는 `processed_jobs == 2`를 요구한다. 즉 queue를 타는 건 두 scan job뿐이라는 뜻이다.

## Phase 3. 앞선 labs의 판단 로직은 여기서 축약된 형태로 다시 쓰인다

capstone이라고 해서 이전 lab의 rule set을 전부 가져오진 않는다. 오히려 중요한 seam만 남긴다.

- IAM: `IAM-001`, `IAM-002`만 있다. 이전 lab의 escalation-style `IAM-003`은 없다.
- CloudTrail: `CreateAccessKey`와 `DeleteTrail`만 finding으로 저장한다. 이전 security lake mini의 5개 taxonomy 전체를 가져오지 않는다.
- k8s: `hostPath`, `latest`, `broad security context` 세 축만 남고, image metadata scanner는 빠진다.

이건 축소가 아니라 의도에 가깝다. capstone의 목표가 rule catalog 완성이 아니라 control plane 통합이기 때문이다. 실제 demo findings를 다시 확인해 보니 총 10건이었고, source는 네 가지였다.

- `terraform-plan`
- `iam-policy`
- `cloudtrail`
- `k8s-manifest`

즉 capstone은 "모든 탐지"보다 "다양한 소스가 공통 finding 모델로 합쳐진다"는 사실을 보여 주는 쪽에 더 무게를 둔다.

## Phase 4. exception과 remediation이 report에서 비로소 운영 문맥이 된다

통합 흐름이 설득력을 얻는 지점은 report다. `active_exception_scope_ids()`는 approved + unexpired exception의 `scope_id`를 모으고, `list_findings()`는 row.id가 그 집합에 들어 있으면 status를 `suppressed`로 바꾼다. 그래서 예외는 DB row에만 남는 게 아니라, 최종 report의 finding 상태를 실제로 바꾼다.

remediation도 같은 식으로 이어진다. `build_remediation()`은 `CSPM-001`이면 `auto_patch_available`, `CSPM-002`면 `manual_approval_required`, 나머지는 `manual_review`로 분기한다. 이 결과는 다시 remediation plan row로 저장되고 report에 합쳐진다.

이번 `make demo-capstone` 재실행에서 생성된 `.artifacts/capstone/demo/08-report.md`를 보면 바로 확인된다.

- 첫 finding `CSPM-001`은 `suppressed`
- `CSPM-002`는 `open`
- exception 1건과 remediation plan 1건이 같은 report에 함께 기록

한 가지 현재 semantics도 같이 보였다. exception API는 `scope_type`을 받지만 suppression 계산은 사실상 `scope_id`만 사용한다. 그래서 findings suppression 관점에서는 `scope_id`에 finding ID를 넣는 것이 실질적인 계약이다.

## Phase 5. demo capture가 capstone의 현재 모습을 파일로 고정한다

테스트는 end-to-end 시나리오를 검증하지만, 사람이 나중에 결과를 읽기엔 demo asset이 더 좋다. `demo_capture.py`는 scan request, worker run, cloudtrail ingestion, k8s ingestion, exception 생성, remediation dry-run, report export를 순서대로 호출해서 `01`부터 `08`까지 파일로 남긴다.

그리고 `Makefile`은 실행 환경에 따라 경로를 나눈다. Docker daemon이 있으면 Postgres를 띄우고, 없으면 SQLite fallback으로 같은 시나리오를 재현한다. 이번 재실행에서는 Docker가 살아 있어서 실제로 `postgres healthy` 뒤에 demo asset이 생성됐다.

```bash
cd /Users/woopinbell/work/book-task-3/bithumb
make demo-capstone
```

확인한 출력 핵심:
- `postgres healthy`
- `demo assets written to /Users/woopinbell/work/book-task-3/bithumb/02-capstone/10-cloud-security-control-plane/.artifacts/capstone/demo`

이건 작은 차이가 아니다. capstone이 "로컬에서 설명 가능한 보안 플랫폼"이라는 주장을 테스트뿐 아니라 실행 산출물로도 남긴다는 뜻이기 때문이다.

## 지금 상태에서 분명한 한계

- 모든 입력이 queue worker를 타는 구조는 아니다.
- rule set은 앞선 labs보다 축약돼 있다.
- exception suppression은 finding ID 중심으로 사실상 좁게 정의된다.
- metrics endpoint는 있지만 현재 test coverage의 핵심 축은 아니다.

그래도 이 capstone이 잘하는 일은 분명하다. 개별 탐지기를 더 많이 붙이는 대신, 다양한 입력이 finding 저장, 예외, remediation, report, demo asset으로 이어지는 한 개의 운영 흐름을 실제로 보여 준다. 앞선 labs를 왜 했는지가 여기서 비로소 한 화면으로 정리된다.
