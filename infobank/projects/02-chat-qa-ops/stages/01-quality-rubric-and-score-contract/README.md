# 01 품질 기준과 점수 계약

## 이 stage의 문제

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할지 고정한다.

## 입력/제약

- 입력: weighted rubric, grade band, critical override 규칙
- 제약: LLM judge가 없어도 score contract 자체는 독립적으로 검증 가능해야 한다.

## 이 stage의 답

- weighted score, grade band, critical override를 독립 패키지로 분리한다.
- 이후 capstone 버전 전체가 같은 scoring vocabulary를 쓰게 만든다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/src/stage01/rubric.py`
- `projects/02-chat-qa-ops/capstone/v2-submission-polish/python/backend/src/evaluator`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- LLM judge 자체의 판단 근거는 아직 다루지 않는다.
- empirical tuning은 후속 단계에서 증빙된다.
