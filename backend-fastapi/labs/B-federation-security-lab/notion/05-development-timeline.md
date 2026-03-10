# 개발 타임라인

## 이 문서의 목적

- 외부 로그인과 2FA가 섞인 랩을 어떤 순서로 재현해야 덜 헷갈리는지 적는다.
- 실제 Google 계정 없이도 재현 가능한 경로와, Compose에서 shape만 확인하는 경로를 분리한다.

## 1. 시작 위치를 고정한다

```bash
cd labs/B-federation-security-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
```

- `app/core/config.py` 기본값은 SQLite와 빈 Redis를 사용하므로, `.env`가 없어도 앱 자체는 뜬다.
- `.env.example`은 Compose 기준 값과 실제 Google OIDC endpoint를 담고 있다.
- `make run`으로 코드 구조를 빨리 읽고 싶다면 `.env` 없이 시작하고, PostgreSQL + Redis + Alembic까지 포함한 경로를 보고 싶다면 Compose를 쓴다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_google_callback.py tests/integration/test_two_factor.py -q
make smoke
```

- 이 경로가 가장 재현성이 높다. 테스트 안에서 `GoogleOIDCService`를 monkeypatch해서 `google/login`, `google/callback`, 2FA setup, TOTP confirm, recovery code verify까지 외부 의존성 없이 끝까지 확인한다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live`만 확인한다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/auth/google/login
```

- 두 번째 응답의 핵심은 `authorization_url`이 정상 생성되는지다.
- 이 단계에서는 redirect URL 모양, `state` 발급, 쿠키 생성처럼 외부 provider 앞단의 shape만 빠르게 볼 수 있다.

## 4. Compose로 PostgreSQL, Redis, Alembic까지 같이 올린다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- `api` 컨테이너는 시작할 때 `alembic upgrade head`를 먼저 수행한다.
- `db`와 `redis`가 모두 healthy 상태인지 확인한 뒤에 로그인 흐름을 본다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 완전 재현은 테스트를 기준으로 본다

이 랩에서 완전 재현의 기준은 수동 브라우저 클릭보다 아래 순서의 테스트다.

1. `GET /api/v1/auth/google/login`으로 `authorization_url`과 `state`를 만든다.
2. monkeypatch된 provider를 통해 `GET /api/v1/auth/google/callback?code=sample-code&state=<state>`를 호출한다.
3. `GET /api/v1/auth/me`로 세션이 살아 있는지 확인한다.
4. `POST /api/v1/auth/2fa/setup`으로 secret을 발급받는다.
5. `POST /api/v1/auth/2fa/confirm`으로 TOTP를 등록하고 recovery code 8개를 받는다.
6. 다시 Google 로그인 후 `POST /api/v1/auth/2fa/verify`로 recovery code를 제출해 최종 인증을 완료한다.

## 6. 실제 Google 자격 증명으로 보고 싶을 때

- `.env`의 `GOOGLE_OIDC_CLIENT_ID`, `GOOGLE_OIDC_CLIENT_SECRET`, redirect URI를 실제 값으로 교체한다.
- Google Console에 `http://localhost:8000/api/v1/auth/google/callback`을 등록한다.
- 이후에는 아래 흐름으로 본다.

```bash
curl -c cookies.txt http://127.0.0.1:8000/api/v1/auth/google/login
```

- 브라우저에서 `authorization_url`로 이동해 callback을 완료한다.
- callback 뒤 `cookies.txt`에 세션 쿠키가 생기면 2FA를 이어서 확인한다.

```bash
csrf=$(grep csrf_token cookies.txt | tail -n 1 | awk '{print $7}')

curl -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:8000/api/v1/auth/2fa/setup \
  -H "X-CSRF-Token: ${csrf}"
```

- 위 응답의 `secret`으로 TOTP 코드를 만든다.

```bash
python -c 'import pyotp; print(pyotp.TOTP("<SECRET>").now())'
```

- 생성된 코드로 confirm을 호출하고, 응답의 recovery code를 저장한다.

## 7. 막히면 먼저 확인할 것

- callback이 막히면 먼저 `state` 쿠키와 query string의 `state`가 일치하는지 확인한다.
- 두 번째 로그인 뒤 `/api/v1/auth/me`가 `401`이면 2FA pending 상태일 가능성이 크다. 이 경우 `2fa/verify`를 먼저 마쳐야 한다.
- 수동 브라우저 경로가 불안정하면 다시 테스트 경로로 돌아가는 것이 가장 빠르다.
