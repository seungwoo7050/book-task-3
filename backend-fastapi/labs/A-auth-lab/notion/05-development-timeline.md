# 개발 타임라인

## 이 문서의 목적

- 처음 체크아웃한 사람이 어디서부터 시작하면 이 랩을 다시 성공 상태까지 가져갈 수 있는지 적는다.
- 빠른 자동 검증 경로와 Mailpit까지 포함한 수동 HTTP 확인 경로를 분리해 적는다.

## 1. 시작 위치를 고정한다

```bash
cd labs/A-auth-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
```

- `app/core/config.py` 기본값만 쓰면 SQLite와 빈 Redis로도 앱이 뜬다.
- `.env.example`을 `.env`로 복사하면 `db`, `redis`, `mailpit` 같은 Compose 서비스 호스트를 쓰게 된다.
- 그래서 `make run`만 빠르게 확인하고 싶다면 `.env`를 만들지 않거나, 이미 만들었다면 값을 로컬용으로 바꾼 뒤 실행한다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_local_auth.py -q
make smoke
```

- 첫 번째 명령은 회원가입, 이메일 검증, 로그인, `refresh token rotation`, 로그아웃, 비밀번호 재설정, CSRF 실패 경로를 한 번에 검증한다.
- `make smoke`는 임시 SQLite 파일로 앱 부팅과 `/api/v1/health/live` 응답만 확인한다.
- 코드를 읽기 전에 현재 기능 범위를 가장 빨리 확인하는 방법은 이 두 명령이다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- 로컬 기본 설정을 쓰면 DB는 `a_auth_lab.db`로 만들어지고 Redis는 비활성이다.
- 이 경로는 인증 코드 구조를 빠르게 수정하면서 확인할 때 적합하다.
- 메일 토큰까지 실제로 확인하려면 다음 단계의 Compose 경로가 더 낫다.

## 4. Compose로 전체 의존성을 띄운다

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/health/ready
```

- `api`, `db`, `redis`, `mailpit` 네 서비스가 모두 떠야 한다.
- Mailpit UI는 `http://127.0.0.1:8025`에서 확인한다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 수동 HTTP 흐름을 재현한다

회원가입:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"handle":"player-one","email":"player@example.com","password":"super-secret-1"}'
```

이메일 검증:

- Mailpit UI에서 `verify_email` 메일에 들어 있는 토큰을 복사한다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/verify-email \
  -H 'Content-Type: application/json' \
  -d '{"token":"<VERIFY_TOKEN>"}'
```

로그인과 세션 확인:

```bash
curl -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"player@example.com","password":"super-secret-1"}'

curl -b cookies.txt http://127.0.0.1:8000/api/v1/auth/me
```

refresh token rotation:

```bash
csrf=$(grep csrf_token cookies.txt | tail -n 1 | awk '{print $7}')

curl -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:8000/api/v1/auth/token/refresh \
  -H "X-CSRF-Token: ${csrf}"
```

로그아웃:

```bash
csrf=$(grep csrf_token cookies.txt | tail -n 1 | awk '{print $7}')

curl -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:8000/api/v1/auth/logout \
  -H "X-CSRF-Token: ${csrf}"
```

비밀번호 재설정:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/password-reset/request \
  -H 'Content-Type: application/json' \
  -d '{"email":"player@example.com"}'
```

- Mailpit UI에서 `password_reset` 메일 토큰을 확인한 뒤 아래 명령을 실행한다.

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/password-reset/confirm \
  -H 'Content-Type: application/json' \
  -d '{"token":"<RESET_TOKEN>","new_password":"even-better-secret-2"}'
```

## 6. 막히면 먼저 확인할 것

- 이메일 검증 전에 `/api/v1/auth/login`이 `401`이면 정상이다.
- `token/refresh`나 `logout`에서 `403`이 나오면 먼저 `X-CSRF-Token` 헤더와 `cookies.txt`의 `csrf_token` 값을 다시 맞춘다.
- Mailpit이 비어 있으면 Compose 경로로 실행했는지, `.env`에 `MAILPIT_BASE_URL`이 남아 있는지 먼저 본다.
