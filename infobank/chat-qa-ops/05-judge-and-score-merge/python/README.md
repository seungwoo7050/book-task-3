# Python 구현 안내

judge가 반환하는 판단 값과 최종 weighted score를 분리해 검증한다. 후속 stage에서 judge 구현을 바꿔도 점수 계약은 유지된다는 점을 보여준다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. heuristic judge와 score merge가 하나의 테스트로 고정되어 있다.
- 남은 범위: live provider나 프롬프트 기반 judge는 포함하지 않는다.

## 먼저 볼 파일

- `src/stage05/judge.py`
- `tests/test_judge.py`
