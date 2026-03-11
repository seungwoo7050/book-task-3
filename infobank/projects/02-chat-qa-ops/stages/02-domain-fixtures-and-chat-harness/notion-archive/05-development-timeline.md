> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Domain Fixtures — 개발 타임라인

이 문서는 stage 02를 처음부터 끝까지 재현하기 위해 필요한 모든 단계를 시간순으로 기록합니다.

---

## Phase 1: 프로젝트 구조 생성

### 1-1. 디렉터리 생성

```bash
mkdir -p 02-domain-fixtures-and-chat-harness/python/src/stage02
mkdir -p 02-domain-fixtures-and-chat-harness/python/tests
mkdir -p 02-domain-fixtures-and-chat-harness/python/data/knowledge_base
touch 02-domain-fixtures-and-chat-harness/python/src/stage02/__init__.py
```

### 1-2. pyproject.toml 작성

- `name = "study2-stage02"`
- `requires-python = ">=3.12,<3.13"`
- `dependencies = []` — json과 pathlib은 stdlib
- dev: `pytest>=9.0.0`

### 1-3. 환경 설정

```bash
cd 02-domain-fixtures-and-chat-harness/python
uv sync --extra dev
```

---

## Phase 2: Seeded Knowledge Base 작성

### 2-1. refund_policy.md 작성

`data/knowledge_base/refund_policy.md`에 환불 정책 내용을 한국어로 작성했다.
핵심 키워드: 환불, 본인확인, 접수

### 2-2. identity_verification.md 작성

`data/knowledge_base/identity_verification.md`에 본인확인 절차를 작성했다.
핵심 키워드: 본인확인, 인증, 상담원

### 2-3. cancellation_policy.md 작성

`data/knowledge_base/cancellation_policy.md`에 해지 정책을 작성했다.
핵심 키워드: 해지, 위약금, 잔여 기간

---

## Phase 3: Replay Session Fixture 작성

### 3-1. replay_sessions.json 작성

`data/replay_sessions.json`에 두 개의 세션을 작성했다:
- `"환불은 몇일 걸려요?"` → 기대 문서: `refund_policy.md`
- `"해지 신청은 본인확인 없이 가능해요?"` → 기대 문서: `identity_verification.md`

이 파일은 stage 06의 golden cases와 세트로 사용된다.

---

## Phase 4: Harness 구현

### 4-1. seed_knowledge_base() 함수 작성

`python/src/stage02/harness.py`에 KB 로딩 함수를 작성했다.
`Path.glob('*.md')`로 knowledge_base 디렉터리의 모든 Markdown을 읽어 `{filename: content}` dict로 반환한다.

### 4-2. retrieve() 함수 작성

질의어를 공백으로 split한 뒤, 각 term이 문서 본문이나 doc_id에 포함되는지 확인하는 keyword matching.
점수가 높은 순서로 정렬해서 문서 목록을 반환한다.
매칭이 하나도 없으면 KB의 첫 번째 문서를 기본값으로 반환한다.

### 4-3. run_replay() 함수 작성

replay_sessions.json을 읽고, 각 세션의 `user_message`에 대해 `retrieve()`를 호출해서 결과를 모은다.
반환값: `{session_count, items: [{user_message, retrieved_doc_ids}]}`

---

## Phase 5: 테스트 작성 및 검증

### 5-1. 두 가지 테스트 작성

| 테스트 | 검증 대상 |
|--------|-----------|
| `test_seeded_kb_reproducible` | KB 파일 세 개가 정확히 로드되는지 |
| `test_replay_harness_reproduces_expected_docs` | 첫 번째 replay의 top-1이 `refund_policy.md`인지 |

### 5-2. 테스트 실행

```bash
cd 02-domain-fixtures-and-chat-harness/python
uv run pytest -q
```

기대 결과: `2 passed`

---

## 이 단계에서 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| `uv` | Python 패키지 관리 및 가상환경 |
| `pytest` | 테스트 실행 |
| Python 3.12 | 런타임 |
| `json` (stdlib) | replay session 파싱 |
| `pathlib` (stdlib) | 파일 경로 처리 |
