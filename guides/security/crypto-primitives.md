# 암호 기본 원소 완전 가이드 (Crypto Primitives)

세 가지 질문이 primitive를 구분한다:

1. 이 데이터가 이전과 같은가? → **Hash**
2. secret을 아는 쪽이 이 메시지를 만들었는가? → **MAC**
3. 이 secret에서 새 key를 만들거나 brute-force를 비싸게 해야 하는가? → **KDF**

---

## 1. Hash — 동일성 확인, secret 없음

Hash는 입력이 같으면 항상 같은 출력을 내고, 역산이 계산적으로 불가능하다. **key가 없으므로** 누구나 같은 입력으로 같은 출력을 만들 수 있다.

```python
import hashlib

# SHA-256: 파일 무결성 확인
def file_checksum(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

# SHA3-256: NIST 표준, Keccak 기반
def content_fingerprint(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()

# 사용 예
checksum = file_checksum('firmware.bin')
cache_key = hashlib.sha256(query.encode()).hexdigest()[:16]
```

| 용도 | 적절한가? | 이유 |
|------|---------|------|
| 파일 체크섬, 캐시 key | ✅ | 단순 식별, secret 불필요 |
| 비밀번호 저장 | ❌ | GPU로 초당 수십억 회 시도 가능 |
| webhook 서명 | ❌ | key 없어서 공격자도 동일 출력 생성 가능 |
| content fingerprint (Git object ID 등) | ✅ | 공개 입력 OK |

---

## 2. MAC — secret을 가진 쪽이 만들었음을 증명

MAC(Message Authentication Code)은 key와 message를 함께 사용한다. key를 모르면 같은 MAC을 재현할 수 없다.

```python
import hmac
import hashlib
import secrets

# HMAC-SHA256: 표준 MAC 구현
key = secrets.token_bytes(32)   # 32바이트 랜덤 key
message = b'user_id=42&action=delete'

mac = hmac.new(key, message, hashlib.sha256).hexdigest()

# 검증: 상수 시간 비교 필수
def verify_mac(key: bytes, message: bytes, received_mac: str) -> bool:
    expected = hmac.new(key, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, received_mac)  # timing attack 방어
```

`==` 대신 `hmac.compare_digest`를 써야 하는 이유: 문자열 `==`는 첫 불일치에서 빠르게 반환한다. 응답 시간 차이를 측정하면(timing attack) 유효한 MAC의 앞 몇 바이트를 추측할 수 있다. `compare_digest`는 항상 전체 길이를 비교한다.

```python
# webhook signature 검증 (GitHub, Stripe 패턴)
def verify_webhook(payload: bytes, signature_header: str, secret: str) -> bool:
    expected = 'sha256=' + hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)

# signed cookie: 위변조 감지
def sign_cookie(value: str, secret_key: bytes) -> str:
    sig = hmac.new(secret_key, value.encode(), hashlib.sha256).hexdigest()[:16]
    return f'{value}.{sig}'

def verify_cookie(cookie: str, secret_key: bytes) -> str | None:
    if '.' not in cookie:
        return None
    value, received_sig = cookie.rsplit('.', 1)
    expected_sig = hmac.new(secret_key, value.encode(), hashlib.sha256).hexdigest()[:16]
    if not hmac.compare_digest(expected_sig, received_sig):
        return None
    return value
```

plain hash가 MAC을 대체하지 못하는 이유: key가 없으므로 공격자도 message만 알면 같은 hash를 만들 수 있다. `SHA256(secret + message)` 패턴도 length extension attack에 취약하다.

---

## 3. KDF — secret에서 새 key material 뽑기

KDF(Key Derivation Function)는 두 가지 목적으로 나뉜다.

### 3-1. Password KDF — brute-force를 비싸게 만들기

비밀번호는 entropy가 낮다. 빠른 hash로 저장하면 공격자는 GPU로 초당 수십억 번을 시도할 수 있다.

```python
import bcrypt
import argon2  # pip install argon2-cffi

# bcrypt
password = b'my-password'
salt = bcrypt.gensalt(rounds=12)   # cost factor: 2^12 반복, ~100ms
hashed = bcrypt.hashpw(password, salt)
assert bcrypt.checkpw(password, hashed)   # 상수 시간 비교 내장

# Argon2id (2023년 이후 권장)
ph = argon2.PasswordHasher(
    time_cost=2,        # 반복 횟수
    memory_cost=65536,  # 메모리 사용량 (KB)
    parallelism=2,
)
hashed = ph.hash('my-password')
try:
    ph.verify(hashed, 'my-password')  # OK 또는 VerifyMismatchError
except argon2.exceptions.VerifyMismatchError:
    pass
```

