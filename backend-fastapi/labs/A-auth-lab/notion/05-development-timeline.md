# Development Timeline

## Phase 1: 프로젝트 초기 세팅

### 환경 준비

가장 먼저 프로젝트 디렉터리를 만들고 Python 가상 환경을 구성했다.

```bash
mkdir -p labs/A-auth-lab/fastapi
cd labs/A-auth-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
```

`pyproject.toml`을 작성하면서 핵심 의존성을 결정했다. FastAPI를 웹 프레임워크로, SQLAlchemy 2.0을 ORM으로, Alembic을 마이그레이션 도구로, `argon2-cffi`를 비밀번호 해시 라이브러리로, PyJWT를 토큰 처리용으로, `pydantic-settings`를 설정 관리용으로 골랐다. 개발 의존성으로는 pytest와 ruff를 넣었다.

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

### .env와 설정 클래스

`.env.example` 파일을 만들어서 필요한 환경 변수 목록을 정리했다. `app/core/config.py`에 `Settings` 클래스를 작성해서 `pydantic-settings`의 `BaseSettings`를 상속하게 했다. `DATABASE_URL`, `SECRET_KEY`, `TOKEN_ISSUER`, `REDIS_URL` 등의 변수를 여기서 관리한다.

### Makefile

반복되는 명령을 `Makefile`에 정리했다:

- `make install`: pip 업데이트 + editable install
- `make run`: `uvicorn app.main:app --reload`
- `make lint`: `ruff check app tests`
- `make test`: `pytest`
- `make smoke`: `python -m tests.smoke`

## Phase 2: 데이터 모델과 저장소 계층

### SQLAlchemy 모델 설계

`app/db/base.py`에 SQLAlchemy의 `DeclarativeBase`를 정의하고, naming convention을 일괄 적용했다. `TimestampMixin`을 만들어 `created_at`과 `updated_at`을 자동으로 다루게 했다.

`app/db/models/user.py`에 `User` 모델을 작성했다. 핵심 컬럼은 `id` (UUID), `handle` (고유 닉네임), `email` (고유), `password_hash`, `is_active`, `email_verified_at`이다.

`app/db/models/auth.py`에는 세 개의 모델을 넣었다:
- `RefreshToken`: 발행된 refresh token의 해시, family_id, 만료/폐기/재사용 감지 시각
- `EmailToken`: 이메일 검증과 비밀번호 재설정 토큰
- `AuthAuditLog`: 인증 관련 이벤트 감사 기록

### 세션 관리

`app/db/session.py`에서 SQLAlchemy 엔진과 세션 팩토리를 구성했다. SQLite를 쓸 때는 `check_same_thread=False`를 적용하는 분기를 넣었다. `get_db()` 제너레이터를 만들어 FastAPI의 `Depends`로 주입할 수 있게 했다.

### Repository 계층

`app/repositories/user_repository.py`에 `UserRepository`를, `app/repositories/auth_repository.py`에 `AuthRepository`를 작성했다. 각각 SQLAlchemy 세션을 받아서 도메인에 필요한 쿼리를 제공한다.

## Phase 3: 보안 유틸리티

### `app/core/security.py` 작성

이 파일이 이 랩의 핵심이다. 여기에 들어간 함수들:
- `hash_password()` / `verify_password()`: Argon2 래퍼
- `generate_random_token()`: `secrets.token_urlsafe(32)`
- `hash_secret()`: HMAC-SHA256으로 토큰 해시
- `build_access_token()` / `decode_access_token()`: JWT 발행/검증
- `validate_csrf()`: cookie와 header의 CSRF token 비교
- `set_access_cookie()` / `set_refresh_cookie()` / `set_csrf_cookie()`: 응답에 cookie 설정
- `clear_auth_cookies()`: 로그아웃 시 cookie 제거

### `app/core/errors.py` 작성

`AppError` 예외 클래스와 전역 에러 핸들러를 구성했다. 모든 에러 응답은 `{"error": {"code": "...", "message": "...", "details": {}}}` 형태로 통일했다.

### `app/core/rate_limit.py` 작성

Redis가 있으면 Redis pipeline으로, 없으면 in-memory dictionary로 rate limiting을 처리하는 `RateLimiter` 클래스를 만들었다.

## Phase 4: 인증 서비스 로직

### `app/domain/services/auth.py`  작성

