# Python 구현 안내

FastAPI snapshot server로 overview, failures, session review, golden run, version compare contract를 독립 검증한다. 대시보드가 읽을 응답 형태를 학습용으로 고정한 백엔드 pack이다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. 주요 dashboard endpoint가 FastAPI test client로 확인된다.
- 남은 범위: 지속 저장소나 실시간 잡 처리까지 포함한 운영 백엔드는 아니다.

## 먼저 볼 파일

- `src/stage07/app.py`
- `tests/test_api.py`
