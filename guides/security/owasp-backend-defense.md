# OWASP 백엔드 방어 완전 가이드

Backend endpoint 설계에서 반복 등장하는 다섯 가지 방어 경계를 코드 수준으로 정리한다.

```
사용자 입력 → [1. Injection 방어] → 서버 로직 → [2. Access Control 확인]
          → 외부 호출 → [3. SSRF 방어] → 응답 → [4. Error 노출 통제]
          → 파일 접근 → [5. Path Traversal 방어]
```

---

## 1. Injection — 입력이 쿼리 구조를 바꾸지 못하게

SQL injection 이외에 NoSQL, LDAP, command injection도 같은 원칙으로 방어한다: **사용자 입력은 값이지 구조가 아니다.**

```python
import sqlite3
from sqlalchemy import text
from sqlalchemy.orm import Session

# 취약: 문자열 포맷팅으로 쿼리 조립
def get_user_UNSAFE(conn, username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return conn.execute(query)  # username = "' OR '1'='1" 이면 모든 행 반환

# 안전: parameterized query — 입력은 항상 값 위치에
def get_user_safe(conn: sqlite3.Connection, username: str):
    return conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()

# SQLAlchemy: ORM이라도 raw SQL에서는 bindparam 사용
def search_users(db: Session, name: str):
    # 취약: text() 안에서 f-string 사용
    # db.execute(text(f'SELECT * FROM users WHERE name = "{name}"'))

    # 안전: named bindparam
    return db.execute(
        text('SELECT * FROM users WHERE name = :name'),
        {'name': name}
    ).fetchall()

# OS command injection: subprocess에서 shell=True 금지
import subprocess

def convert_image_UNSAFE(filename: str):
    os.system(f'convert {filename} output.png')  # filename에 ; rm -rf / 삽입 가능

def convert_image_safe(filename: str):
    subprocess.run(
        ['convert', filename, 'output.png'],  # 리스트: 셸 처리 없음
        check=True, timeout=30
    )
```

---

## 2. Broken Access Control — 인증과 권한은 다른 질문

로그인 여부(authentication)와 해당 리소스에 접근할 권한(authorization)은 별도로 확인해야 한다.

```python
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

app = FastAPI()

# 취약: user_id를 경로에서만 받고 소유권 미확인
@app.get('/documents/{doc_id}')
def get_doc_UNSAFE(doc_id: int, current_user=Depends(get_current_user)):
    return db.get_document(doc_id)  # 다른 사용자 문서도 반환될 수 있음

# 안전: 소유권 + scope 확인
@app.get('/documents/{doc_id}')
def get_doc(doc_id: int, current_user=Depends(get_current_user)):
    doc = db.get_document(doc_id)
    if doc is None:
        raise HTTPException(404)
    # 소유자이거나 admin 권한인지 확인
    if doc.owner_id != current_user.id and 'admin' not in current_user.roles:
        raise HTTPException(403, 'Forbidden')
    return doc

# IDOR(Insecure Direct Object Reference) 방어 패턴
@app.put('/users/{target_user_id}')
def update_user(
    target_user_id: int,
    current_user=Depends(get_current_user),
):
    # 본인 또는 admin만 수정 가능
    if target_user_id != current_user.id and 'admin' not in current_user.roles:
        raise HTTPException(403)
    # ...

# JWT scope 확인
def require_scope(required: str):
    def checker(current_user=Depends(get_current_user)):
        if required not in current_user.scopes:
            raise HTTPException(403, f'Missing scope: {required}')
        return current_user
    return checker

@app.delete('/admin/users/{user_id}')
def delete_user(
    user_id: int,
    _=Depends(require_scope('admin:write')),
):
    # ...
    pass
```

---

## 3. SSRF — 서버가 대신 fetch할 때 경계 설정

서버가 사용자 입력 URL을 fetch하면 내부 네트워크, cloud metadata endpoint(169.254.169.254), 관리 포트에 접근할 수 있다.

