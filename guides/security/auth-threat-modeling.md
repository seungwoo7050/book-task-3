# 인증 위협 모델링 완전 가이드 (Auth Threat Modeling)

세 가지 질문으로 auth 흐름을 분류한다:

1. 브라우저가 자동으로 자격증명을 보내는가? → **Cookie Session** (CSRF 방어 필요)
2. 클라이언트가 직접 토큰을 첨부하는가? → **Bearer JWT** (저장 위치 + 검증 규칙)
3. 제3자 identity provider가 개입하는가? → **OAuth / OIDC** (redirect 흐름 + state/PKCE)

---

## 1. Cookie Session — CSRF 방어

브라우저는 같은 도메인 쿠키를 자동으로 첨부한다. 공격자가 피해자 브라우저로 상태 변경 요청을 유도할 수 있다.

```python
from fastapi import FastAPI, Request, Response, Cookie, HTTPException
import secrets, hmac

app = FastAPI()

# 전략 1: SameSite=Strict — 같은 출처 요청에만 쿠키 첨부
@app.post('/login')
def login(response: Response):
    session_id = secrets.token_urlsafe(32)
    response.set_cookie(
        key='session_id',
        value=session_id,
        httponly=True,     # JS 접근 차단 (XSS 방어)
        secure=True,       # HTTPS 전용
        samesite='strict', # cross-site 요청 시 쿠키 미첨부
    )
    return {'ok': True}

# 전략 2: Synchronizer Token Pattern (CSRF token)
CSRF_SECRET = secrets.token_bytes(32)

def generate_csrf_token(session_id: str) -> str:
    return hmac.new(CSRF_SECRET, session_id.encode(), 'sha256').hexdigest()

@app.post('/transfer')
def transfer(
    request: Request,
    session_id: str = Cookie(default=None),
    csrf_token: str | None = None,  # body 또는 header에서 수동 첨부
):
    if not session_id:
        raise HTTPException(401)
    expected = generate_csrf_token(session_id)
    if not hmac.compare_digest(expected, csrf_token or ''):
        raise HTTPException(403, 'CSRF token mismatch')
    # ... 실제 처리

# 전략 3: Double-Submit Cookie — stateless CSRF 방어
# 쿠키에도 csrf_token을 싣고, body에도 같은 값 요구
# cross-site 요청은 쿠키를 읽지 못하므로 두 값이 불일치
```

| 전략 | 특징 | 제한 |
|------|------|------|
| SameSite=Strict | 설정만으로 cross-site 요청 차단 | 다른 도메인에서 링크 클릭 시 세션 유실 가능 |
| CSRF Token (Synchronizer) | 서버 상태 유지, 가장 확실 | 세션 저장소 필요 |
| Double-Submit Cookie | stateless, 분산 환경 적합 | subdomain takeover 시 우회 가능 |

---

## 2. Bearer JWT — 저장 위치와 검증 규칙

JWT는 서버가 상태를 보유하지 않아도 되지만, 저장 위치가 잘못되면 탈취 경로가 열린다.

```python
import jwt  # PyJWT
from datetime import datetime, timedelta, timezone

SECRET_KEY = 'change-this-in-production'

# 발급: 최소한의 claim만 포함
def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(user_id),
        'iat': now,
        'exp': now + timedelta(minutes=15),  # 짧은 유효기간
        'iss': 'api.example.com',            # issuer
        'aud': 'app.example.com',            # audience
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 검증: 모든 claim 명시적 확인
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['HS256'],  # 허용 알고리즘 명시 (alg:none 방어)
            audience='app.example.com',
            issuer='api.example.com',
            options={'require': ['exp', 'iat', 'sub', 'iss', 'aud']},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, 'Token expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(401, f'Invalid token: {e}')
```

**저장 위치별 위험:**

| 저장 위치 | XSS 노출 | CSRF 노출 | 권장 여부 |
|---------|---------|---------|---------|
| localStorage | ✅ 노출됨 | ✗ 안전 | ❌ 민감 토큰에 부적합 |
| sessionStorage | ✅ 노출됨 | ✗ 안전 | ❌ 동일 |
| HttpOnly Cookie | ✗ 안전 | ✅ 노출됨 | ✅ CSRF 방어와 병행 |
| Memory (JS 변수) | ✅ 노출됨 | ✗ 안전 | ✅ SPA에서 access token |

**흔한 JWT 검증 누락 패턴:**
```python
# 위험: algorithm 미지정 → alg:none 공격
jwt.decode(token, key)  # algorithms 인수 없음

# 위험: audience/issuer 미검증 → 다른 서비스 토큰 수락
jwt.decode(token, key, algorithms=['HS256'])  # aud, iss 확인 없음

# 위험: 만료된 토큰 허용
jwt.decode(token, key, algorithms=['HS256'], options={'verify_exp': False})
```

