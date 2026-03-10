# 접근 기록

## 핵심 선택

- 결과를 단순 경고 문자열이 아니라 `Finding` 구조체로 고정했습니다. 그래야 뒤 프로젝트에서 그대로 재사용할 수 있습니다.
- broad policy와 escalation action을 서로 다른 control로 분리했습니다. remediation 우선순위가 다르기 때문입니다.
- read-only prefix를 분리해 `Resource=*`라도 무조건 위험으로 치지 않도록 했습니다.

## 버린 대안

- wildcard가 있으면 전부 고위험으로 처리하는 단순 규칙은 포기했습니다. scoped read-only 정책에서 오탐이 심해집니다.
- AWS 공식 권한 참조를 전부 파싱하는 방식은 현재 범위에 비해 과합니다.
- 하나의 policy에서 finding 하나만 나오게 제한하지 않았습니다. 실제 운영에서는 여러 규칙이 동시에 걸릴 수 있기 때문입니다.

## 다음 프로젝트와의 연결

이 프로젝트의 진짜 산출물은 finding 구조입니다. `05-cspm-rule-engine`과 `10-cloud-security-control-plane`이 같은 구조를
재사용하므로, 지금 단계에서 `control_id`, `severity`, `resource_type`, `resource_id`, `evidence_ref`를 분명하게 잡아 두는 것이 중요합니다.

## 다시 써도 유지할 기준

- 오탐을 줄이는 기준이 문서화되어 있어야 합니다.
- finding은 사람이 읽을 수 있어야 합니다.
- 뒤 프로젝트에서 바로 재사용할 수 있는 필드 구조를 유지해야 합니다.
