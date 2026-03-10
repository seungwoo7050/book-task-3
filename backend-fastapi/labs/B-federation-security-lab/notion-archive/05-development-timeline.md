# Development Timeline

## Phase 1: 프로젝트 초기 세팅

A-auth-lab의 구조를 참고하되, 완전히 새로운 프로젝트로 시작한다.

```bash
mkdir -p labs/B-federation-security-lab/fastapi
cd labs/B-federation-security-lab/fastapi

# pyproject.toml 작성 후 개발 모드 설치
python3 -m pip install -e ".[dev]"
```

핵심 의존성은 A-auth-lab과 겹치지만 두 가지가 추가된다:
- `pyotp` — TOTP 코드 생성 및 검증용
- `itsdangerous` — OAuth state를 서명된 쿠키에 저장하기 위해
- `httpx` — Google 토큰/유저인포 엔드포인트 호출용 (테스트에서는 mock)
- `redis` — rate limiting 백엔드

```bash
# 전체 의존성 확인
pip list | grep -E "pyotp|itsdangerous|httpx|redis"
```

패키지 구조를 잡는다:
```
app/
  api/
    v1/
      routes/
        auth.py
        health.py
      router.py
    deps.py
  core/
    config.py
    errors.py
    logging.py
    rate_limit.py
    security.py
  db/
    base.py
    models/
      user.py
      auth.py
    session.py
  domain/
    services/
      auth.py
      google_oidc.py
      two_factor.py
  repositories/
    auth_repository.py
    user_repository.py
  schemas/
    auth.py
    common.py
  main.py
```

## Phase 2: 데이터 모델 설계

User 모델은 A-auth-lab보다 확장된다. `password_hash`가 사라지고 대신 2FA 관련 필드가 추가된다:

```python
# app/db/models/user.py
class User(TimestampMixin, Base):
    # ... 기본 필드 (id, handle, email, display_name, avatar_url, is_active)
    two_factor_enabled: Mapped[bool]
    two_factor_secret: Mapped[str | None]
    pending_two_factor_secret: Mapped[str | None]
```

`ExternalIdentity` 모델을 새로 추가한다. 핵심은 `(provider, provider_subject)` 유니크 제약이다:

```python
class ExternalIdentity(TimestampMixin, Base):
    __table_args__ = (
        UniqueConstraint("provider", "provider_subject",
                        name="uq_external_identity_provider_subject"),
    )
    provider: Mapped[str]          # "google"
    provider_subject: Mapped[str]  # Google의 sub claim
    profile: Mapped[dict]          # JSON으로 원본 프로필 저장
```

RefreshToken은 A-auth-lab과 동일한 family 구조, TwoFactorRecoveryCode와 AuthAuditLog가 새로 추가된다.

## Phase 3: Google OIDC 서비스 구현

`GoogleOIDCService` 클래스를 만든다. 실제 Google API를 호출하는 세 메서드:

1. `build_authorization_request()` — state, nonce, code_verifier 생성, authorization URL 조립
2. `exchange_code_for_tokens(code, code_verifier)` — httpx.post로 토큰 교환
3. `validate_id_token(id_token, nonce)` — PyJWT + JWKS로 서명 검증
4. `fetch_userinfo(access_token)` — userinfo endpoint에서 아바타 등 추가 정보

PKCE 관련 유틸리티를 `security.py`에 추가:

```python
def generate_pkce_verifier() -> str:
    return secrets.token_urlsafe(64)

def build_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")
```

OAuth state 서명/복원도 같은 파일에:

```python
def sign_oauth_state(payload: dict, settings: Settings) -> str:
    serializer = URLSafeSerializer(settings.secret_key, salt="google-oidc-state")
    return serializer.dumps(payload)
```

## Phase 4: Auth 서비스 — Federation + Session 발급

`AuthService`에 `sync_google_user` 메서드를 구현한다. external identity 검색 → 이메일 매칭 → 신규 생성의 3단계 흐름.

세션 발급 흐름에 2FA 분기를 추가한다:

```
callback 도착
  → sync_google_user
  → user.two_factor_enabled?
    → True:  start_pending_second_factor → pending_auth_token 반환
    → False: issue_session → access + refresh + csrf 반환
```

pending_auth_token은 type이 `"pending_2fa"`인 JWT이고 TTL 300초.

## Phase 5: 2FA 서비스 구현

`TwoFactorService` 클래스:

```python
# pyotp를 사용한 TOTP 구현
secret = pyotp.random_base32()
uri = pyotp.TOTP(secret).provisioning_uri(email, issuer_name="b-federation-security-lab")
is_valid = pyotp.TOTP(secret).verify(code, valid_window=1)
```