```python
import ipaddress, re
from urllib.parse import urlparse
import httpx

# 사설 IP 대역 + loopback + link-local
BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),  # AWS metadata, Azure IMDS
    ipaddress.ip_network('::1/128'),
    ipaddress.ip_network('fc00::/7'),
]

ALLOWED_HOSTS = {'api.partner.com', 'cdn.example.com'}

def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False  # file://, gopher://, dict:// 등 차단

        # allowlist 우선 확인
        if parsed.hostname in ALLOWED_HOSTS:
            return True

        # IP 직접 지정 시 사설 대역 차단
        try:
            addr = ipaddress.ip_address(parsed.hostname)
            for net in BLOCKED_NETWORKS:
                if addr in net:
                    return False
        except ValueError:
            pass  # 도메인 이름 → DNS로 resolve 후 IP 재확인 필요

        return False  # 기본 거부 (allowlist 방식)
    except Exception:
        return False

async def fetch_external(url: str) -> bytes:
    if not is_safe_url(url):
        raise HTTPException(400, 'Blocked URL')
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content
```

**주의**: DNS rebinding 방어가 필요하다. 허용된 도메인이 resolve된 IP가 사설 대역이라면 차단해야 한다. 실무에서는 DNS resolve 후 IP를 다시 검증하거나 전용 egress proxy를 사용한다.

---

## 4. Error 노출 통제 — 내부 구조를 외부에 드러내지 않기

stacktrace, DB schema 이름, 내부 경로가 노출되면 공격자는 구조를 추측하기 쉬워진다.

```python
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# 위험: 예외를 그대로 응답에 포함
@app.exception_handler(Exception)
def unsafe_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'detail': str(exc), 'traceback': traceback.format_exc()},
        # → DB 연결 문자열, 파일 경로, 테이블 이름 등 노출 가능
    )

# 안전: 내부에는 로그, 외부에는 일반 메시지만
@app.exception_handler(Exception)
def safe_handler(request: Request, exc: Exception):
    # 내부 추적용 로그 (request_id 포함)
    request_id = request.headers.get('X-Request-ID', 'unknown')
    logger.exception('Unhandled error [%s] %s %s', request_id, request.method, request.url)

    # 외부에는 최소 정보만
    return JSONResponse(
        status_code=500,
        content={
            'error': 'Internal server error',
            'request_id': request_id,  # 로그 연계용
        },
    )

# 예측 가능한 에러 응답 형식: 어떤 에러든 같은 구조
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    code: str | None = None
    request_id: str | None = None
    # stacktrace, internal_path 같은 필드는 절대 포함하지 않는다
```

---

## 5. Path Traversal — 파일 경로를 사용자 입력으로 조립할 때

`../` 시퀀스와 symlink를 통해 허용된 디렉토리 밖의 파일에 접근할 수 있다.

```python
from pathlib import Path

UPLOAD_DIR = Path('/var/app/uploads').resolve()

# 취약: 사용자 입력을 경로에 직접 포함
def read_file_UNSAFE(filename: str) -> bytes:
    path = f'/var/app/uploads/{filename}'
    return open(path, 'rb').read()  # filename = '../../etc/passwd' 가능

# 안전: resolve() 후 허용 디렉토리 접두어 확인
def read_upload(filename: str) -> bytes:
    # 1단계: 경로 조합
    candidate = (UPLOAD_DIR / filename).resolve()

    # 2단계: 허용 디렉토리 안에 있는지 확인
    # is_relative_to는 Python 3.9+
    if not candidate.is_relative_to(UPLOAD_DIR):
        raise HTTPException(400, 'Invalid path')

    # 3단계: 실제 파일인지 확인 (symlink로 우회 방어)
    if not candidate.is_file():
        raise HTTPException(404)

    return candidate.read_bytes()

# 파일명만 허용 (슬래시 포함 금지)
import re

def sanitize_filename(name: str) -> str:
    # 영문, 숫자, 하이픈, 언더스코어, 점만 허용
    if not re.fullmatch(r'[a-zA-Z0-9._-]+', name):
        raise HTTPException(400, 'Invalid filename')
    if name.startswith('.'):
        raise HTTPException(400, 'Hidden files not allowed')
    return name
```

---

## 빠른 참조

| 취약점 | 입력 경로 | 방어 핵심 |
|-------|---------|---------|
| SQL/Command Injection | 사용자 입력 → 쿼리/명령 | parameterized query, 리스트 기반 subprocess |
| Broken Access Control | resource ID → DB 접근 | 소유권 확인, scope 검증 |
| SSRF | 사용자 URL → 서버 fetch | allowlist + 사설 IP 차단 |
| Error Exposure | 서버 예외 → 응답 본문 | 내부는 로그, 외부는 일반 메시지 |
| Path Traversal | 파일명 → 경로 조합 | resolve() + is_relative_to() |

연결 프로젝트: [owasp-backend-mitigations](../../security-core/study/Foundations-Security/owasp-backend-mitigations/README.md)
