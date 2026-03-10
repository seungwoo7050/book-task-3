# 04 주장-근거 추적 파이프라인 문제 정의

답변에서 claim을 분리하고 각 claim에 retrieval trace와 verdict trace를 남기는 groundedness 검증 단계를 다룬다.

## 문제 해석

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?

## 입력

- assistant response text
- seeded knowledge base 또는 doc_id -> content 매핑

## 기대 산출물

- claim list
- claim별 `support` 또는 `not_found` verdict
- retrieval trace와 evidence_doc_ids

## 완료 기준

- 각 claim 결과에 retrieval query와 matched docs가 남는다.
- 근거가 없는 문장도 `not_found`로 기록되어 silent drop이 없다.
- 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.

## 현재 확인 가능한 증거

- `python/tests/test_pipeline.py`가 retrieval trace 보존을 직접 검증한다.
- pipeline은 vector DB 없이도 trace schema를 설명 가능하게 유지한다.

## 이 pack에서 바로 확인할 수 있는 것

- 구현 디렉터리: claim trace, retrieval trace and verdict trace
- 이번 단계에서 일부러 제외한 범위: LLM provider 없음
- 검증 명령: `cd python && UV_PYTHON=python3.12 uv run pytest -q`
