# 00-source-brief-python 문제지

## 왜 중요한가

이 트랙이 무엇을 만들고 어떤 sequence와 stack을 따르는지 코드를 통해 어떻게 고정할 것인가?

## 목표

시작 위치의 구현을 완성해 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다, reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다, 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/source_brief.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/test_source_brief.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.
- reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.
- 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `SourceBrief`와 `build_source_brief`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_source_brief_contract`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`00-source-brief-python_answer.md`](00-source-brief-python_answer.md)에서 확인한다.