`AuthService` 클래스에 credential lifecycle의 모든 비즈니스 로직을 모았다:
- `register_user()`: 이메일/핸들 중복 확인 → Argon2 해시 → User 생성 → verification token 발행 → 메일 큐잉
- `verify_email()`: token 해시 조회 → 만료 확인 → `email_verified_at` 설정
- `authenticate_user()`: 이메일로 사용자 조회 → Argon2 검증 → 이메일 인증 여부 확인
- `request_password_reset()`: 사용자 존재 여부와 관계없이 동일한 응답 → token 발행 → 메일 큐잉
- `reset_password()`: token 검증 → 새 비밀번호 Argon2 해시 → 저장
- `issue_session()`: refresh token + access token + CSRF token 한 묶음 발행
- `rotate_refresh_token()`: 기존 token 폐기 → 새 token 발행 (같은 family_id 유지)
- `revoke_refresh_token()`: 단일 token 또는 family 폐기

## Phase 5: API 라우트

### `app/api/v1/routes/auth.py` 작성

7개의 엔드포인트를 구현했다:
- `POST /register`: 회원가입
- `POST /verify-email`: 이메일 검증
- `POST /login`: 로그인 (cookie 발행)
- `GET /me`: 현재 사용자 조회
- `POST /password-reset/request`: 비밀번호 재설정 요청
- `POST /password-reset/confirm`: 비밀번호 재설정 확인
- `POST /token/refresh`: 토큰 갱신 (CSRF 필수)
- `POST /logout`: 로그아웃 (CSRF 필수)

### `app/api/deps.py` 작성

FastAPI 의존성 함수들: `get_auth_service()`, `get_mailbox()`, `require_csrf()`, `get_current_user()`.

## Phase 6: 앱 부트스트랩

### `app/bootstrap.py`와 `app/main.py`

`bootstrap.py`에 `initialize_schema()`를 만들어 `Base.metadata.create_all()`을 호출하게 했다. `main.py`에서 `lifespan` hook으로 이 함수를 부르고, `create_app()` 팩토리에서 CORS, 에러 핸들러, 라우터를 등록했다.

```bash
make run
# uvicorn app.main:app --reload
# http://localhost:8000/docs 에서 Swagger UI 확인
```

## Phase 7: Docker Compose 환경

### Dockerfile과 compose.yaml

`Dockerfile`을 작성해서 Python 3.12-slim 이미지 위에 앱을 패키징했다. `compose.yaml`에는 4개 서비스를 정의했다:
- `api`: FastAPI 앱 (포트 8000)
- `db`: PostgreSQL 16 (포트 5432)
- `redis`: Redis 7 (포트 6379)
- `mailpit`: Mailpit v1.20 (포트 8025, 메일 UI)

```bash
cp .env.example .env
# .env 파일에서 DATABASE_URL을 PostgreSQL로 변경
docker compose up --build
```

### Alembic 설정

`alembic init alembic`으로 마이그레이션 디렉터리를 초기화하고, `alembic/env.py`에서 `app.core.config`의 settings를 읽어 `sqlalchemy.url`을 동적으로 설정하도록 수정했다.

```bash
alembic revision --autogenerate -m "initial tables"
alembic upgrade head
```

## Phase 8: 테스트

### `tests/conftest.py`

테스트 환경 전용 설정: 임시 디렉터리에 SQLite DB를 생성하고, `monkeypatch`로 환경 변수를 주입한다. 매 테스트마다 테이블을 drop/create해서 격리를 보장한다.

### `tests/integration/test_local_auth.py`

3개의 통합 테스트:
1. **login-refresh-rotation-and-logout**: 가입 → 이메일 검증 → 로그인 → refresh rotation → 탈취된 토큰 재사용 감지 → 재로그인 → 로그아웃
2. **password-reset-flow**: 가입 → 이메일 검증 → 비밀번호 재설정 요청 → 새 비밀번호로 재설정 → 구 비밀번호 로그인 실패 → 신 비밀번호 로그인 성공
3. **csrf-rejects-refresh-without-header**: CSRF 헤더 없이 refresh 시 403 반환 확인

```bash
make test
```

### `tests/smoke.py`

최소한의 smoke 테스트: 임시 환경에서 앱을 띄우고 `/api/v1/health/live` 엔드포인트가 200을 반환하는지만 확인한다.

```bash
make smoke
```

## Phase 9: 검증과 마무리

### 최종 검증 순서

```bash
make lint       # ruff로 코드 품질 확인
make test       # pytest로 통합 테스트 실행
make smoke      # smoke 테스트로 앱 기동 확인
docker compose up --build  # 전체 스택 부팅 확인
```

### 문서 정리

`fastapi/README.md`에 build/lint/test/smoke/docker 명령을 정리했다. `docs/README.md`에 핵심 개념 요약을 적었다.
