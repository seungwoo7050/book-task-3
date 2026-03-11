# D-data-api-lab FastAPI

이 문서는 D-data-api-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- projects / tasks / comments CRUD
- filtering / sorting / pagination
- soft delete
- optimistic locking
- `/api/v1/health/live`, `/api/v1/health/ready`

## 빠른 실행

가장 빠른 로컬 확인:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make run
```

Compose 전체 확인:

```bash
cp .env.example .env
docker compose up --build
```

## 검증 명령

```bash
make lint
make test
make smoke
docker compose up --build
```

## 런타임 구성

- `api`: 호스트 `8002` 포트로 노출됩니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `d_data_api_lab`입니다.

## 실행 전에 알아둘 점

- `make run`은 기본 SQLite 설정으로도 바로 뜹니다.
- `.env.example`은 PostgreSQL이 있는 Compose 경로용 값입니다.
- Compose는 데이터 API 실험에 필요한 API와 DB만 포함합니다.
- 인증 없이 데이터 모델과 서비스 경계에 집중하는 워크스페이스입니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
