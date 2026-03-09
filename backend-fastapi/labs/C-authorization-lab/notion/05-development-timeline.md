# Development Timeline

## Phase 1: 프로젝트 초기 세팅

포트 충돌을 피하기 위해 A(8000), B(8000)와 다른 포트를 사용한다. 이 랩은 외부 API 포트 8001, PostgreSQL 5433.

```bash
mkdir -p labs/C-authorization-lab/fastapi
cd labs/C-authorization-lab/fastapi

# pyproject.toml 작성 후 설치
python3 -m pip install -e ".[dev]"
```

이 랩의 의존성은 A/B보다 가볍다. `pyotp`, `itsdangerous`, `PyJWT[crypto]`가 없다—인증 관련 기능을 완전히 생략했기 때문이다. 핵심 의존성: FastAPI, SQLAlchemy, Alembic, psycopg, uvicorn, pydantic-settings.

패키지 구조:
```
app/
  api/
    v1/routes/
      authorization.py
      health.py
    deps.py
  core/
    config.py, errors.py, logging.py
  db/
    models/authorization.py
    base.py, session.py
  domain/services/
    authorization.py
  repositories/
    authorization_repository.py
  schemas/
    authorization.py, common.py
  bootstrap.py
  main.py
```

## Phase 2: 데이터 모델 설계

5개 테이블: users, workspaces, memberships, invites, documents.

핵심 설계 결정:
- User는 email과 name만. 인증 필드가 없다.
- Workspace의 `owner_user_id`는 FK로 소유자 참조.
- Membership에 `(user_id, workspace_id)` 유니크 제약.
- Invite에 unique token (secrets.token_urlsafe(18)) + status (pending/accepted/declined).
- Document에 `owner_user_id`와 `workspace_id` 두 FK.

## Phase 3: Authorization Service 핵심 로직

ROLE_ORDER 딕셔너리로 역할 서열을 정의:
```python
ROLE_ORDER = {"viewer": 1, "member": 2, "admin": 3, "owner": 4}
```

`_require_role` 메서드: membership 조회 후 역할 수준 비교. 미달이면 403.

주요 서비스 메서드:
- `create_workspace`: Workspace + owner Membership을 한 트랜잭션으로 생성
- `create_invite`: admin 이상만 호출 가능, pending Invite 생성
- `accept_invite`: email 일치 확인 → Membership 생성 → status="accepted"
- `decline_invite`: email 일치 확인 → status="declined"
- `change_role`: owner만 가능, 이중 검증
- `create_document`: member 이상만 가능
- `get_document`: viewer 이상만 가능

## Phase 4: API 라우트와 Header-Based Actor

`deps.py`에 actor 주입 dependency:
```python
def get_actor_id(x_user_id: Annotated[str, Header(alias="X-User-Id")]) -> str:
    return x_user_id
```

엔드포인트:
- `POST /api/v1/authorization/users` — 사용자 생성 (actor 불필요)
- `POST /api/v1/authorization/workspaces` — workspace 생성 (actor 필요)
- `POST /api/v1/authorization/workspaces/{id}/invites` — 초대 발행 (admin+)
- `POST /api/v1/authorization/invites/{token}/accept` — 초대 수락
- `POST /api/v1/authorization/invites/{token}/decline` — 초대 거절
- `PATCH /api/v1/authorization/workspaces/{id}/members/{user_id}` — 역할 변경 (owner)
- `POST /api/v1/authorization/workspaces/{id}/documents` — 문서 생성 (member+)
- `GET /api/v1/authorization/documents/{id}` — 문서 읽기 (viewer+)

## Phase 5: Bootstrap과 Schema 자동 생성

```python
# app/bootstrap.py
def initialize_schema() -> None:
    Base.metadata.create_all(bind=get_engine())
```

main.py startup에서 호출되어 SQLite/PostgreSQL 모두에서 테이블 자동 생성.

## Phase 6: Docker Compose 구성

```yaml
# compose.yaml
services:
  api:    # port 8001:8000, uvicorn reload
  db:     # PostgreSQL 16, POSTGRES_DB=c_authorization_lab, port 5433:5432
```

Redis가 없다—이 랩에는 rate limiting이나 세션 저장이 필요 없기 때문.

```bash
docker compose up --build -d
docker compose ps
curl -s http://localhost:8001/api/v1/health/live
```

## Phase 7: Alembic 마이그레이션

```bash
alembic init alembic
# alembic.ini와 env.py 설정

alembic revision -m "initial authorization schema"
alembic upgrade head
```

5개 테이블 생성: users, workspaces, memberships, invites, documents.

```bash
# PostgreSQL에서 확인
docker compose exec db psql -U postgres -d c_authorization_lab -c "\dt"
```

## Phase 8: 테스트 작성

conftest: SQLite tmp_path 기반, 테스트마다 스키마 재생성.

두 개의 통합 테스트:

1. **invite-accept-promote-document**: owner 생성 → workspace 생성 → viewer 초대 → viewer가 accept → viewer가 문서 생성 시도 (403) → owner가 viewer를 member로 승격 → 문서 생성 성공 (200)

2. **invite-decline-outsider-forbidden**: owner 생성 → workspace + document 생성 → invitee 초대 → invitee가 decline → outsider가 document 읽기 시도 (403)

```bash
make test    # pytest
make lint    # ruff check
make smoke   # smoke test
```

## Phase 9: 최종 검증

```bash
# 전체 검증 순서
make install
make lint
make test
make smoke

# Compose 검증
docker compose up --build -d
curl -sf http://localhost:8001/api/v1/health/live
docker compose down
```
