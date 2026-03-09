# Source Brief — 개발 타임라인

이 문서는 stage 00을 처음부터 끝까지 재현하기 위해 필요한 모든 단계를 시간순으로 기록합니다.
소스코드에는 남지 않는 CLI 명령, 설치 과정, 파일 생성 순서를 포함합니다.

---

## Phase 1: 프로젝트 구조 초기화

### 1-1. Python 프로젝트 디렉터리 생성

```bash
mkdir -p 00-source-brief/python/src/stage00
mkdir -p 00-source-brief/python/tests
touch 00-source-brief/python/src/stage00/__init__.py
```

### 1-2. pyproject.toml 작성

```bash
# 00-source-brief/python/pyproject.toml
```

- `requires-python = ">=3.12,<3.13"`으로 Python 버전을 고정
- `dependencies = []`로 외부 의존성 없음을 명시
- dev 그룹에 `pytest>=9.0.0`만 추가

### 1-3. uv 환경 세팅

```bash
cd 00-source-brief/python
uv sync --extra dev
```

`uv`는 이 프로젝트 전체에서 Python 패키지 관리자로 사용된다. `pip` 대신 `uv`를 선택한 이유는 lock 파일 기반의 재현 가능한 환경과 빠른 속도 때문이다.

---

## Phase 2: 핵심 코드 작성

### 2-1. reference spine 상수 정의

`python/src/stage00/source_brief.py` 파일을 생성하고, 맨 위에 `REFERENCE_SPINE` tuple을 작성했다.
이 tuple은 이 트랙을 이해하기 위해 읽어야 할 핵심 문서 5개를 나열한다.

### 2-2. SourceBrief dataclass 작성

같은 파일에 `SourceBrief`를 `frozen=True` dataclass로 정의했다.
필드는 `topic`, `capstone_goal`, `baseline_version`, `primary_stack` 네 가지다.

### 2-3. build_source_brief() 팩토리 함수 작성

dataclass 인스턴스를 생성하는 팩토리 함수를 추가했다.
직접 생성자를 호출하는 대신 팩토리를 쓴 이유는, 후속 stage에서 import할 때 **인터페이스를 한 곳으로 모으기 위해서**다.

---

## Phase 3: 테스트 작성 및 실행

### 3-1. conftest.py 배치

```bash
touch 00-source-brief/python/tests/conftest.py
```

pytest가 `src/` 아래 모듈을 찾을 수 있도록 conftest를 배치했다.

### 3-2. test_source_brief.py 작성

검증 항목:
- `brief.topic == "챗봇 상담 품질 관리"`
- `brief.baseline_version == "08/v0-initial-demo"`
- `"FastAPI" in brief.primary_stack`
- `len(REFERENCE_SPINE) == 5`

이 네 가지 assertion은 "source brief가 drift하지 않았다"를 보장한다.

### 3-3. 테스트 실행

```bash
cd 00-source-brief/python
uv run pytest -q
```

기대 결과: `1 passed`

---

## Phase 4: 문서 작성

### 4-1. stage README 작성

`00-source-brief/README.md`를 작성했다. stage의 목적, capstone 연결, 구현 포인터를 포함한다.

### 4-2. docs/ 및 problem/ 디렉터리 생성

```bash
mkdir -p 00-source-brief/docs
mkdir -p 00-source-brief/problem
```

`docs/`에는 acceptance criteria와 durable index를, `problem/`에는 scope와 input/output 정의를 배치했다.

---

## Phase 5: 검증 체크리스트

| 검증 항목 | 명령어 | 기대 결과 |
|-----------|--------|-----------|
| 테스트 통과 | `cd python && uv run pytest -q` | 1 passed |
| Python 버전 확인 | `python --version` | 3.12.x |
| stack contract 고정 | 테스트에서 `"FastAPI" in primary_stack` 확인 | True |
| reference spine 길이 | 테스트에서 `len(REFERENCE_SPINE) == 5` 확인 | True |

---

## 이 단계에서 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| `uv` | Python 패키지 관리 및 가상환경 |
| `pytest` | 테스트 실행 |
| Python 3.12 | 런타임 |
| `dataclasses` (stdlib) | frozen dataclass로 계약 고정 |
