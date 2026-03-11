> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Source Brief — 접근 방식: 왜 dataclass와 상수 tuple이었나

## 고민의 시작

프로젝트 방향을 기록하는 가장 쉬운 방법은 README에 자연어로 쓰는 것이다.
실제로 처음에는 그렇게 했다. "주제는 상담 품질 관리, 스택은 Python + FastAPI..."라고 써두면 됐다.

그런데 문제는 후속 stage를 만들면서 생겼다.
stage 03에서 guardrail 규칙을 설계할 때 "우리 스택에 React가 포함이었나?"라는 질문이 나왔고, stage 07에서 dashboard를 만들 때 baseline 버전이 `v0`인지 `v0-initial-demo`인지 미묘하게 흔들렸다.
문서마다 stack 설명이 조금씩 달라질 수 있다는 걸 체감한 순간, **코드 객체로 고정하자**는 방향이 정해졌다.

## 선택한 방향

### 1. `SourceBrief`를 frozen dataclass로 표현

```
topic: "챗봇 상담 품질 관리"
capstone_goal: "QA Ops 플랫폼 데모 완성"
baseline_version: "08/v0-initial-demo"
primary_stack: ("Python 3.12", "FastAPI", "Pydantic", "SQLAlchemy", "React", "PostgreSQL", "Langfuse")
```

`frozen=True`로 만든 이유는 명확하다. 이 값은 stage 전체에서 **변경 없이 참조**되어야 한다. 누군가 실수로 `primary_stack`에 항목을 추가하면 테스트가 깨지도록 만들고 싶었다.

### 2. Reference spine을 다섯 문서로 제한

```python
REFERENCE_SPINE = (
    "README.md",
    "docs/legacy-intent-audit.md",
    "docs/project-selection-rationale.md",
    "docs/curriculum-map.md",
    "docs/reference-spine.md",
)
```

왜 다섯 개냐면, 읽어야 할 문서 수를 **최소화**하기 위해서다.
이 저장소를 처음 보는 사람이 "어디서부터 읽어야 하지?"라고 물으면, reference spine에 있는 다섯 문서를 순서대로 읽으면 된다.

## 선택하지 않은 방향

- **README 서술만 남기고 코드 계약은 만들지 않는 방식**: 이게 가장 쉽지만, stage가 8개까지 이어지는 구조에서 서술적 기록은 drift의 원인이 된다.
- **legacy 디렉터리 구조를 그대로 학습 sequence로 간주하는 방식**: legacy 구조는 과거 의도를 반영하고 있어서, 새 커리큘럼의 순서가 거기에 종속되면 유연성이 사라진다.

## 이 선택이 후속 stage에 미친 영향

- `08/v0`를 기준점으로 삼는 이유가 source brief에서 명시적으로 고정되었다.
- 이후 모든 README와 verification 문서는 이 source brief의 stack, baseline 정보를 따르게 되었다.
- stage 01의 rubric weight부터 stage 07의 dashboard snapshot까지, "우리가 쓰는 스택은 무엇인가"라는 질문에 대한 답이 코드 한 곳에서 나온다.