Recovery code 생성: `secrets.choice`로 `XXXX-XXXX` 형태 8개 생성, HMAC-SHA256 해시로 DB 저장.

## Phase 6: API 라우트 구현

엔드포인트 목록:
- `GET  /auth/google/login` — authorization URL 반환 + state 쿠키 설정
- `GET  /auth/google/callback` — 코드 교환 + identity linking + 세션/pending 발급
- `GET  /auth/me` — access_token 쿠키 검증 + 사용자 정보 반환
- `POST /auth/token/refresh` — refresh token rotation (CSRF 필수)
- `POST /auth/logout` — refresh token revoke + 쿠키 제거 (CSRF 필수)
- `POST /auth/2fa/setup` — pending secret 생성 (인증 필수, CSRF 필수)
- `POST /auth/2fa/confirm` — TOTP 검증 + 2FA 활성화 + recovery codes 반환
- `POST /auth/2fa/verify` — pending_auth → TOTP/recovery 검증 → 세션 발급
- `POST /auth/2fa/recovery-codes/regenerate` — recovery code 재생성
- `POST /auth/2fa/disable` — 2FA 비활성화

Rate limiter를 `Depends`로 해당 엔드포인트에 적용:

```python
@router.get("/google/login",
    dependencies=[Depends(RateLimiter(limit=10, window_seconds=60, prefix="auth:google-login"))])
```

## Phase 7: Docker Compose 구성

```yaml
# compose.yaml - 서비스 3개
services:
  api:     # FastAPI + Alembic migration
  db:      # PostgreSQL 16's POSTGRES_DB=b_federation_security_lab
  redis:   # Redis 7 — rate limiting 백엔드
```

```bash
docker compose up --build -d
docker compose ps
docker compose logs api --tail 30

# health check
curl -s http://localhost:8000/api/v1/health/live
```

A-auth-lab과 달리 Redis가 추가되었고, 포트는 기본 8000/5432/6379.

## Phase 8: Alembic 마이그레이션

```bash
cd labs/B-federation-security-lab/fastapi

# 마이그레이션 파일 생성
alembic revision -m "initial schema"
# → alembic/versions/20260308_0001_initial.py 생성
```

마이그레이션이 생성하는 테이블 5개:
1. `users` — handle, email, two_factor 관련 필드
2. `external_identities` — provider + provider_subject 유니크 제약
3. `refresh_tokens` — family_id 기반 토큰 체인
4. `two_factor_recovery_codes` — 해시 기반 recovery code
5. `auth_audit_logs` — event_type + details JSON

```bash
# 마이그레이션 적용
alembic upgrade head

# 테이블 확인 (Docker Compose PostgreSQL)
docker compose exec db psql -U postgres -d b_federation_security_lab -c "\dt"
```

## Phase 9: 테스트 작성 및 실행

conftest 설정의 핵심:
- SQLite in-memory로 테스트 격리
- `RateLimiter._memory_store.clear()` — 테스트 간 rate limit 상태 초기화
- `get_settings.cache_clear()` — 환경변수 오염 방지

Google OIDC mock 패턴:

```python
# monkeypatch로 GoogleOIDCService의 세 메서드를 대체
monkeypatch.setattr(GoogleOIDCService, "exchange_code_for_tokens", fake_exchange)
monkeypatch.setattr(GoogleOIDCService, "validate_id_token", fake_validate)
monkeypatch.setattr(GoogleOIDCService, "fetch_userinfo", fake_userinfo)
```

테스트 시나리오:
1. Google callback → 사용자 생성 + 세션 발급 → `/me` 확인
2. 2FA setup → confirm → recovery code 수령
3. 2FA 사용자 Google 로그인 → pending 상태 → `/me` 401 → recovery code로 verify → `/me` 200

```bash
make test
make lint
make smoke

# Docker Compose 상태에서의 통합 검증
docker compose exec api pytest
```

## Phase 10: Rate Limiter 검증

```bash
# 로컬에서 rate limit 동작 확인 (11번 연속 요청)
for i in $(seq 1 11); do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/api/v1/auth/google/login
done
# 11번째부터 429 반환

# Redis 키 확인
docker compose exec redis redis-cli KEYS "auth:*"
```

## Phase 11: 최종 검증

```bash
make lint    # ruff check
make test    # pytest
make smoke   # smoke test 스크립트

# Compose probe
docker compose up --build -d
curl -sf http://localhost:8000/api/v1/health/live
curl -sf http://localhost:8000/api/v1/health/ready
docker compose down
```
