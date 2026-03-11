> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Judge & Score Merge — 접근 방식: heuristic judge와 merge 분리

## 핵심 결정

### 1. judge는 subscore와 failure types를 만들고, merge는 final score만 계산

이 분리의 핵심 이유: **LLM judge를 도입하더라도 final scoring contract는 별도로 검증 가능해야** 하기 때문이다.

구체적으로:
- `judge_response()` → `{correctness, resolution, communication, failure_types}`
- `merge_score()` → `float` (final weighted total)

merge는 stage 01의 `WEIGHTS`와 동일한 가중치를 사용한다.
judge가 바뀌어도 merge의 테스트는 그대로 돌아간다.

### 2. stage pack에서는 heuristic judge를 유지

"왜 LLM을 안 쓰나?"라는 질문에 대한 답: 외부 모델 의존성 없이도 **score merge 구조를 설명하고 테스트**할 수 있어야 하기 때문이다.

heuristic judge의 기준:
- `correctness`: `90.0 - len(failures) * 10` — failure가 많을수록 감점
- `resolution`: 응답 길이가 10자 초과면 85, 아니면 70
- `communication`: "안내" 또는 "확인" 표현이 있으면 85, 없으면 75

이 기준은 명백히 **조잡하다**. 하지만 이 stage의 목표는 judge의 정교함이 아니라 **judge와 merge 사이의 경계**를 보는 것이다.

## 선택하지 않은 방향

- **judge가 총점까지 직접 반환하는 monolithic evaluator**: judge 교체 시 점수 체계도 바뀌어서 회귀 비교 불가능
- **groundedness/compliance를 judge 내부 추정치로만 숨기는 방식**: stage 04(evidence pipeline)와 stage 03(guardrail)의 output을 merge에서 합산해야 하므로, judge가 독자적으로 추정하면 중복과 불일치가 생김

## 이 선택이 후속 stage에 미친 영향

- v1의 LLM judge trace와 stage 01 rubric contract 사이를 잇는 **중간 역할**을 한다.
- provider가 바뀌어도 merge contract는 유지된다는 점을 이 stage에서 보여줬다.
- stage 07 dashboard의 점수 표시는 이 merge 함수의 출력을 전제로 한다.
