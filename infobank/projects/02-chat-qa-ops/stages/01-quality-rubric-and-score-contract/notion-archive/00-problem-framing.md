> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Quality Rubric — 왜 "점수 체계"를 가장 먼저 고정해야 했는가

## 출발점

상담 품질을 평가하겠다는 목표가 잡힌 뒤, 자연스러운 다음 질문은 이것이었다:

> "좋은 상담이란 뭔가? 그걸 어떤 숫자로 표현할 건가?"

처음에는 "LLM judge가 알아서 점수를 내면 되지 않나"라고 생각했다. 프롬프트에 "1~100점으로 평가해줘"라고 쓰면 숫자가 나오니까.
하지만 문제는 **비교**에서 생겼다. v0에서 나온 85점과 v1에서 나온 87점이 **같은 기준으로 나온 숫자인지** 보장할 수 없었다.

judge가 바뀌면 점수도 바뀐다. 프롬프트가 바뀌면 점수도 바뀐다.
결국 "점수 계산 규칙 자체"를 judge로부터 분리해서 고정하지 않으면, 나중에 개선 효과를 증빙할 방법이 없다는 결론에 이르렀다.

## 이 단계가 해결하려는 것

핵심 질문:

> "정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?"

이 단계를 마치면 세 가지가 고정된다:

1. **Weight 총합이 항상 1.0**이다 — correctness 30%, groundedness 25%, compliance 20%, resolution 15%, communication 10%.
2. **Critical failure는 어떤 점수보다 우선**한다 — 100점짜리 답변이라도 compliance 위반이 있으면 `CRITICAL`, total 0.0.
3. **Grade band**가 A/B/C/D/F로 일관되게 분류된다 — A≥90, B≥75, C≥60, D≥40, 나머지 F.

## 성공 기준

- weight 총합이 `1.0`으로 유지된다.
- critical failure는 어떤 점수보다 우선한다.
- grade band가 후속 stage와 capstone에서 재사용 가능하다.

## 이 트랙을 처음 보는 사람을 위한 전제

- 이 단계는 **LLM judge의 품질**을 검증하는 게 아니다. judge가 뭘 반환하든, 최종 점수는 **이 rubric의 규칙대로** 계산된다는 것을 보장하는 단계다.
- QA Ops의 목표가 상담 품질을 **수치화하고 비교**하는 것임을 이해하면, 왜 점수 체계를 이 시점에서 고정해야 하는지 납득된다.
- weight 값 자체가 인간 평가자 합의로 교정된 것은 아니다. 이 단계의 목적은 calibration이 아니라 **contract freeze**다.
