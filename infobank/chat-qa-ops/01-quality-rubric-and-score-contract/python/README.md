# Python 구현 안내

점수 계산 규칙을 judge 구현과 분리해 고정한다. critical override와 grade band가 흔들리지 않게 만드는 작은 구현이다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. weight 총합, critical override, grade band contract가 테스트로 고정되어 있다.
- 남은 범위: 실시간 evaluator나 LLM judge 연결은 이 pack에 포함하지 않는다.

## 먼저 볼 파일

- `src/stage01/rubric.py`
- `tests/test_rubric.py`
