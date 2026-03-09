# "허용/거부"를 넘어 "얼마나 위험한가"를 판단하기

## 과제 01과 이 과제의 차이

과제 01에서는 "이 요청이 허용되는가, 거부되는가"를 판단하는 엔진을 만들었다.
입력은 하나의 정책과 하나의 요청이었고, 출력은 허용/거부 결정이었다.

그런데 실제 보안 운영에서 필요한 질문은 조금 다르다.
"이 정책이 **얼마나 위험한가**?"라는 질문이다.

정책 문법이 맞는지가 아니라, 그 정책이 부여하는 권한이
최소 권한 원칙(least privilege)에 비추어 얼마나 넓은지를 판단해야 한다.

이 과제는 그 판단을 `Finding`이라는 표준 구조로 출력하는 분석기를 만드는 것이다.

## Finding이라는 구조

모든 보안 도구의 핵심 산출물은 finding이다.
"무엇이 문제이고, 얼마나 심각하고, 어디에 있는지"를 하나의 레코드로 담는 것이다.

이 과제에서 정의한 Finding의 필드:

- `source`: 어디서 발견했는지 ("iam-policy")
- `control_id`: 어떤 규칙에 걸렸는지 ("IAM-001", "IAM-002", "IAM-003")
- `severity`: 얼마나 심각한지 ("HIGH")
- `resource_type`: 어떤 종류의 리소스인지
- `resource_id`: 구체적으로 어떤 statement인지
- `title`: 사람이 읽을 수 있는 설명
- `evidence_ref`: 증거 참조

이 구조가 중요한 이유는, 이후 과제에서 계속 재사용되기 때문이다.
과제 05(CSPM Rule Engine)의 Finding도 같은 구조이고,
과제 10(Control Plane)에서 DB에 저장되는 finding도 같은 필드를 가진다.

## 세 가지 탐지 규칙

### IAM-001: 모든 액션을 허용하는 정책

`Action`에 `"*"`가 포함되어 있으면 발동한다.
"이 정책은 모든 AWS 작업을 할 수 있습니다"라는 뜻이고,
이건 production 환경에서 절대 있어서는 안 되는 설정이다.

처음에는 wildcard가 포함된 정도를 계산하려고 했지만,
`*` 하나가 있는 것 자체가 이미 최고 위험이라서 이진 판단으로 충분했다.

### IAM-002: 모든 리소스에 적용되는 정책

`Resource`에 `"*"`가 포함되어 있고, 읽기 전용이 아닌 액션이 포함되어 있으면 발동한다.
읽기 전용 액션(`s3:Get*`, `ec2:Describe*` 등)만 있는 경우는 제외했다.

이 구분이 false positive를 줄이는 데 중요했다.
`s3:GetObject`만 허용하는 정책이 `Resource=*`라고 해서
`Action=*`과 같은 레벨로 취급하면 운영자가 finding을 신뢰하지 않게 된다.

### IAM-003: 권한 상승(privilege escalation) 가능 액션

`iam:PassRole`, `iam:CreatePolicyVersion`, `iam:AttachUserPolicy` 등
다른 정책을 만들거나 역할을 넘길 수 있는 액션이 포함되어 있으면 발동한다.

이 규칙은 "이 정책의 소유자가 자기 권한을 스스로 확장할 수 있는가?"라는 질문에 답한다.
attack path 분석에서 가장 먼저 확인하는 패턴이기도 하다.

## 설계 선택

### READ_ONLY_PREFIXES를 분리한 이유

IAM-002에서 읽기 전용 액션을 제외하기 위해 `READ_ONLY_PREFIXES` 튜플을 정의했다.
하드코딩이지만, 이 과제의 범위에서는 S3/EC2/IAM 읽기 접두사면 충분하다.

더 정교한 방법은 AWS의 service authorization reference를 파싱하는 것이지만,
v1에서는 "false positive를 줄이는 최소한의 필터"로 충분했다.

### HIGH_RISK_ACTIONS를 상수로 관리한 이유

Privilege escalation 가능 액션 목록은 보안 연구 커뮤니티에서 잘 알려진 패턴이다.
이 목록을 코드에 상수로 넣은 이유는, 이 과제의 목적이 "분석 엔진 구조를 만드는 것"이지
"완전한 escalation path DB를 구축하는 것"이 아니기 때문이다.

실제 프로덕션에서는 이 목록을 외부 YAML/JSON으로 관리하겠지만,
학습 과제에서는 코드에 있는 편이 "어떤 액션이 위험한지"를 바로 읽을 수 있어서 낫다.

## 실제로 만들어 본 뒤에 체감한 것

세 가지 테스트 fixture를 만들면서 깨달은 것이 있다.

- `broad_admin_policy.json`: `Action=*`, `Resource=*` → IAM-001, IAM-002 둘 다 발동
- `passrole_policy.json`: `iam:PassRole` 포함 → IAM-003 발동
- `scoped_policy.json`: `s3:GetObject`만 특정 버킷에 → finding 없음

세 번째 fixture가 중요했다. "안전한 정책에서는 finding이 0개"라는 것을 확인하는 것이
분석기의 정확성을 검증하는 가장 기본적인 방법이었다.

그리고 IAM-001과 IAM-002가 같은 정책에서 동시에 발동할 수 있다는 점도 중요했다.
finding은 독립적이다. 하나의 정책에서 여러 finding이 나올 수 있고,
각각이 다른 control_id를 가진다. 이 독립성이 나중에 triage와 remediation에서 유용해진다.

## 이 과제의 위치

- **과제 01 → 이 과제**: "요청이 허용되는가"에서 "정책이 얼마나 위험한가"로 질문이 바뀐다
- **이 과제 → 과제 05**: IAM finding 구조가 CSPM finding 구조와 동일한 형태로 이어진다
- **이 과제 → 과제 06**: finding을 입력으로 받아 remediation dry-run을 만드는 과제
- **이 과제 → 과제 10**: Control Plane의 scan API가 IAM policy path를 받아서 같은 분석을 수행한다

## 한계와 v1 범위

- SCP(Service Control Policy)와 Permission Boundary는 다루지 않는다.
- Condition keys를 통한 권한 축소(narrowing)는 분석하지 않는다.
- Policy variables (`${aws:username}` 등)는 해석하지 않는다.
- cross-account trust relationship은 범위 밖이다.
