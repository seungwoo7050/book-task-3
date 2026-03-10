# 개발 타임라인

## 이 문서의 목적

- A~G 랩에서 배운 것을 이 capstone에서 어떤 순서로 다시 묶어야 하는지 재현 가능한 흐름으로 적는다.
- 가장 확실한 통합 재현은 자동 테스트라는 점을 분명히 하고, Compose 기반 shape 확인은 보조 경로로 둔다.

## 1. 시작 위치를 고정한다

```bash
cd capstone/workspace-backend/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
```

- `app/core/config.py` 기본값은 SQLite와 빈 Redis를 사용하므로 `.env` 없이도 로컬 서버는 뜬다.
- `.env.example`을 복사하면 PostgreSQL + Redis Compose 경로로 전환된다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_capstone.py -q
make smoke
```

- 이 테스트 하나가 local auth, 이메일 검증, Google 스타일 로그인, workspace invite, project/task/comment API, notification drain, websocket 수신까지 끝까지 이어 준다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live`만 확인한다.
- 이 capstone의 완전 재현 기준은 수동 클릭이 아니라 위 테스트다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- 로컬 루프는 도메인 경계를 읽거나 route shape를 빠르게 확인할 때 유용하다.
- 다만 owner의 이메일 검증 토큰은 테스트에서 `app.state.mailbox`로 꺼내기 때문에, 브라우저만으로 완전한 엔드투엔드 재현을 하기는 어렵다.

## 4. Compose로 통합 shape를 확인한다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8010/api/v1/health/live
curl http://127.0.0.1:8010/api/v1/health/ready
```

- Compose에서는 API가 `8010`, PostgreSQL이 `5440`, Redis가 `6390` 포트로 노출된다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 통합 재현의 기준 시나리오

`tests/integration/test_capstone.py`를 읽을 때 순서를 아래처럼 따라가면 된다.

1. owner가 `/api/v1/auth/register`로 가입한다.
2. 테스트 helper가 mailbox에서 검증 토큰을 꺼내 `/api/v1/auth/verify-email`을 호출한다.
3. owner가 `/api/v1/auth/login`으로 로그인한다.
4. collaborator가 `/api/v1/auth/google/login`으로 즉시 세션을 만든다.
5. owner가 `/api/v1/platform/workspaces`와 `/invites`를 만들고, collaborator가 invite를 수락한다.
6. collaborator가 `/api/v1/platform/ws/notifications?access_token=<token>`에 WebSocket으로 붙는다.
7. owner가 project, task, comment를 만들고 `/api/v1/platform/notifications/drain`을 호출한다.
8. collaborator socket이 `New comment on task`로 시작하는 메시지를 받으면 통합이 끝까지 이어진 것이다.

## 6. 수동으로 확인할 수 있는 부분만 따로 본다

Google 스타일 로그인 shape는 수동으로도 바로 볼 수 있다.

```bash
curl -c collaborator.cookies -b collaborator.cookies -X POST http://127.0.0.1:8000/api/v1/auth/google/login \
  -H 'Content-Type: application/json' \
  -d '{"subject":"google-123","email":"collab@example.com","display_name":"Collab"}'
```

- 위 요청 뒤 `collaborator.cookies`에 `access_token`이 생긴다.
- 이 세션은 workspace 초대 수락이나 `/api/v1/auth/me` 확인에 바로 쓸 수 있다.

반면 owner의 local auth 전체 흐름은 검증 토큰이 외부 UI로 노출되지 않으므로 테스트 경로가 기준이다.

## 7. 막히면 먼저 확인할 것

- capstone에서 가장 흔한 문제는 기능 하나가 아니라 경계 합치기 순서가 어긋나는 것이다.
- websocket만 안 되면 auth보다 먼저 `access_token` 전달 방식과 `/notifications/drain` 호출 여부를 확인한다.
- owner 검증 흐름이 재현되지 않으면 테스트를 먼저 돌리고, 그 다음에 route shape를 수동으로 보는 편이 빠르다.
