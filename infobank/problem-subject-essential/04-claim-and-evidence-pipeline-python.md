# 04-claim-and-evidence-pipeline-python 문제지

## 왜 중요한가

답변의 어떤 문장을 어떤 문서가 뒷받침하는지 어떻게 추적 가능하게 저장할 것인가?

## 목표

시작 위치의 구현을 완성해 각 claim 결과에 retrieval query와 matched docs가 남는다, 근거가 없는 문장도 not_found로 기록되어 silent drop이 없다, 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/src/stage04/__init__.py`
- `../projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/src/stage04/pipeline.py`
- `../projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/tests/test_pipeline.py`
- `../projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python/src/stage04/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 각 claim 결과에 retrieval query와 matched docs가 남는다.
- 근거가 없는 문장도 not_found로 기록되어 silent drop이 없다.
- 후속 judge와 dashboard가 같은 trace 구조를 사용할 수 있다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `extract_claims`와 `verify_claims`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_claim_pipeline_keeps_retrieval_trace`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/04-claim-and-evidence-pipeline/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`04-claim-and-evidence-pipeline-python_answer.md`](04-claim-and-evidence-pipeline-python_answer.md)에서 확인한다.
