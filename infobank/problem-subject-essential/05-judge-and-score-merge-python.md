# 05-judge-and-score-merge-python 문제지

## 왜 중요한가

응답 품질 판단과 최종 score 계산을 어떻게 나누어야 회귀 비교와 모델 교체가 쉬운가?

## 목표

시작 위치의 구현을 완성해 judge와 scorer가 별도 함수 계약을 가진다, failure types는 판단 결과와 최종 score 계산 모두에 반영된다, live provider가 없어도 deterministic 테스트가 가능하다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/src/stage05/__init__.py`
- `../projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/src/stage05/judge.py`
- `../projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/tests/test_judge.py`
- `../projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python/src/stage05/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- judge와 scorer가 별도 함수 계약을 가진다.
- failure types는 판단 결과와 최종 score 계산 모두에 반영된다.
- live provider가 없어도 deterministic 테스트가 가능하다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `judge_response`와 `merge_score`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_judge_and_score_merge`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/05-judge-and-score-merge/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`05-judge-and-score-merge-python_answer.md`](05-judge-and-score-merge-python_answer.md)에서 확인한다.
