# Toolchain

## Runtime

- Python 3.13+
- Docker Compose
- Terraform 1.5.x

## Python Libraries

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

## Local State

- PostgreSQL: control plane state DB
- DuckDB + Parquet: security lake style log store

## Default Verification

```bash
make doctor
make test-all
make demo-capstone
```

AWS 계정은 필수 전제가 아니다. v1은 로컬 fixture와 Terraform plan JSON을 기준으로 검증한다.
`make demo-capstone`은 Docker daemon이 있으면 PostgreSQL을 사용하고, 없으면 SQLite fallback으로
동일한 demo 산출물을 만든다.
