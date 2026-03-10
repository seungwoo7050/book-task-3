# 툴체인과 검증 기준

## 필수 런타임

- Python `3.13+`
- Docker Compose
- Terraform `1.5.x`

## 주요 Python 라이브러리

- FastAPI
- Typer
- Pydantic
- SQLAlchemy
- psycopg
- DuckDB
- PyYAML
- pytest
- ruff
- mypy

## 레포 루트 기준 기본 명령

```bash
make venv
make doctor
make test-unit
make test-integration
make test-capstone
make test-all
make demo-capstone
```

## 각 명령이 확인하는 것

- `make venv`: `.venv`를 만들고 `pyproject.toml` 기준 의존성을 설치합니다.
- `make doctor`: Python, Docker, Terraform이 모두 준비됐는지 확인합니다.
- `make test-unit`: foundations와 core의 개별 Python 프로젝트 테스트를 돌립니다.
- `make test-integration`: Terraform 실습 프로젝트의 검증 테스트를 돌립니다.
- `make test-capstone`: 캡스톤의 API, worker, DB 흐름 테스트를 돌립니다.
- `make demo-capstone`: 데모용 산출물을 `.artifacts/capstone/` 아래에 생성합니다.

## 로컬 상태 저장소

- PostgreSQL: 캡스톤 상태 저장소의 기본 경로
- SQLite: `make demo-capstone`의 fallback 경로
- DuckDB + Parquet: 로그 적재와 질의용 로컬 lake

## 자주 막히는 지점

- `python3 --version`이 3.13 미만이면 `make venv`가 실패합니다.
- Docker daemon이 꺼져 있으면 `make doctor`와 `make demo-capstone`의 PostgreSQL 경로가 실패합니다.
- Terraform이 없으면 `make doctor`와 Terraform 실습 재현이 실패합니다.
- `.venv`가 다른 인터프리터로 만들어졌다면 삭제 후 다시 생성하는 편이 빠릅니다.

## 문서와 검증의 관계

문서는 코드보다 앞서지 않습니다. README에 적는 명령은 반드시 현재 Makefile과 파일 경로에서 실제로 찾을 수
있는 값만 적고, 환경 의존성이 있는 경우에는 실패 조건까지 함께 설명합니다.
