# 02 도메인 픽스처와 리플레이 하니스

## 이 stage의 문제

fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는지 정리한다.

## 입력/제약

- 입력: seeded KB, sample conversations, replay session fixture
- 제약: database 없이도 deterministic replay가 가능해야 한다.

## 이 stage의 답

- KB loader와 replay harness를 분리해 입력셋 재현 경로를 고정한다.
- 후속 regression과 compare가 같은 fixture 기반에서 동작하게 만든다.

## capstone 연결 증거

- `projects/02-chat-qa-ops/stages/02-domain-fixtures-and-chat-harness/python/src/stage02/harness.py`
- `projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/src/evaluator/replay_harness.py`

## 검증 명령

```bash
cd python
UV_PYTHON=python3.12 uv run pytest -q
```

## 현재 한계

- persistence와 운영 API는 아직 없다.
- fixture 품질 자체를 장기적으로 관리하는 체계는 범위 밖이다.
