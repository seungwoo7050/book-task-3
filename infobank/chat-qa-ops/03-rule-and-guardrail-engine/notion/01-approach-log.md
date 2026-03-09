# Guardrail Engine — 접근 방식: failure type 분리와 JSON 규칙 파일

## 핵심 결정

### 1. 실패 원인을 네 가지 독립 코드로 분리

처음에는 "compliance violation"이라는 하나의 generic bucket으로 시작했다.
하지만 dashboard에서 "어떤 종류의 실패가 많은가?"를 보여줘야 할 때, generic bucket은 아무 정보도 주지 않았다.

"본인확인 누락"과 "과장 약속"은 전혀 다른 문제다. 전자는 절차를 빠뜨린 것이고, 후자는 존재하지 않는 약속을 한 것이다.
golden set에서 회귀를 분석할 때도, failure type별로 "어떤 종류의 실패가 줄었는가"를 보는 게 "compliance 점수가 올랐다"보다 훨씬 유용했다.

### 2. 정책 소스를 JSON으로 분리하고, 엔진은 단순 membership 검사로 유지

`rules.json`에는 `forbidden_promises`, `pii_patterns`, `escalation_terms` 세 개의 키워드 목록이 들어간다.
엔진은 이 목록에 대해 `any(term in text for term in terms)` 수준의 검사만 한다.

왜 이렇게 단순하냐면, stage 목표가 **regex DSL 확장이 아니라 규칙 종류를 분명히 드러내는 것**이기 때문이다.
규칙의 sophistication은 capstone에서 올리면 되고, 여기서는 taxonomy가 핵심이다.

### 3. mandatory notice는 규칙 파일이 아니라 코드에서 직접 처리

해지/환불/명의변경 키워드가 사용자 메시지에 있을 때 답변에 "본인확인"이 없으면 실패 — 이 규칙은 다른 세 규칙과 형태가 다르다.
다른 규칙은 "특정 단어가 있으면 실패"이지만, 이 규칙은 "특정 단어가 없으면 실패"다.
그래서 JSON에 넣기보다 코드에서 직접 구문으로 처리했다.

## 선택하지 않은 방향

- **stage 단계에서 LLM safety classifier에 의존하는 방식**: LLM이 바뀌면 결과가 바뀌어서 deterministic regression이 불가능해진다.
- **하나의 generic compliance score만 남기고 failure type을 버리는 방식**: 개선 효과를 증빙할 때 "어떤 failure가 줄었다"가 핵심 논거가 된다.

## 이 선택이 후속 stage에 미친 영향

- v0에서 추가한 escalation rule과 guardrail tests는 이 stage의 taxonomy를 확장한 것이다.
- failure codes는 dashboard failures 페이지와 golden set assertion의 **공통 언어**가 되었다.
- stage 05에서 judge가 failure_types를 받아서 correctness에 반영하고, stage 06에서 golden case assertion이 failure type 감소를 추적한다.
