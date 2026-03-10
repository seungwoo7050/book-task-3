# 개발 타임라인

## 이 문서의 목적

- 이 랩을 다시 볼 때 권한표와 HTTP 흐름을 한 번에 재현할 수 있게 순서를 고정한다.
- 자동 테스트 경로와 수동 API 확인 경로를 함께 적어, “권한이 정말 이렇게 막히는가”를 바로 확인하게 만든다.

## 1. 시작 위치를 고정한다

```bash
cd labs/C-authorization-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
```

- `app/core/config.py` 기본값은 SQLite를 사용하므로 `.env` 없이도 로컬 편집 루프를 열 수 있다.
- `.env.example`을 복사하면 PostgreSQL이 있는 Compose 경로로 전환된다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_authorization_flows.py -q
make smoke
```

- 위 테스트는 owner, viewer, outsider를 만들고, workspace 생성, invite accept, 문서 생성 차단, 역할 승격, decline, outsider read 금지까지 확인한다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live`만 확인한다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- 이 모드에서는 DB가 `c_authorization_lab.db`로 만들어진다.
- 역할 비교 로직과 서비스 계층 흐름을 빠르게 손볼 때 가장 편하다.

## 4. Compose로 PostgreSQL 경로까지 확인한다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8001/api/v1/health/live
curl http://127.0.0.1:8001/api/v1/health/ready
```

- Compose에서는 API가 `8001`, PostgreSQL이 `5433` 포트로 노출된다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 수동 권한 흐름을 재현한다

먼저 사용자 두 명을 만든다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authorization/users \
  -H 'Content-Type: application/json' \
  -d '{"email":"owner@example.com","name":"Owner"}'

curl -X POST http://127.0.0.1:8000/api/v1/authorization/users \
  -H 'Content-Type: application/json' \
  -d '{"email":"viewer@example.com","name":"Viewer"}'
```

- 응답에서 `owner_id`, `viewer_id`를 복사해 다음 명령에 넣는다.

워크스페이스를 만들고 viewer를 초대한다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authorization/workspaces \
  -H 'Content-Type: application/json' \
  -H 'X-User-Id: <OWNER_ID>' \
  -d '{"name":"Platform"}'

curl -X POST http://127.0.0.1:8000/api/v1/authorization/workspaces/<WORKSPACE_ID>/invites \
  -H 'Content-Type: application/json' \
  -H 'X-User-Id: <OWNER_ID>' \
  -d '{"email":"viewer@example.com","role":"viewer"}'
```

- 응답에서 `workspace_id`, `invite_token`을 복사한다.

viewer가 초대를 수락한 뒤, 문서 생성이 막히는지 본다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/authorization/invites/<INVITE_TOKEN>/accept \
  -H 'X-User-Id: <VIEWER_ID>'

curl -X POST http://127.0.0.1:8000/api/v1/authorization/workspaces/<WORKSPACE_ID>/documents \
  -H 'Content-Type: application/json' \
  -H 'X-User-Id: <VIEWER_ID>' \
  -d '{"title":"Spec"}'
```

- 두 번째 응답은 `403`이어야 정상이다.

owner가 viewer를 member로 승격한 뒤 다시 문서를 만든다.

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/authorization/workspaces/<WORKSPACE_ID>/members/<VIEWER_ID> \
  -H 'Content-Type: application/json' \
  -H 'X-User-Id: <OWNER_ID>' \
  -d '{"role":"member"}'

curl -X POST http://127.0.0.1:8000/api/v1/authorization/workspaces/<WORKSPACE_ID>/documents \
  -H 'Content-Type: application/json' \
  -H 'X-User-Id: <VIEWER_ID>' \
  -d '{"title":"Spec"}'
```

- 마지막 응답은 `200`이어야 한다.

## 6. 막히면 먼저 확인할 것

- 거의 모든 차단은 `X-User-Id` 누락이나 잘못된 actor 선택에서 나온다.
- viewer가 바로 문서를 만들 수 있으면 역할 비교 순서가 깨졌을 가능성이 높다.
- invite 관련 흐름이 이상하면 accept와 decline이 같은 토큰 상태를 어떻게 바꾸는지 테스트를 다시 보는 편이 빠르다.