왜 단순 SHA-256(password)가 안 되는가:
- SHA-256 하나는 수 nanosecond → GPU 클러스터로 초당 10억+ 회 시도 가능
- bcrypt rounds=12는 ~100ms → 같은 GPU로 초당 수천 회로 줄어듦
- Argon2id는 메모리도 많이 써서 ASIC/GPU 가속도 어렵게 만든다

### 3-2. Key Expansion KDF — 하나의 secret에서 목적별 키 분리

이미 충분한 entropy를 가진 secret에서 context별 하위 키를 안전하게 분리할 때 쓴다.

```python
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os

root_secret = os.urandom(32)  # 충분한 entropy의 root key

def derive_key(root: bytes, context: str, length: int = 32) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=context.encode(),  # context 분리: 같은 root에서 다른 키 유도
    )
    return hkdf.derive(root)

# 같은 root_secret에서 목적별로 독립된 키 생성
encryption_key = derive_key(root_secret, 'encryption/v1')
signing_key    = derive_key(root_secret, 'signing/v1')
session_key    = derive_key(root_secret, 'session/v1')
# 하나가 노출돼도 다른 키를 역산할 수 없다
```

---

## 4. Nonce와 Entropy

```python
import os, secrets

# nonce: 같은 key로 알고리즘을 반복해도 안전하게
# AES-GCM에서 같은 (key, nonce) 쌍이 두 번 쓰이면 전체 암호화가 깨진다
nonce = os.urandom(12)   # AES-GCM nonce: 96 bit, 절대 재사용 금지

# 안전한 랜덤 ID 생성
token      = secrets.token_hex(32)
session_id = secrets.token_urlsafe(32)
```

| 개념 | 질문 | 올바른 도구 |
|------|------|-----------|
| entropy | 입력이 충분히 예측 불가능한가? | `os.urandom()`, `secrets` 모듈 |
| nonce | 같은 key를 재사용해도 안전한가? | random nonce (same key 재사용 금지) |
| salt | 같은 password라도 다른 hash가 나오는가? | `os.urandom(16)` per record |

---

## 5. 흔한 실수 패턴

```python
# 실수 1: 비밀번호를 plain hash로 저장
hashed_pw = hashlib.sha256(password.encode()).hexdigest()  # GPU로 쉽게 crack
# 올바른 코드
hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# 실수 2: MAC 검증에 == 사용 (timing attack)
if expected_mac == received_mac:   # timing에서 정보 누출
    pass
# 올바른 코드
if hmac.compare_digest(expected_mac, received_mac):
    pass

# 실수 3: 같은 root key를 여러 목적에 직접 재사용
# 올바른 코드: HKDF로 목적별 분리
auth_key    = derive_key(root_secret, 'auth/v1')
session_key = derive_key(root_secret, 'session/v1')

# 실수 4: SHA256(secret + message) 형태의 self-made MAC
# length extension attack에 취약 → 반드시 hmac 모듈 사용
mac = hmac.new(secret, message, hashlib.sha256).hexdigest()  # 올바른 코드
```

---

## 빠른 참조

| Primitive | key 있음? | 계산 속도 | 주요 사용처 | 금지 사용처 |
|----------|---------|---------|-----------|-----------|
| SHA-256 / SHA-3 | 없음 | 빠름 | 파일 체크섬, 캐시 key | 비밀번호 저장, 인증 MAC |
| HMAC-SHA256 | 있음 (공유 key) | 빠름 | webhook 서명, 쿠키 무결성 | 비밀번호 저장 |
| bcrypt / Argon2id | 있음 (salt 내장) | 느림 (의도적) | 비밀번호 해시 저장 | 대량 데이터 체크섬 |
| HKDF | 있음 (root key) | 빠름 | key 분리 / 확장 | 비밀번호 직접 저장 |

연결 프로젝트: [crypto-primitives-in-practice](../../security-core/study/Foundations-Security/crypto-primitives-in-practice/README.md)
