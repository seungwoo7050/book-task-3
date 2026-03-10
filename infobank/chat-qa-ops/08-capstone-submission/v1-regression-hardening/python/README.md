# Python 구현 안내

이 디렉터리는 Chat QA Ops의 백엔드와 테스트 하네스를 담는다.

## 범위

- FastAPI API
- CLI
- evaluation pipeline
- Upstage/OpenAI/Ollama provider chain
- run lineage, retrieval trace, claim trace, judge trace
- `PostgreSQL` 우선 smoke path + `SQLite` fallback
- pytest 회귀셋
- Langfuse no-op/prepared envelope

## 실행 명령

```bash
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
UV_PYTHON=python3.12 make smoke-postgres
```

프론트엔드 관련 명령도 이 Makefile에서 `../react`를 대상으로 연결된다.
