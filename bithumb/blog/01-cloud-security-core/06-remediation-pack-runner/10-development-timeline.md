# 06 Remediation Pack Runner: finding을 실행이 아닌 조치안으로 바꾸기

finding을 곧바로 실행하는 대신, 사람이 검토할 수 있는 dry-run 조치안으로 바꾸는 단계다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "왜 remediation의 첫 산출물을 실행 결과가 아닌 plan 문서로 봤는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. finding을 입력받는 `RemediationPlan` 구조를 먼저 세우고 mode를 분리했다.
2. `CSPM-001`과 `CSPM-002`를 서로 다른 remediation mode로 매핑했다.
3. 승인 전후 상태를 별도 함수로 나눠 이후 worker가 재사용할 수 있게 했다.

## Phase 1. remediation 출력 shape부터 고정했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `remediation 출력 shape부터 고정했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: finding을 받아 사람이 검토할 plan 문서로 바꾸는 최소 구조를 세운다.
- 변경 단위: `python/src/remediation_pack_runner/runner.py`의 `RemediationPlan`, `build_dry_run`
- 처음 가설: 실행을 미뤄도 괜찮으려면 summary, commands_or_patch, status 같은 필드가 먼저 있어야 한다.
- 실제 진행: `RemediationPlan` dataclass를 만들고, control_id에 따라 `mode`, `summary`, `commands_or_patch`를 채우는 함수를 작성했다. 이때 출력은 실제 적용 결과가 아니라 검토 자료라는 점을 명확히 하기 위해 status를 `pending_approval`로 시작했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
```

검증 신호:
- CLI 출력이 `mode: auto_patch_available`, `status: pending_approval`를 함께 보여 줬다.
- `commands_or_patch`에는 실제 Terraform patch 초안 줄이 들어갔다.

핵심 코드:

```python
def build_dry_run(finding: dict[str, Any]) -> RemediationPlan:
    control_id = str(finding["control_id"])
    resource_id = str(finding["resource_id"])
    if control_id == "CSPM-001":
        return RemediationPlan(
            finding_id=resource_id,
            mode="auto_patch_available",
            summary="Enable all public access block flags for the bucket.",
            commands_or_patch=[
                "resource \"aws_s3_bucket_public_access_block\" \"target\" {",
                "  block_public_acls       = true",
                "  block_public_policy     = true",
                "  ignore_public_acls      = true",
                "  restrict_public_buckets = true",
                "}",
            ],
            status="pending_approval",
        )
    if control_id == "CSPM-002":
        return RemediationPlan(
            finding_id=resource_id,
            mode="manual_approval_required",
            summary="Narrow exposed ingress CIDRs and remove public SSH/RDP access.",
            commands_or_patch=[
                "terraform: replace 0.0.0.0/0 with a trusted corporate CIDR",
                "aws ec2 revoke-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 --cidr 0.0.0.0/0",
            ],
            status="pending_approval",
        )
    return RemediationPlan(
        finding_id=resource_id,
        mode="manual_review",
        summary="Review the finding and apply a least-privilege remediation.",
        commands_or_patch=[
            "open a change request",
            "document approver and rollback steps",
        ],
        status="pending_approval",
    )
