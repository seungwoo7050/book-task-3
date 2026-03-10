# 회고

## 이 프로젝트가 실제로 증명한 것

- 이 프로젝트는 단순 허용/거부 판단이 끝이 아니라, 운영자가 triage할 수 있는 finding 레코드로 변환하는 단계가 따로 필요함을 증명했습니다.
- broad admin과 privilege escalation을 다른 control_id로 분리함으로써, 위험 축이 다르면 설명 구조도 달라져야 한다는 점을 고정했습니다.
- safe policy가 빈 리스트를 반환하는 negative test는 analyzer가 오탐을 줄이는 방향으로 설계됐다는 직접 근거입니다.

## 이번 버전이 의도적으로 단순화한 것

- Condition, SCP, permission boundary, 서비스별 fine-grained semantics는 아직 포함하지 않았습니다.
- escalation action 목록은 외부 룰셋이 아니라 코드 내부의 제한된 집합입니다.
- severity는 정교한 scoring 시스템이 아니라 학습용 규칙 기반 분류입니다.

## 학습자가 여기서 반드시 가져가야 할 판단

- 보안 analyzer 초반 단계에서는 rule 수를 늘리는 것보다, false positive를 줄이는 negative test를 먼저 확보하는 편이 낫습니다.
- finding 구조는 결과 메시지보다 `control_id`, `severity`, `resource_id`처럼 뒤 시스템이 재사용할 필드를 먼저 안정화해야 합니다.
- 이 프로젝트가 성공하려면 broad policy 1건을 잡는 것보다, secure/scoped policy를 억지로 위험하게 만들지 않는 것이 더 중요합니다.

## 공개 기록으로 확장할 때 보강할 증거

- 공개용 문서에서는 `broad_admin_policy.json`과 `scoped_policy.json`을 나란히 두고 왜 하나만 위험한지 설명하는 편이 설득력이 큽니다.
- `IAM-001`, `IAM-002`, `IAM-003` 각 control이 어떤 운영 질문을 대신하는지 표로 정리하면 더 좋습니다.
- 다음 단계인 remediation과의 연결을 보여 주려면, finding dict 예시를 하나 캡처해 두는 편이 실용적입니다.
