# Claim & Evidence Pipeline — 개발 타임라인

이 문서는 stage 04를 처음부터 끝까지 재현하기 위해 필요한 모든 단계를 시간순으로 기록합니다.

---

## Phase 1: 프로젝트 구조 생성

### 1-1. 디렉터리 생성

```bash
mkdir -p 04-claim-and-evidence-pipeline/python/src/stage04
mkdir -p 04-claim-and-evidence-pipeline/python/tests
touch 04-claim-and-evidence-pipeline/python/src/stage04/__init__.py
```

### 1-2. pyproject.toml 작성

- `name = "study2-stage04"`
- `requires-python = ">=3.12,<3.13"`
- `dependencies = []`
- dev: `pytest>=9.0.0`

### 1-3. 환경 설정

```bash
cd 04-claim-and-evidence-pipeline/python
uv sync --extra dev
```

---

## Phase 2: Pipeline 구현

### 2-1. extract_claims() 함수 작성

`python/src/stage04/pipeline.py`에 claim extraction 함수를 작성했다.

동작 방식:
1. 텍스트의 `?`를 `.`로 치환
2. `.`으로 split
3. 빈 문자열 제거
4. 각 문장에 `claim_id` 부여 (`claim-1`, `claim-2`, ...)

### 2-2. verify_claims() 함수 작성

각 claim에 대해:
1. claim의 `statement`를 단어(공백 split)로 분해
2. KB의 각 문서에서 해당 단어가 포함되는지 확인
3. 매칭된 문서가 있으면 `verdict: "support"`, 없으면 `verdict: "not_found"`
4. retrieval trace에 **검색 쿼리(claim 문장 자체)**와 **반환된 문서 목록**을 남김
5. evidence_doc_ids에는 최대 2개의 매칭 문서를 포함

핵심: 매칭이 0이어도 결과 리스트에서 빠뜨리지 않는다.

---

## Phase 3: 테스트 작성 및 검증

### 3-1. 테스트 작성

| 테스트 | 검증 대상 |
|--------|-----------|
| `test_claim_pipeline_keeps_retrieval_trace` | 첫 claim이 `support` verdict이고 retrieval trace에 `refund_policy.md`가 포함 |

테스트에서는 inline KB(`{"refund_policy.md": "환불은 본인확인 후 접수 가능합니다."}`)를 사용해서 외부 파일 의존성을 제거했다.

### 3-2. 테스트 실행

```bash
cd 04-claim-and-evidence-pipeline/python
uv run pytest -q
```

기대 결과: `1 passed`

---

## 이 단계에서 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| `uv` | Python 패키지 관리 및 가상환경 |
| `pytest` | 테스트 실행 |
| Python 3.12 | 런타임 |
