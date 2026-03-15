# 01-quality-rubric-and-score-contract-python 문제지

## 왜 중요한가

정성적 상담 품질을 어떤 weighted rubric과 critical override 규칙으로 일관되게 계산할 것인가?

## 목표

시작 위치의 구현을 완성해 weight 총합이 1.0으로 유지된다, critical failure는 어떤 점수보다 우선한다, grade band가 후속 stage와 capstone에서 재사용 가능하다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/src/stage01/__init__.py`
- `../projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/src/stage01/rubric.py`
- `../projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/tests/test_rubric.py`
- `../projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python/src/stage01/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- weight 총합이 1.0으로 유지된다.
- critical failure는 어떤 점수보다 우선한다.
- grade band가 후속 stage와 capstone에서 재사용 가능하다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `to_grade`와 `merge_score`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_weights_sum_to_one`와 `test_critical_override_wins`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/01-quality-rubric-and-score-contract/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-quality-rubric-and-score-contract-python_answer.md`](01-quality-rubric-and-score-contract-python_answer.md)에서 확인한다.
