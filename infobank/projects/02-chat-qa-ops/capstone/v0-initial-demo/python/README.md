# Python 구현 안내

이 디렉터리는 Chat QA Ops의 백엔드와 테스트 하네스를 담는다.

## 범위

- FastAPI API
- CLI
- evaluation pipeline
- `SQLite` 기반 데이터 저장
- pytest 회귀셋
- seeded KB + replay harness
- dependency health / preflight contract

## 실행 명령

```bash
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make replay
UV_PYTHON=python3.12 make gate-all
```

프론트엔드 관련 명령도 이 Makefile에서 `../react`를 대상으로 연결된다.
