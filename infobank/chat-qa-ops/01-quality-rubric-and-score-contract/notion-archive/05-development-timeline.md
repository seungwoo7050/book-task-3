# Quality Rubric — 개발 타임라인

이 문서는 stage 01을 처음부터 끝까지 재현하기 위해 필요한 모든 단계를 시간순으로 기록합니다.

---

## Phase 1: 프로젝트 구조 초기화

### 1-1. 디렉터리 생성

```bash
mkdir -p 01-quality-rubric-and-score-contract/python/src/stage01
mkdir -p 01-quality-rubric-and-score-contract/python/tests
touch 01-quality-rubric-and-score-contract/python/src/stage01/__init__.py
```

### 1-2. pyproject.toml 작성

- `name = "study2-stage01"`
- `requires-python = ">=3.12,<3.13"`
- `dependencies = []` — 외부 라이브러리 불필요
- dev: `pytest>=9.0.0`

### 1-3. 환경 설정

```bash
cd 01-quality-rubric-and-score-contract/python
uv sync --extra dev
```

---

## Phase 2: Rubric 구현

### 2-1. WEIGHTS 상수 정의

`python/src/stage01/rubric.py` 파일을 생성하고, 다섯 축의 weight를 dictionary로 정의했다.

- correctness: 0.30
- groundedness: 0.25
- compliance: 0.20
- resolution: 0.15
- communication: 0.10

이 값들의 합이 **정확히 1.0**이 되도록 조정했다.

### 2-2. GRADE_BANDS 상수 정의

성적 등급 경계를 tuple of tuples로 정의했다: `(("A", 90), ("B", 75), ("C", 60), ("D", 40))`.
이 순서는 `to_grade()` 함수에서 위에서 아래로 순회하면서 첫 번째로 충족되는 등급을 반환하는 데 사용된다.

### 2-3. to_grade() 함수 작성

total score를 받아 grade band에 매칭하는 함수. 어떤 band에도 해당하지 않으면 `"F"`를 반환한다.

### 2-4. merge_score() 함수 작성

**핵심 설계 결정**: 함수 진입 직후 `critical` 파라미터를 먼저 검사한다.
`critical=True`이면 가중 평균을 아예 계산하지 않고 즉시 `{"total": 0.0, "grade": "CRITICAL"}`을 반환한다.

그 다음에야 다섯 축의 가중 평균을 계산하고, `round(total, 2)`로 소수점 2자리로 반올림한다.

---

## Phase 3: 테스트 작성 및 검증

### 3-1. 세 가지 테스트 케이스 작성

| 테스트 | 검증 대상 |
|--------|-----------|
| `test_weights_sum_to_one` | weight 합산이 1.0 |
| `test_critical_override_wins` | 모든 축 100점 + critical → total 0.0, grade CRITICAL |
| `test_grade_band_contract` | 모든 축 90점 → grade A |

### 3-2. 테스트 실행

```bash
cd 01-quality-rubric-and-score-contract/python
uv run pytest -q
```

기대 결과: `3 passed`

---

## Phase 4: 문서 정리

### 4-1. stage README 작성

목적, capstone 연결, 구현 포인터를 정리했다.

### 4-2. docs/rubric-spec.md 작성

rubric의 세부 사양을 durable index로 정리했다.

---

## 이 단계에서 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| `uv` | Python 패키지 관리 및 가상환경 |
| `pytest` | 테스트 실행 |
| Python 3.12 | 런타임 |
