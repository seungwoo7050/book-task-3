> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Quality Rubric — 접근 방식: rubric과 judge를 왜 분리했는가

## 핵심 결정

### 1. rubric과 grade band를 judge로부터 분리

처음에는 judge가 "총점 85, grade A"를 한 번에 반환하는 구조를 생각했다.
하지만 이렇게 하면 judge를 heuristic에서 LLM으로 교체할 때, 총점 계산 규칙도 바뀐다.

실제로 겪은 상황: heuristic judge가 correctness 90점을 주고, LLM judge는 같은 답변에 correctness 75점을 미겼다.
이때 **총점이 다른 이유가 judge의 판단 때문인지, 계산 규칙 때문인지** 구분이 안 됐다.

그래서 judge는 **각 축의 subscore만 내놓고**, 최종 점수 계산은 `merge_score()`가 별도로 담당하게 분리했다.
이렇게 하면 judge가 바뀌어도 merge contract는 같은 테스트로 검증된다.

### 2. critical failure를 별도 branch로 처리

가중 평균 안에서 critical severity를 표현하는 방법도 생각했다. 예를 들어 compliance에 0점을 주면 총점이 내려가니까.
하지만 compliance가 0이어도 다른 축이 높으면 총점이 60~70점대로 나온다. "PII를 노출했는데 C등급"이 되는 건 말이 안 됐다.

그래서 `critical=True`이면 **어떤 subscore든 무시하고** 즉시 `{"total": 0.0, "grade": "CRITICAL"}`을 반환하도록 분기했다.
이건 단순한 if문이지만, 설명 가능성과 회귀 검증에서 큰 차이를 만든다.

## 선택하지 않은 방향

- **judge 프롬프트가 자유롭게 총점을 반환하도록 두는 방식**: judge를 교체하면 점수 규칙도 바뀌어서 회귀 비교가 불가능해진다.
- **grade band 없이 raw score만 저장하는 방식**: 숫자만 있으면 "이게 좋은 건지 나쁜 건지" 해석이 맥락에 의존하게 된다.

## 이 선택이 후속 stage에 미친 영향

- v0~v2 모두 같은 scoring vocabulary(`WEIGHTS`, `GRADE_BANDS`, `merge_score`)를 사용한다.
- dashboard overview의 평균 점수와 grade 분포는 이 contract를 전제로 해석된다.
- stage 05에서 judge와 merge를 연결할 때, 이 단계에서 고정한 인터페이스를 그대로 사용했다.
