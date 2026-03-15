# 04 IAM Policy Analyzer structure outline

## 중심 질문

- 이 analyzer가 왜 "위험 정책을 찾는다"가 아니라 "remediation 가능한 control 단위로 자른다"는 이야기로 읽혀야 하는지
- broad admin, passrole, safe policy가 각각 어떤 품질 기준 역할을 하는지

## 글 흐름

1. 결과 스키마를 먼저 고정한 이유로 시작한다.
2. broad admin을 `IAM-001`과 `IAM-002`로 나누는 장면을 두 번째 축으로 둔다.
3. passrole fixture가 `IAM-002`와 `IAM-003`을 동시에 내는 구조를 세 번째 축으로 둔다.
4. scoped policy 0건과 exact-match 기반 현재 한계를 마지막에 남긴다.

## 반드시 남길 증거

- `Finding` dataclass와 `findings_as_dicts()`
- `IAM-001`, `IAM-002`, `IAM-003` 생성 조건
- broad admin CLI 출력 2건
- passrole CLI 출력 2건
- scoped CLI `[]`
- `2026-03-14` pytest `3 passed in 0.01s`

## 반드시 피할 서술

- 이 analyzer가 IAM 전체 위험 모델을 구현한 것처럼 보이게 하는 과장
- passrole fixture를 `IAM-003`만 나오는 예제로 축소하는 문장
- false positive 0건 기준을 빼먹고 탐지 개수만 강조하는 설명
- `s3:*` 같은 wildcard family도 이미 세밀하게 해석한다고 오해하게 만드는 표현

## 톤 체크

- chronology는 `finding shape -> broad split -> escalation split -> safe 0건과 한계` 순서로 살아 있어야 한다.
- 홍보문보다 "어떤 질문을 control 단위로 분리했는가"와 "무엇이 아직 exact rule 기반인가"가 함께 읽히는 탐색형 톤을 유지한다.
