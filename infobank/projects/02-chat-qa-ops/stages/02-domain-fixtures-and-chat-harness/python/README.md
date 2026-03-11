# Python 구현 안내

seeded knowledge base, replay fixture, deterministic harness를 분리해 회귀 입력을 재현한다. 사람이 읽을 수 있는 데이터 파일을 그대로 테스트에 사용한다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. fixture 로딩과 예상 evidence 문서 재현이 pytest로 확인된다.
- 남은 범위: 실제 DB persistence나 vector store는 연결하지 않는다.

## 먼저 볼 파일

- `data/replay_sessions.json`
- `src/stage02/harness.py`
- `tests/test_harness.py`
