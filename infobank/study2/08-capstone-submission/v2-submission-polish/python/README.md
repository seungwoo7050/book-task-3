# Python Implementation

이 디렉터리는 Chat QA Ops의 백엔드와 테스트 하네스를 담는다.

## Scope

- FastAPI API
- CLI
- evaluation pipeline
- `retrieval-v1` / `retrieval-v2` 버전 스위치
- alias/category/risk 기반 retrieval rerank
- retrieval-conditioned answer composer
- pytest 회귀셋
- compare artifact 생성용 CLI/API contract 유지

## Commands

```bash
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
UV_PYTHON=python3.12 make smoke-postgres
```

프론트엔드 관련 명령도 이 Makefile에서 `../react`를 대상으로 연결된다.
