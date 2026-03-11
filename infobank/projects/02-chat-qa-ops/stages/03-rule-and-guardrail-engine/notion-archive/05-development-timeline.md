> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Guardrail Engine — 개발 타임라인

이 문서는 stage 03을 처음부터 끝까지 재현하기 위해 필요한 모든 단계를 시간순으로 기록합니다.

---

## Phase 1: 프로젝트 구조 생성

### 1-1. 디렉터리 생성

```bash
mkdir -p 03-rule-and-guardrail-engine/python/src/stage03
mkdir -p 03-rule-and-guardrail-engine/python/tests
mkdir -p 03-rule-and-guardrail-engine/python/data
touch 03-rule-and-guardrail-engine/python/src/stage03/__init__.py
```

### 1-2. pyproject.toml 작성

- `name = "study2-stage03"`
- `requires-python = ">=3.12,<3.13"`
- `dependencies = []`
- dev: `pytest>=9.0.0`

### 1-3. 환경 설정

```bash
cd 03-rule-and-guardrail-engine/python
uv sync --extra dev
```

---

## Phase 2: 규칙 데이터 정의

### 2-1. rules.json 작성

`data/rules.json`에 세 개의 키워드 목록을 정의했다:

- `forbidden_promises`: `["무조건", "100%", "반드시"]`
- `pii_patterns`: `["주민번호", "카드번호", "990101-1234567"]`
- `escalation_terms`: `["민원", "분쟁", "환불 거절", "피해"]`

mandatory_notice_terms는 별도로 JSON에 넣지 않고 코드에서 직접 처리하기로 결정했다.
이유: 이 규칙은 "특정 키워드가 user message에 있을 때 response에 특정 단어가 없으면 실패"라는 구조가 다른 규칙과 다르기 때문이다.

---

## Phase 3: Guardrail 엔진 구현

### 3-1. load_rules() 함수 작성

`python/src/stage03/guardrails.py`에 JSON 파일을 읽어 dict를 반환하는 함수를 작성했다.

### 3-2. evaluate() 함수 작성

네 가지 규칙을 순서대로 검사하는 함수:

1. **Mandatory notice**: `["해지", "환불", "명의변경"]` 중 하나가 user_message에 있는데 response에 `"본인확인"`이 없으면 `MISSING_MANDATORY_STEP` 추가
2. **Forbidden promise**: rules의 `forbidden_promises` 중 하나가 response에 있으면 `UNSUPPORTED_CLAIM` 추가
3. **PII exposure**: rules의 `pii_patterns` 중 하나가 response에 있으면 `PII_EXPOSURE` 추가
4. **Escalation miss**: rules의 `escalation_terms` 중 하나가 user_message에 있는데 response에 `"상담원"` 또는 `"전문 부서"`가 없으면 `ESCALATION_MISS` 추가

반환값: `list[str]` — 감지된 failure type 목록 (빈 리스트이면 문제 없음)

---

## Phase 4: 테스트 작성 및 검증

### 4-1. 네 가지 테스트 작성

| 테스트 | 입력 | 기대 failure |
|--------|------|-------------|
| `test_mandatory_notice_rule` | "해지하려면?" / "절차를 안내드리겠습니다." | `MISSING_MANDATORY_STEP` |
| `test_forbidden_promise_rule` | "할인돼요?" / "무조건 가능합니다." | `UNSUPPORTED_CLAIM` |
| `test_pii_rule` | "입력할까요?" / "주민번호 990101-1234567 입력하세요." | `PII_EXPOSURE` |
| `test_escalation_rule` | "분쟁 접수하고 싶어요" / "정책만 안내드립니다." | `ESCALATION_MISS` |

### 4-2. 테스트 실행

```bash
cd 03-rule-and-guardrail-engine/python
uv run pytest -q
```

기대 결과: `4 passed`

---

## 이 단계에서 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| `uv` | Python 패키지 관리 및 가상환경 |
| `pytest` | 테스트 실행 |
| Python 3.12 | 런타임 |
| `json` (stdlib) | 규칙 파일 파싱 |
