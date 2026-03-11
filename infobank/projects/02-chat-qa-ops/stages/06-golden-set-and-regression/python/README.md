# Python 구현 안내

golden case와 compare manifest를 작은 데이터 파일로 분리해 regression proof의 최소 단위를 만든다. 사람이 diff로 검토할 수 있는 증빙 구조를 우선한다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. golden assertion과 compare manifest 로딩이 pytest로 고정되어 있다.
- 남은 범위: full capstone report UI나 장기 보관용 리포트 렌더링은 포함하지 않는다.

## 먼저 볼 파일

- `data/golden_cases.json`
- `data/compare_manifest.json`
- `src/stage06/regression.py`
- `tests/test_regression.py`
