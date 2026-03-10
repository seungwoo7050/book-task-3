# 개발 타임라인

## 이 문서의 목적

- CRUD 랩을 다시 따라갈 때 엔터티 생성보다 규칙 검증 순서를 먼저 고정한다.
- 필터링, 정렬, soft delete, optimistic locking을 어떻게 재현하면 되는지 실제 요청 기준으로 적는다.

## 1. 시작 위치를 고정한다

```bash
cd labs/D-data-api-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
```

- 기본 설정은 SQLite를 쓰므로 `.env` 없이도 로컬 루프가 돈다.
- `.env.example`을 복사하면 Compose의 PostgreSQL 경로로 전환된다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_data_api.py -q
make smoke
```

- 위 테스트는 필터링, 정렬, pagination, soft delete, `include_deleted`, optimistic locking, task/comment 생성까지 한 번에 본다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live` 응답만 확인한다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- 규칙 수정과 응답 shape 확인은 이 경로가 가장 빠르다.
- SQLite 파일은 작업 디렉터리에 `d_data_api_lab.db`로 생긴다.

## 4. Compose로 PostgreSQL 경로까지 확인한다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8002/api/v1/health/live
curl http://127.0.0.1:8002/api/v1/health/ready
```

- Compose에서는 API가 `8002`, PostgreSQL이 `5434` 포트로 노출된다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 수동 데이터 흐름을 재현한다

프로젝트 세 개를 만든다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/data/projects \
  -H 'Content-Type: application/json' \
  -d '{"title":"Alpha","status":"active"}'

curl -X POST http://127.0.0.1:8000/api/v1/data/projects \
  -H 'Content-Type: application/json' \
  -d '{"title":"Gamma","status":"archived"}'

curl -X POST http://127.0.0.1:8000/api/v1/data/projects \
  -H 'Content-Type: application/json' \
  -d '{"title":"Beta","status":"active"}'
```

active 프로젝트만 제목 순으로 한 페이지씩 본다.

```bash
curl "http://127.0.0.1:8000/api/v1/data/projects?status=active&sort=title&page=1&page_size=1"
```

- 응답의 첫 항목 제목이 `Alpha`인지 본다.

soft delete와 `include_deleted`를 본다.

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/data/projects/<BETA_ID>

curl "http://127.0.0.1:8000/api/v1/data/projects?status=active"
curl "http://127.0.0.1:8000/api/v1/data/projects?include_deleted=true&sort=-title"
```

- 첫 번째 조회에서는 `Beta`가 빠져야 하고, 두 번째 조회에서는 `Alpha`, `Beta`, `Gamma`가 모두 보여야 한다.

optimistic locking과 하위 리소스 생성을 본다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/data/projects \
  -H 'Content-Type: application/json' \
  -d '{"title":"Roadmap","status":"active"}'
```

- 응답에서 `project_id`와 `version`을 복사한다.

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/data/projects/<PROJECT_ID> \
  -H 'Content-Type: application/json' \
  -d '{"version":1,"title":"Roadmap v2"}'

curl -X PATCH http://127.0.0.1:8000/api/v1/data/projects/<PROJECT_ID> \
  -H 'Content-Type: application/json' \
  -d '{"version":1,"status":"archived"}'
```

- 두 번째 PATCH는 `409`가 나와야 정상이다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/data/projects/<PROJECT_ID>/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Ship API","status":"todo","priority":1}'

curl -X POST http://127.0.0.1:8000/api/v1/data/tasks/<TASK_ID>/comments \
  -H 'Content-Type: application/json' \
  -d '{"body":"Need pagination semantics in the README."}'
```

## 6. 막히면 먼저 확인할 것

- soft delete가 안 보이면 기본 조회가 `deleted_at is null` 조건을 정말 적용하는지 본다.
- stale update가 `409` 대신 `200`이면 version 비교가 서비스 계층에서 빠졌을 가능성이 크다.
- task/comment 생성보다 먼저 project version 충돌을 잡는 편이 디버깅이 훨씬 쉽다.