```

왜 이 코드가 중요했는가: 이 함수 덕분에 remediation은 더 이상 “나중에 사람이 알아서”가 아니게 됐다. 자동화할 수 없는 단계도 구조화된 제안으로 바뀌었다.

새로 배운 것: dry-run remediation의 핵심은 실행을 미루는 데 있지 않고, 검토를 가능한 형태로 만드는 데 있다.

다음: 이제 같은 finding이라도 자동 패치 후보와 수동 승인 대상을 명확히 나눠야 했다.

## Phase 2. remediation mode를 control별로 갈랐다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `remediation mode를 control별로 갈랐다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 위험 종류에 따라 조치 전략이 달라진다는 점을 코드로 드러낸다.
- 변경 단위: `python/src/remediation_pack_runner/runner.py`의 `CSPM-001`, `CSPM-002`, fallback 분기
- 처음 가설: S3 public access block 같은 건 auto patch 후보가 될 수 있지만, public ingress는 승인과 rollback이 필수다.
- 실제 진행: `CSPM-001`은 `auto_patch_available`, `CSPM-002`는 `manual_approval_required`, 나머지는 `manual_review`로 분리했다. 이 분기 덕분에 remediation runner가 단순 메시지 출력기가 아니라 운영 모드 분류기 역할도 맡게 됐다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
```

검증 신호:
- sample finding이 `study2-public-logs`일 때 patch 초안이 곧바로 출력됐다.
- README가 manual approval / manual review를 별도 운영 모드로 설명하고 있다.

핵심 코드:

```python
    if control_id == "CSPM-001":
        return RemediationPlan(
            finding_id=resource_id,
            mode="auto_patch_available",
            summary="Enable all public access block flags for the bucket.",
            commands_or_patch=[
                "resource \"aws_s3_bucket_public_access_block\" \"target\" {",
                "  block_public_acls       = true",
                "  block_public_policy     = true",
                "  ignore_public_acls      = true",
                "  restrict_public_buckets = true",
                "}",
            ],
            status="pending_approval",
        )
    if control_id == "CSPM-002":
        return RemediationPlan(
            finding_id=resource_id,
            mode="manual_approval_required",
            summary="Narrow exposed ingress CIDRs and remove public SSH/RDP access.",
            commands_or_patch=[
                "terraform: replace 0.0.0.0/0 with a trusted corporate CIDR",
                "aws ec2 revoke-security-group-ingress --group-id <sg-id> --protocol tcp --port 22 --cidr 0.0.0.0/0",
            ],
            status="pending_approval",
        )
    return RemediationPlan(
```

왜 이 코드가 중요했는가: 이 분기가 생겨야 remediation이 현실적으로 들린다. 같은 “수정”이라도 위험 유형에 따라 review 강도가 달라지기 때문이다.

새로 배운 것: 보안 조치 자동화는 이분법이 아니다. auto patch, manual approval, manual review를 분리해야 운영 리스크를 설명할 수 있다.

다음: 마지막으로 승인 전후 상태 전이를 별도 함수로 떼어 worker가 재사용할 수 있게 해야 했다.

## Phase 3. approval 상태 전이를 별도 함수로 분리했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `approval 상태 전이를 별도 함수로 분리했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: plan 생성과 승인 처리를 분리해 추후 orchestration에 연결하기 쉽게 만든다.
- 변경 단위: `python/src/remediation_pack_runner/runner.py`의 `approve`, `python/tests/test_runner.py`
- 처음 가설: 조치안 생성과 승인 완료는 같은 시점이 아니다. 상태 전이를 분리해야 이후 worker가 끼어들 수 있다.
- 실제 진행: `approve`는 summary에 approver를 남기고 status를 `approved`로 바꾸는 작은 함수로 분리됐다. 테스트는 patch가 포함된 plan 생성과 approval 반영 둘 다 따로 확인했다.

CLI:

```bash
$ PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests
```

검증 신호:
- pytest가 `2 passed in 0.01s`로 통과했다.
- `test_approve_marks_plan_approved`가 summary 안의 approver와 상태 변화를 동시에 요구했다.

핵심 코드:

```python
def approve(plan: RemediationPlan, approved_by: str) -> RemediationPlan:
    return RemediationPlan(
        finding_id=plan.finding_id,
        mode=plan.mode,
        summary=f"{plan.summary} Approved by {approved_by}.",
        commands_or_patch=plan.commands_or_patch,
        status="approved",
    )
```

왜 이 코드가 중요했는가: 이 여덟 줄이 remediation runner를 단발성 formatter가 아니라 상태 전이를 가진 컴포넌트로 바꿨다. capstone worker가 그대로 붙을 수 있었던 이유도 여기 있다.

새로 배운 것: 보안 조치 흐름에서 중요한 것은 patch 내용만이 아니라 승인 이전과 이후를 분리해 추적하는 일이다.

다음: 다음 프로젝트에서는 로그 적재와 탐지를 한 번에 묶어 local security lake 감각을 만든다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

이 runner는 자동 수정기를 만들지 않았다. 대신 어떤 조치가 자동 후보이고, 어떤 조치가 승인과 rollback 계획을 요구하는지 구조화했다. 그래서 capstone에서는 remediation worker가 이 결과를 그대로 저장하고 보고서에 실을 수 있었다.
