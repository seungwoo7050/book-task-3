# 06 Remediation Pack Runner: finding을 실행 전에 멈춰 세우는 방법

이 lab을 처음 보면 "보안 finding에 대한 자동 조치기"처럼 보이지만, 실제 코드를 따라가면 초점은 다르다. 여기서 만드는 것은 실행기보다 `검토 가능한 조치안`이다. 그래서 chronology도 patch를 얼마나 똑똑하게 만들었는지가 아니라, 어떻게 실행을 한 단계 늦추고도 다음 시스템이 쓸 수 있는 구조를 만들었는지에 맞춰 읽는 편이 자연스럽다.

## 구현 순서 요약
1. finding 하나를 받아 JSON plan 하나를 돌려주는 최소 계약을 먼저 세웠다.
2. control별로 `auto_patch_available`, `manual_approval_required`, `manual_review`를 갈랐다.
3. approval 상태 전이를 별도 함수로 떼서 후속 worker가 다시 쓸 수 있게 만들었다.

## Phase 1. 실행보다 먼저 plan shape를 고정했다

처음 풀어야 했던 질문은 "무엇을 자동화할 것인가"보다 "무엇을 데이터로 남길 것인가"였다. `runner.py`는 그래서 `RemediationPlan`부터 선언한다. `finding_id`, `mode`, `summary`, `commands_or_patch`, `status`를 함께 묶어 두면, 실제 인프라를 건드리지 않아도 운영자가 볼 수 있는 조치 제안이 만들어진다.

이 설계는 `sample_finding.json` 하나로 바로 드러난다. 입력에는 `control_id=CSPM-001`, `resource_id=study2-public-logs` 정도만 들어 있지만, 출력은 곧바로 "S3 public access block을 모두 켜라"는 patch 초안과 `pending_approval` 상태를 갖는다. 실행을 생략했는데도 다음 단계로 넘길 정보는 남는 구조다.

재실행:

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m remediation_pack_runner.cli \
/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json
```

확인한 출력 핵심:
- `finding_id`: `study2-public-logs`
- `mode`: `auto_patch_available`
- `status`: `pending_approval`
- `commands_or_patch`: S3 public access block 리소스 초안 6줄

여기서 중요한 건 patch의 완성도가 아니라, remediation을 "적용"이 아닌 "검토 가능한 제안"으로 먼저 정식화했다는 점이다.

## Phase 2. control별로 조치 강도를 다르게 분류했다

다음 질문은 모든 finding을 같은 방식으로 다뤄도 되느냐였다. `build_dry_run()`의 답은 명확하다. 아니다. `CSPM-001`은 자동 패치 후보로, `CSPM-002`는 승인 필수 대상으로, 나머지는 수동 검토 대상으로 돌린다.

이 구분은 작아 보여도 이 lab의 진짜 중심이다. S3 public access block처럼 안전한 형태의 설정 보정은 patch template로 제안할 수 있지만, public SSH/RDP ingress는 조직 CIDR, change window, rollback 여부를 함께 따져야 한다. 그래서 분기 결과도 patch 텍스트가 아니라 trusted CIDR 교체 문구와 AWS CLI revoke 명령으로 남겨 둔다.

이번 Todo에서는 pytest가 덮지 않는 branch도 직접 확인했다.

보조 재실행:

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python - <<'PY'
from remediation_pack_runner.runner import build_dry_run, as_dict

print(as_dict(build_dry_run({
    "control_id": "CSPM-002",
    "resource_id": "sg-123456",
    "title": "Public SSH",
    "severity": "HIGH",
    "resource_type": "aws_security_group",
    "evidence_ref": "sg_public_ssh",
})))

print(as_dict(build_dry_run({
    "control_id": "IAM-003",
    "resource_id": "role-admin",
    "title": "Escalation risk",
    "severity": "HIGH",
    "resource_type": "aws_iam_role",
    "evidence_ref": "role_admin",
})))
PY
```

확인한 출력 핵심:
- `sg-123456`은 `manual_approval_required`
- `role-admin`은 `manual_review`
- 둘 다 처음 상태는 `pending_approval`

이 단계에서 하나 더 확인한 사실이 있다. README를 얼핏 보면 `dry-run` 서브커맨드가 있는 것처럼 읽히지만, 현재 Typer 설정상 실제 CLI는 서브커맨드 없이 `python -m remediation_pack_runner.cli <finding_path>`로 바로 호출해야 한다. 문서보다 코드가 진짜 인터페이스라는 사실이 다시 드러난 셈이다.

## Phase 3. approval은 "승인 기록"까지만 담당한다

마지막으로 본 것은 approval이 무엇을 하는지였다. `approve()`는 복잡한 워크플로 함수가 아니다. summary 뒤에 approver 이름을 붙이고, 상태를 `approved`로 바꾸고, 나머지 필드는 그대로 둔다. 실행 자체는 일어나지 않는다.

이 선택은 의도적으로 보인다. 이 lab은 approval system이나 rollback orchestration을 만들지 않는다. 대신 "승인이 일어났다"는 사실을 후속 worker가 읽을 수 있는 최소 상태 전이만 남긴다. 그래서 capstone에서 remediation worker가 이 구조를 그대로 재사용할 수 있다.

재실행:

```bash
PYTHONPATH=/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/src \
/Users/woopinbell/work/book-task-3/bithumb/.venv/bin/python \
-m pytest \
/Users/woopinbell/work/book-task-3/bithumb/01-cloud-security-core/06-remediation-pack-runner/python/tests
```

확인한 출력:

```text
..                                                                       [100%]
2 passed in 0.01s
```

그리고 보조 재실행으로는 `security.lead` 승인 후 summary가 `Approved by security.lead.`를 덧붙이고 `status='approved'`로만 바뀌는 것도 확인했다.

## 지금 상태에서 분명한 한계

이 lab은 deliberately small하다. 그래서 장점과 한계가 동시에 선명하다.

- 실제 patch apply는 없다.
- rollback step도 구조화된 필드가 아니라 설명 문구 수준이다.
- approver identity는 summary 문자열에 덧붙는 텍스트일 뿐 별도 필드가 아니다.
- pytest는 `CSPM-001` happy path와 approval만 고정하고, `CSPM-002`와 fallback `manual_review`는 아직 source-level branch에 더 가깝다.

그래도 이 단계가 필요한 이유는 분명하다. 탐지와 실행 사이에 `검토 가능한 remediation plan`을 끼워 넣어야 control plane이 안전하게 커질 수 있기 때문이다. 이 lab은 바로 그 완충 지점을 코드로 처음 만드는 자리다.
