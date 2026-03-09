# 탐지에서 끝나지 않는다 — dry-run 조치안까지

## 왜 이 과제를 만들었나

보안 도구가 finding을 100개 만들어도, 그 finding을 보고 "어떻게 고칠까?"에 답하지 못하면
운영자에게는 noise일 뿐이다.

과제 04에서 IAM 정책의 위험도를 finding으로 바꿨고,
과제 05에서 Terraform plan의 misconfiguration을 finding으로 바꿨다.
이제 남은 질문은 "그래서 이 finding을 어떻게 해결하냐?"이다.

이 과제는 finding을 받아서 `RemediationPlan`을 만드는 runner를 구현한다.
핵심은 **dry-run** — 실제 변경을 실행하지 않고, 조치 계획만 생성하는 것이다.

## 자동 패치와 수동 승인의 구분

모든 finding이 자동으로 고쳐질 수 있는 것은 아니다.
이 과제에서는 finding의 `control_id`에 따라 세 가지 모드로 나눈다.

### auto_patch_available (CSPM-001)

S3 퍼블릭 접근 차단 플래그를 전부 `true`로 바꾸는 Terraform 패치를 제안한다.
이건 비교적 안전한 변경이라서, 자동 패치 후보로 분류한다.

```hcl
resource "aws_s3_bucket_public_access_block" "target" {
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

하지만 "자동 패치 가능"이지 "자동 적용"이 아니다.
`status`는 `pending_approval`로 시작하고, 누군가 `approve`해야 `approved`가 된다.

### manual_approval_required (CSPM-002)

Security Group의 SSH 접근을 제한하는 변경은 네트워크에 영향을 준다.
잘못하면 합법적인 접근이 차단될 수 있어서, 반드시 사람이 검토하고 승인해야 한다.

조치안에는 두 가지를 제안한다:
1. Terraform에서 `0.0.0.0/0`을 신뢰할 수 있는 CIDR로 교체
2. AWS CLI로 직접 ingress 규칙 삭제: `aws ec2 revoke-security-group-ingress ...`

### manual_review (기타)

위 두 패턴에 해당하지 않는 finding은 "수동 리뷰" 모드다.
변경 요청을 열고; 승인자와 롤백 계획을 문서화하라는 가이드를 제공한다.

## 설계 선택

### RememdiationPlan을 dataclass로 만든 이유

`RemediationPlan`은 불변 데이터 구조다.
`finding_id`, `mode`, `summary`, `commands_or_patch`, `status`를 가진다.

`approve()` 함수는 기존 plan을 수정하지 않고 새 plan을 반환한다.
이렇게 한 이유는 audit trail에서 "승인 전 plan"과 "승인 후 plan"을 둘 다 남길 수 있기 때문이다.

### commands_or_patch를 문자열 리스트로 한 이유

Terraform HCL이나 AWS CLI 명령 같은 다양한 형식의 조치안을 담아야 했다.
구조화된 패치 객체를 만들 수도 있었지만,
v1에서는 "사람이 읽고 실행할 수 있는 텍스트"가 더 실용적이었다.

실제 프로덕션에서는 이 텍스트를 파싱해서 자동 실행하는 것으로 확장할 수 있지만,
이 과제의 범위는 "제안"까지다.

### dry-run이라는 제약이 가르쳐 준 것

처음에는 "자동으로 고치면 되지 않나?"라고 생각했다.
그런데 실제 보안 운영에서는 자동 수정이 오히려 사고를 만들 수 있다.

- 네트워크 설정을 자동으로 바꾸면 서비스가 중단될 수 있다
- IAM 정책을 자동으로 축소하면 정상 업무가 차단될 수 있다
- 암호화를 자동으로 활성화하면 기존 데이터 접근이 깨질 수 있다

그래서 "조치안을 만들되, 실행은 사람이 검토한 후에"라는 dry-run 접근이
보안 운영에서 더 현실적이라는 걸 체감했다.

## 실제로 만들어 본 뒤에 체감한 것

가장 인상적이었던 것은, finding의 `control_id`만으로 조치안의 성격이 완전히 달라진다는 점이다.

CSPM-001은 패치가 명확하지만, CSPM-002는 "무엇으로 바꿀지"를 사람이 결정해야 한다.
이 구분이 코드에서 `build_dry_run`의 분기로 드러나고,
결과적으로 보안 운영의 핵심 시사점 — "모든 것을 자동화할 수는 없다" — 을 코드로 보여 준다.

## 이 과제의 위치

- **과제 05 → 이 과제**: CSPM finding을 입력받아 조치안을 생성한다
- **이 과제 → 과제 09**: remediation plan도 거버넌스 대상이다 — 예외와 증적으로 연결
- **이 과제 → 과제 10**: Control Plane의 remediation worker가 같은 build_dry_run 패턴을 사용하고, API로 dry-run을 요청할 수 있다

## 한계와 v1 범위

- 실제 apply(적용)는 하지 않는다.
- rollback plan은 포함하지 않는다.
- 조치안의 우선순위(어떤 finding을 먼저 고칠지)는 다루지 않는다.
- Terraform patch를 실제 `.tf` 파일에 적용하는 자동화는 범위 밖이다.
