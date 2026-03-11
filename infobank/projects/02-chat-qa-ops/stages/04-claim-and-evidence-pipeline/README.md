# 04 주장-근거 추적 파이프라인

## 이 stage의 문제

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 추적 가능하게 저장하는 구조를 만든다.

## 입력/제약

- 입력: assistant response text, seeded knowledge base, doc mapping
- 제약: 근거가 없는 문장도 silent drop 없이 남겨야 한다.

## 이 stage의 답

- claim extraction, retrieval trace, verdict trace를 분리한다.
- 후속 judge와 dashboard가 같은 provenance 구조를 재사용하게 만든다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/src/stage04/pipeline.py`
- `projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/backend/src/evaluator/evidence_verifier.py`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- 실제 provider 연동은 포함하지 않는다.
- vector DB나 retrieval infra 전체를 다루지는 않는다.