---

## 3. OAuth / OIDC redirect — state와 PKCE

공격자가 피해자를 자신이 제어하는 callback URI로 유도하거나, authorization code를 가로채지 못하도록 방어한다.

```python
import secrets, hashlib, base64
from urllib.parse import urlencode

# PKCE: Proof Key for Code Exchange
# authorization code 탈취 재사용 방어
def generate_pkce_pair() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()
    return code_verifier, code_challenge  # verifier: 로컬 보관, challenge: 서버로 전송

def build_authorization_url(client_id: str, redirect_uri: str) -> tuple[str, str, str]:
    state = secrets.token_urlsafe(32)          # CSRF 방어: session에 저장
    code_verifier, code_challenge = generate_pkce_pair()

    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'openid profile email',
        'state': state,                        # callback에서 검증
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    }
    url = 'https://idp.example.com/oauth/authorize?' + urlencode(params)
    return url, state, code_verifier

# callback 처리: state 검증 필수
def handle_callback(code: str, returned_state: str, saved_state: str, code_verifier: str):
    if not hmac.compare_digest(returned_state, saved_state):
        raise HTTPException(400, 'State mismatch: possible CSRF')
    # code_verifier를 token endpoint로 전송하면 서버가 검증
    # ...token exchange...

# OIDC: id_token claim 확인
def verify_id_token(id_token: str, expected_nonce: str) -> dict:
    # OIDC library (e.g. python-jose, authlib)로 파싱
    claims = decode_id_token(id_token, jwks_uri='https://idp.example.com/.well-known/jwks.json')
    assert claims['iss'] == 'https://idp.example.com'
    assert claims['aud'] == 'my-client-id'
    assert claims['nonce'] == expected_nonce  # replay attack 방어
    return claims
```

| 파라미터 | 방어 대상 | 없으면 |
|---------|---------|------|
| `state` | redirect CSRF | 공격자가 victim 브라우저로 자신의 code를 사용 |
| `code_challenge` (PKCE) | authorization code 탈취 | code를 가로챈 공격자가 token 교환 가능 |
| `nonce` (OIDC) | id_token replay | 이전 id_token을 다른 컨텍스트에서 재사용 |

---

## 4. Refresh Token과 Recovery Code

```python
import hashlib, secrets
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class RefreshToken:
    token_hash: str      # DB에는 hash만 보관
    user_id: int
    family: str          # rotation family: 재사용 탐지에 사용
    created_at: datetime
    used: bool = False

def issue_refresh_token(user_id: int, family: str | None = None) -> tuple[str, RefreshToken]:
    raw = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    record = RefreshToken(
        token_hash=token_hash,
        user_id=user_id,
        family=family or secrets.token_hex(16),
        created_at=datetime.now(timezone.utc),
    )
    return raw, record  # raw는 클라이언트로, record는 DB로

def rotate_refresh_token(raw_token: str, db) -> tuple[str, RefreshToken]:
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    existing = db.find_by_hash(token_hash)

    if existing is None:
        raise HTTPException(401, 'Unknown refresh token')

    if existing.used:
        # Refresh token reuse: 탈취 가능성 → 해당 family 전체 폐기
        db.revoke_family(existing.family)
        raise HTTPException(401, 'Refresh token reuse detected')

    existing.used = True
    db.save(existing)
    return issue_refresh_token(existing.user_id, family=existing.family)

# Recovery code (MFA backup): 평문이 아닌 hash로 저장
def generate_recovery_codes(count: int = 10) -> list[tuple[str, str]]:
    codes = []
    for _ in range(count):
        raw = secrets.token_hex(10)  # 사용자에게 보여주는 코드
        code_hash = hashlib.sha256(raw.encode()).hexdigest()
        codes.append((raw, code_hash))  # raw: 사용자에게, hash: DB에
    return codes
```

**Refresh token reuse detection**: 이미 사용된 토큰이 다시 들어오면 탈취 후 재사용을 의미할 수 있다. 같은 family 전체를 폐기해 피해를 최소화한다.

---

## 빠른 참조

| 흐름 | 핵심 공격면 | 필수 방어 |
|------|-----------|---------|
| Cookie Session | CSRF | SameSite=Strict 또는 CSRF token |
| Bearer JWT | 탈취 + 검증 우회 | HttpOnly 쿠키 저장, alg/aud/iss 명시 |
| OAuth/OIDC | redirect CSRF, code 탈취 | state 검증, PKCE |
| Refresh Token | 토큰 재사용 | rotation + reuse detection |
| Recovery Code | 평문 유출 | SHA-256 hash 저장 |

연결 프로젝트: [auth-threat-modeling](../../security-core/study/Foundations-Security/auth-threat-modeling/README.md)
선수 가이드: [crypto-primitives.md](crypto-primitives.md)
