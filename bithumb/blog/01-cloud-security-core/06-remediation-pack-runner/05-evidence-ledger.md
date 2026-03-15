# 06 Remediation Pack Runner 근거 정리

이 문서는 "무엇을 만들었다"보다 "어떤 근거 때문에 그렇게 읽어야 하는가"를 고정하는 메모다. 특히 이 lab은 코드가 아주 작아서 README만 읽으면 다 된 것처럼 보이는데, 실제로는 테스트가 덮는 branch와 source만으로 확인되는 branch를 구분해서 보는 게 중요했다.

## Phase 1. `RemediationPlan`이 이 lab의 실제 계약이다

- 당시 목표: finding을 실행하지 않고도 다음 단계가 재사용할 수 있는 plan 데이터로 바꾼다.
- 핵심 근거:
  - `runner.py`의 `RemediationPlan` dataclass는 `finding_id`, `mode`, `summary`, `commands_or_patch`, `status` 다섯 필드를 고정한다.
  - `sample_finding.json`은 `control_id=CSPM-001`, `resource_id=study2-public-logs`를 가진 최소 입력이다.
  - CLI는 `build_dry_run()` 결과를 `as_dict()`로 JSON 직렬화해 그대로 출력한다.
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m remediation_pack_runner.cli /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json`
- 검증 신호:
  - 출력 JSON의 `finding_id`는 `study2-public-logs`
  - `mode`는 `auto_patch_available`
  - `status`는 `pending_approval`
  - `commands_or_patch`에는 S3 public access block 리소스 초안 6줄이 들어간다
- 해석:
  - 이 lab의 1차 목표는 remediation 실행기가 아니라, 사람이 읽고 승인할 수 있는 조치안 포맷터를 만드는 것이다.

## Phase 2. control별 remediation mode 분기가 핵심 로직이다

- 당시 목표: finding 종류에 따라 운영 모드를 다르게 태운다.
- 핵심 근거:
  - `CSPM-001`은 `auto_patch_available`
  - `CSPM-002`는 `manual_approval_required`
  - 나머지는 `manual_review`
  - `CSPM-002` 분기에는 trusted CIDR 교체 문구와 `aws ec2 revoke-security-group-ingress` 명령이 같이 들어 있다
- 추가 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python - <<'PY'`
  - `from remediation_pack_runner.runner import build_dry_run, as_dict`
  - `print(as_dict(build_dry_run({'control_id':'CSPM-002','resource_id':'sg-123456','title':'Public SSH','severity':'HIGH','resource_type':'aws_security_group','evidence_ref':'sg_public_ssh'})))`
  - `print(as_dict(build_dry_run({'control_id':'IAM-003','resource_id':'role-admin','title':'Escalation risk','severity':'HIGH','resource_type':'aws_iam_role','evidence_ref':'role_admin'})))`
  - `PY`
- 검증 신호:
  - `sg-123456`은 `manual_approval_required`, `pending_approval`
  - `role-admin`은 `manual_review`, `pending_approval`
- 해석:
  - 이 runner는 patch generator라기보다 "어떤 조치 강도로 다뤄야 하는가"를 정규화하는 classifier에 가깝다.
- 주의:
  - 테스트는 현재 `sample_finding.json`과 approval flow만 다룬다.
  - `CSPM-002`와 fallback `manual_review`는 이번 재실행으로는 확인했지만, 정식 pytest coverage에는 아직 없다.

## Phase 3. approval은 상태 표지이지, 실행 orchestration은 아니다

- 당시 목표: plan 생성과 승인 상태 전이를 분리한다.
- 핵심 근거:
  - `approve(plan, approved_by)`는 기존 plan을 복사하면서 summary 뒤에 `Approved by <name>.`를 붙이고 `status='approved'`만 설정한다.
  - `commands_or_patch`와 `mode`는 그대로 유지된다.
  - `test_approve_marks_plan_approved()`도 approver 이름과 상태만 검증한다.
- 재실행:
  - `PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/src /Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python -m pytest /Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/tests`
- 검증 신호:
  - `2 passed in 0.01s`
  - 보조 재실행에서 `approve(build_dry_run(...), 'security.lead')`는 `status='approved'`와 summary suffix만 바뀐다
- 해석:
  - 이 lab은 approval ledger의 첫 걸음까지만 만든다. 실제 apply, rollback, ticket, 외부 승인 시스템은 아직 연결되지 않았다.

## 이번 Todo에서 남긴 한계

- README 서술만 보면 `dry-run` 서브커맨드가 있는 것처럼 읽히지만, 실제 CLI는 단일 커맨드형이라 `python -m remediation_pack_runner.cli <finding_path>`로만 동작한다.
- pytest는 `CSPM-001`과 approval happy path만 고정한다.
- remediation plan은 plain string list라서 patch schema, rollback metadata, approver identity model은 아직 구조화되지 않았다.
