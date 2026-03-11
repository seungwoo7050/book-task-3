# Python 구현 안내

source brief를 코드 객체와 테스트로 고정한다. 이후 stage가 같은 baseline, 같은 reference spine을 읽도록 만드는 것이 목적이다.

## 실행 및 검증

- 의존성 설치: `UV_PYTHON=python3.12 uv sync`
- 테스트: `UV_PYTHON=python3.12 uv run pytest -q`

## 현재 상태

- 상태: 검증 완료. baseline version과 primary stack contract가 pytest로 고정되어 있다.
- 남은 범위: 런타임 기능은 없다. 설계 기준과 문서 계약을 다루는 단계다.

## 먼저 볼 파일

- `src/stage00/source_brief.py`
- `tests/test_source_brief.py`
