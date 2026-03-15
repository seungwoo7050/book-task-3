# 06-golden-set-and-regression-python 문제지

## 왜 중요한가

개선 실험이 실제 품질 향상인지 어떻게 데이터셋과 manifest로 증빙할 것인가?

## 목표

시작 위치의 구현을 완성해 golden case는 required evidence 문서를 명시한다, assertion 실패는 reason code로 설명된다, baseline과 candidate label을 manifest 파일로 고정한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/src/stage06/__init__.py`
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/src/stage06/regression.py`
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/tests/test_regression.py`
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/data/compare_manifest.json`
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/data/golden_cases.json`
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/pyproject.toml`

## starter code / 입력 계약

- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/src/stage06/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- golden case는 required evidence 문서를 명시한다.
- assertion 실패는 reason code로 설명된다.
- baseline과 candidate label을 manifest 파일로 고정한다.

## 제외 범위

- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/data/compare_manifest.json` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `evaluate_case`와 `load_manifest`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_golden_assertion_and_compare_manifest`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python/data/compare_manifest.json` 등 fixture/trace 기준으로 결과를 대조했다.
- `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/06-golden-set-and-regression/python && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`06-golden-set-and-regression-python_answer.md`](06-golden-set-and-regression-python_answer.md)에서 확인한다.
