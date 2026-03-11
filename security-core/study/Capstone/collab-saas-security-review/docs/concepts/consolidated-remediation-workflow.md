# consolidated remediation workflow

이 capstone의 핵심은 "finding을 더 많이 만드는 것"이 아니라, 다른 성격의 판단을 같은 우선순위 언어로 다시 정렬하는 것입니다.

## 왜 offline pipeline인가

`security-core`의 foundations 프로젝트는 모두 fixture와 CLI로 재현 가능해야 한다는 공통 제약을 가집니다. capstone만 별도 서버,
DB, worker를 요구하면 앞선 프로젝트와 읽는 법이 달라지고, 통합의 핵심이 "review 판단"이 아니라 "인프라 기동"으로 밀립니다.
그래서 이 capstone은 서비스 운영을 흉내 내는 대신, 운영자가 실제로 읽는 review artifact에 집중합니다.

## 입력을 나누는 이유

- `crypto_review`: secret handling과 key lifecycle의 최소 기준을 묻는다.
- `auth_scenarios`: session, JWT, OAuth control gap을 묻는다.
- `backend_cases`: route 경계에서 필요한 방어를 묻는다.
- `dependency_bundle`: 패치 우선순위와 보완 통제를 묻는다.

각 입력은 foundations 프로젝트에서 이미 한 번 분리해 설명했던 질문을 가져오지만, capstone에서는 "무엇을 먼저 고칠까"라는
한 문장으로 다시 모입니다.

## category별로 무엇이 남는가

- crypto는 `CRYPTO-*` finding으로 "secret handling 자체가 안전한가"를 남깁니다.
- auth는 `AUTH-*` finding으로 "로그인과 세션 경계가 안전한가"를 남깁니다.
- backend는 `OWASP-*` finding으로 "route 경계의 방어가 있는가"를 남깁니다.
- dependency는 `P1`~`P4`와 action으로 "패치 queue를 어떻게 운영할 것인가"를 남깁니다.

## remediation board로 합치는 방법

1. crypto/auth/backend finding은 severity를 `P1`~`P3`로 정규화합니다.
2. dependency item은 기존 triage priority를 그대로 유지합니다.
3. 정렬은 `P1 -> P4`, 같은 priority 안에서는 `crypto -> auth -> backend -> dependency` 순서를 유지합니다.

이 정렬 규칙을 고정하면 "토큰 저장소 문제와 CVE 하나 중 무엇을 먼저 고칠까" 같은 질문을 반복 가능한 방식으로 답할 수 있습니다.

## artifact가 분리되는 이유

- `01-service-profile.json`은 경영진/리뷰어가 먼저 보는 요약입니다.
- `02`~`05`는 각 카테고리 담당자가 원인과 근거를 확인하는 상세 자료입니다.
- `06-remediation-board.json`은 작업 큐와 우선순위 정렬 결과입니다.
- `07-report.md`는 회의나 PR 설명에 그대로 붙일 수 있는 사람 읽기용 보고서입니다.

## 일부러 하지 않는 것

- 실제 API 호출, worker, queue, DB 상태 전이
- runtime policy enforcement
- 외부 advisory feed 동기화

이 capstone은 제품을 흉내 내는 것이 아니라, 통합 보안 review 문서와 artifact를 reproducible하게 만드는 데 집중합니다.
