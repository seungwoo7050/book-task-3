# 00-source-brief-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다, reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다, 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다를 한 흐름으로 설명하고 검증한다. 핵심은 `SourceBrief`와 `build_source_brief` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 주제, capstone goal, baseline version, primary stack이 코드 객체 하나에 정리된다.
- reference spine이 임의 서술이 아니라 테스트 가능한 상수로 유지된다.
- 후속 stage가 이 brief를 설계 기준으로 재사용할 수 있다.
- 첫 진입점은 `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`이고, 여기서 `SourceBrief`와 `build_source_brief` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/source_brief.py`: `SourceBrief`, `build_source_brief`가 핵심 흐름과 상태 전이를 묶는다.
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/conftest.py`: pytest fixture와 테스트 환경 구성을 고정하는 파일이다.
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/test_source_brief.py`: `test_source_brief_contract`가 통과 조건과 회귀 포인트를 잠근다.
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/pyproject.toml`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `SourceBrief` 구현은 `test_source_brief_contract`이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/pyproject.toml`는 실행 루트와 모듈 경계를 고정해 검증이 어느 위치에서 돌아야 하는지 알려 준다.

## 정답을 재구성하는 절차

1. `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_source_brief_contract`이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_source_brief_contract`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/__init__.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/src/stage00/source_brief.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/conftest.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/tests/test_source_brief.py`
- `../projects/02-chat-qa-ops/stages/00-source-brief/python/pyproject.toml`
