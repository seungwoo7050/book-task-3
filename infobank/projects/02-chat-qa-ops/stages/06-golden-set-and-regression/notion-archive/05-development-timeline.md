> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Golden Set & Regression — 개발 타임라인

## 1단계: 디렉터리 생성

```bash
mkdir -p chat-qa-ops/06-golden-set-and-regression/python/{src/stage06,tests,data}
```

## 2단계: golden_cases.json 작성

```bash
cat > chat-qa-ops/06-golden-set-and-regression/python/data/golden_cases.json << 'EOF'
{
  "cases": [
    {
      "id": "gs-001",
      "required_evidence_doc_ids": ["refund_policy.md"]
    },
    {
      "id": "gs-002",
      "required_evidence_doc_ids": ["identity_verification.md"]
    }
  ]
}
EOF
```

데이터 파일을 먼저 만든 이유: evaluate_case()의 입력 형태를 데이터 기준으로 결정하기 위해서다.
코드보다 데이터가 먼저 있으면 인터페이스 설계가 자연스러워진다.

## 3단계: compare_manifest.json 작성

```bash
cat > chat-qa-ops/06-golden-set-and-regression/python/data/compare_manifest.json << 'EOF'
{
  "baseline": "v1.0",
  "candidate": "v1.1",
  "dataset": "golden-set"
}
EOF
```

## 4단계: pyproject.toml 작성

```bash
cat > chat-qa-ops/06-golden-set-and-regression/python/pyproject.toml << 'EOF'
[project]
name = "stage06-golden-set-and-regression"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF
```

외부 패키지 의존성 없음. json과 pathlib만 사용한다.

## 5단계: regression.py 구현

```bash
touch chat-qa-ops/06-golden-set-and-regression/python/src/stage06/__init__.py
# regression.py 작성
```

구현 순서:
1. `evaluate_case(required_doc_ids, actual_doc_ids)` — any() 기반 통과 판정 + reason_codes 반환
2. `load_manifest(path)` — JSON 파일을 dict로 로드

두 함수 모두 5줄 이내로 완료된다.

## 6단계: 테스트 작성 및 실행

```bash
touch chat-qa-ops/06-golden-set-and-regression/python/tests/test_regression.py
```

테스트 내용:
1. required doc가 actual에 있으면 passed=True
2. manifest에서 baseline/candidate 버전이 올바르게 로드되는지

```bash
cd chat-qa-ops/06-golden-set-and-regression/python
uv run pytest tests/ -x -v
```

## 7단계: README 정리

```bash
cat > chat-qa-ops/06-golden-set-and-regression/python/README.md << 'EOF'
# Stage 06 — Golden Set & Regression
...
EOF
```

## 비고

- 이 stage는 전체 stage 중 코드량이 가장 적다 (regression.py가 11줄).
- 복잡도가 낮은 대신, 데이터 설계(golden_cases.json의 구조)가 핵심이다.
- 실제 운영에서는 golden case를 CI에 연결하여 PR마다 자동 실행하는 것이 목표다.
