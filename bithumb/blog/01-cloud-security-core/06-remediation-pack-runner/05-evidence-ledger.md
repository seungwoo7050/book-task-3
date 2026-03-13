# 06 Remediation Pack Runner 근거 정리

finding을 곧바로 실행하는 대신, 사람이 검토할 수 있는 dry-run 조치안으로 바꾸는 단계다. 이 문서는 그 흐름을 글로 풀기 전에, 실제 근거를 phase 단위로 다시 세워 둔 정리 노트다.

한 phase를 읽을 때는 `당시 목표 -> 실제 조치 -> CLI -> 검증 신호` 순서로 보면 무엇이 먼저 굳어졌는지 빠르게 따라갈 수 있다.

## Phase 1. remediation 출력 shape부터 고정했다

이 구간에서는 `remediation 출력 shape부터 고정했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 1
- 당시 목표: finding을 받아 사람이 검토할 plan 문서로 바꾸는 최소 구조를 세운다.
- 변경 단위: `python/src/remediation_pack_runner/runner.py`의 `RemediationPlan`, `build_dry_run`
- 처음 가설: 실행을 미뤄도 괜찮으려면 summary, commands_or_patch, status 같은 필드가 먼저 있어야 한다.
- 실제 조치: `RemediationPlan` dataclass를 만들고, control_id에 따라 `mode`, `summary`, `commands_or_patch`를 채우는 함수를 작성했다. 이때 출력은 실제 적용 결과가 아니라 검토 자료라는 점을 명확히 하기 위해 status를 `pending_approval`로 시작했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json`
- 검증 신호:
  - CLI 출력이 `mode: auto_patch_available`, `status: pending_approval`를 함께 보여 줬다.
  - `commands_or_patch`에는 실제 Terraform patch 초안 줄이 들어갔다.
- 핵심 코드 앵커: `01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py:16-54`
- 새로 배운 것: dry-run remediation의 핵심은 실행을 미루는 데 있지 않고, 검토를 가능한 형태로 만드는 데 있다.
- 다음: 이제 같은 finding이라도 자동 패치 후보와 수동 승인 대상을 명확히 나눠야 했다.

## Phase 2. remediation mode를 control별로 갈랐다

이 구간에서는 `remediation mode를 control별로 갈랐다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 2
- 당시 목표: 위험 종류에 따라 조치 전략이 달라진다는 점을 코드로 드러낸다.
- 변경 단위: `python/src/remediation_pack_runner/runner.py`의 `CSPM-001`, `CSPM-002`, fallback 분기
- 처음 가설: S3 public access block 같은 건 auto patch 후보가 될 수 있지만, public ingress는 승인과 rollback이 필수다.
- 실제 조치: `CSPM-001`은 `auto_patch_available`, `CSPM-002`는 `manual_approval_required`, 나머지는 `manual_review`로 분리했다. 이 분기 덕분에 remediation runner가 단순 메시지 출력기가 아니라 운영 모드 분류기 역할도 맡게 됐다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json`
- 검증 신호:
  - sample finding이 `study2-public-logs`일 때 patch 초안이 곧바로 출력됐다.
  - README가 manual approval / manual review를 별도 운영 모드로 설명하고 있다.
- 핵심 코드 앵커: `01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py:19-45`
- 새로 배운 것: 보안 조치 자동화는 이분법이 아니다. auto patch, manual approval, manual review를 분리해야 운영 리스크를 설명할 수 있다.
- 다음: 마지막으로 승인 전후 상태 전이를 별도 함수로 떼어 worker가 재사용할 수 있게 해야 했다.

## Phase 3. approval 상태 전이를 별도 함수로 분리했다

이 구간에서는 `approval 상태 전이를 별도 함수로 분리했다`를 먼저 단단히 묶어 두면서, 다음 phase가 기대는 기준을 만들었다.

- 시간 표지: Phase 3
- 당시 목표: plan 생성과 승인 처리를 분리해 추후 orchestration에 연결하기 쉽게 만든다.
- 변경 단위: `python/src/remediation_pack_runner/runner.py`의 `approve`, `python/tests/test_runner.py`
- 처음 가설: 조치안 생성과 승인 완료는 같은 시점이 아니다. 상태 전이를 분리해야 이후 worker가 끼어들 수 있다.
- 실제 조치: `approve`는 summary에 approver를 남기고 status를 `approved`로 바꾸는 작은 함수로 분리됐다. 테스트는 patch가 포함된 plan 생성과 approval 반영 둘 다 따로 확인했다.
- CLI:
  - `PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests`
- 검증 신호:
  - pytest가 `2 passed in 0.01s`로 통과했다.
  - `test_approve_marks_plan_approved`가 summary 안의 approver와 상태 변화를 동시에 요구했다.
- 핵심 코드 앵커: `01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py:57-64`
- 새로 배운 것: 보안 조치 흐름에서 중요한 것은 patch 내용만이 아니라 승인 이전과 이후를 분리해 추적하는 일이다.
- 다음: 다음 프로젝트에서는 로그 적재와 탐지를 한 번에 묶어 local security lake 감각을 만든다.
