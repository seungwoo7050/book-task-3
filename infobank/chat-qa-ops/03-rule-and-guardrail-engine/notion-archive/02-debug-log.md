# Guardrail Engine — 디버깅 기록: escalation 규칙이 보이지 않았던 문제

## Case: 민원/분쟁 표현이 들어와도 상담원 이관 부재가 따로 표시되지 않음

### 증상

"분쟁 접수하고 싶어요"라는 사용자 메시지에 "정책만 안내드립니다"라고 답한 케이스를 테스트했을 때,
기대한 `ESCALATION_MISS`가 나오지 않았다.

guardrail 엔진을 돌리면 `MISSING_MANDATORY_STEP`만 나왔다. 왜냐하면 "분쟁"이 연관된 규칙이 mandatory notice와 같은 bucket에 있었기 때문이다.

### 원인

초기 구현에서 escalation 규칙을 mandatory notice와 **같은 조건 블록**으로 섞어놨다.
"민원", "분쟁" 키워드가 있으면 mandatory notice의 트리거 목록에 들어가 있었고, 결과적으로 `MISSING_MANDATORY_STEP`이 먼저 반환되면서 escalation 이슈가 가려졌다.

문제는 "mandatory step 누락"과 "escalation 미안내"는 **원인도 해결책도 다르다**는 것이다.
전자는 "본인확인을 빠뜨렸다"이고, 후자는 "상담원에게 연결해야 하는데 안 했다"이다.

### 해결

escalation을 **전용 failure type과 trigger term 목록**으로 분리했다.
`rules.json`에 `escalation_terms: ["민원", "분쟁", "환불 거절", "피해"]`를 별도 키로 추가하고,
코드에서 escalation 조건을 mandatory notice와 **독립적인 if 블록**으로 분리했다.

### 검증

`test_escalation_rule`이 `ESCALATION_MISS`를 **직접** 기대한다.
"분쟁 접수하고 싶어요" + "정책만 안내드립니다" → `ESCALATION_MISS` in failures.

## 이 경험에서 배운 것

failure type을 합치면 구현은 단순해지지만, **원인 분석이 불가능**해진다.
"어떤 규칙이 위반됐는지"를 모르면 "어떻게 고칠지"도 모른다.
failure taxonomy는 처음부터 **분리가 기본**이고, 합치는 건 나중에 해도 된다.
