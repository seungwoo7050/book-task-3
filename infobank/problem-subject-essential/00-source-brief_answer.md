# 00-source-brief 답안지

이 문서는 umbrella 답안지다. 실제 해답은 runtime별 답안지로 분리했고, 여기서는 어떤 runtime 답안지를 읽어야 막히지 않는지만 정리한다.

## 이 umbrella의 역할

- 같은 개념을 여러 runtime 구현으로 섞어 읽지 않게 진입 순서를 고정한다.
- 실제 코드 워크스루, 검증 명령, 실패 포인트는 아래 runtime 답안지에서 직접 확인한다.

## 문제를 푸는 핵심 전략

- 지금 구현하려는 runtime 하나만 선택한다.
- 선택한 runtime의 문제지로 입력 계약을 고정한 뒤 같은 이름의 `_answer.md`로 내려간다.
- 여러 runtime을 동시에 참고하지 않고 하나를 끝까지 닫은 뒤 필요하면 다른 runtime을 비교한다.

## 정답을 재구성하는 절차

1. 아래 runtime 답안지 중 현재 구현할 대상 하나를 고른다.
2. 해당 runtime 답안지의 코드 워크스루와 검증 명령만 따라가며 해답을 재구성한다.
3. 다른 runtime이 필요해질 때만 비교용으로 다시 올라온다.

## 런타임별 답안지

- `python`: [`00-source-brief-python`](00-source-brief-python_answer.md)

## 읽는 순서

- 지금 구현하려는 runtime 하나만 고른다.
- 고른 runtime의 문제지에서 입력 계약을 확인한 뒤, 같은 이름의 `_answer.md`로 바로 내려간다.

## 소스 근거

- `python` 해설 진입점: [`00-source-brief-python`](00-source-brief-python_answer.md)
- `python` 실제 source/test 근거: `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`, `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/source_brief.py`, `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/conftest.py`, `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/test_source_brief.py`
