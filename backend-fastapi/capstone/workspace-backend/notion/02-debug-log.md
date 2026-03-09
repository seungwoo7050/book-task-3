# 디버그 기록: 통합에서 만난 충돌들

## 문제 1: Schema bootstrapping 순서와 import 누락

### 증상

`create_app()` 호출 시 `initialize_schema()`가 테이블을 일부만 생성했다.
Membership, Invite 같은 테이블이 없어서 API 호출 시 `OperationalError`가 발생했다.

### 원인

`bootstrap.py`에서 import하는 모델 목록에 `Invite`, `Membership`이 빠져 있었다.
SQLAlchemy의 `Base.metadata.create_all()`은 import된 모델만 인식한다.
import가 없으면 metadata에 등록되지 않아 테이블이 생성되지 않는다.

### 해결

`bootstrap.py`에서 `db.models.auth`와 `db.models.platform`의 모든 모델을 명시적으로 import했다.
```python
from app.db.models import (Comment, EmailToken, ExternalIdentity, Invite,
                            Membership, Notification, Project, RefreshToken,
                            Task, User, Workspace)
```

### 교훈

SQLAlchemy의 declarative model은 import side effect에 의존한다.
"모델 파일이 있다"와 "metadata에 등록되었다"는 다른 이야기다.
bootstrap 파일에서 모든 모델을 explicit하게 import하면 이 문제를 방지할 수 있다.

## 문제 2: CSRF 검증과 TestClient의 cookie 전파

### 증상

`POST /token/refresh`에서 CSRF 검증이 실패했다.
cookie에 csrf_token이 있는데 헤더로 보내지 않으면 403이 반환된다.

### 원인

TestClient가 cookie를 자동으로 보내지만,
CSRF token은 JS에서 읽어서 `X-CSRF-Token` 헤더로 명시적으로 보내야 한다.
테스트 코드에서 csrf cookie를 읽어 헤더에 넣는 과정이 빠져 있었다.

### 해결

현재 테스트에서는 CSRF가 필요한 엔드포인트(refresh, logout)를 직접 호출하는 대신,
통합 흐름에서 login → cookie 자동 설정 → CSRF 헤더 첨부 순서를 맞췄다.

### 교훈

Cookie 기반 인증을 테스트할 때는 "브라우저가 해주는 일"을 테스트 코드에서
수동으로 재현해야 한다. CSRF는 특히 그렇다.

## 문제 3: WebSocket accept + disconnect 순서

### 증상

테스트에서 WebSocket 연결 후 drain → receive_json 순서에서
가끔 `WebSocketDisconnect`가 먼저 발생했다.

### 원인

`websocket_connect` context manager 안에서
HTTP 요청(drain)을 보내고 WebSocket 메시지를 받는 순서가
단일 프로세스 TestClient에서는 실행 순서가 보장되지 않을 수 있다.

### 해결

드레인을 먼저 호출하고 `receive_json`을 바로 이어서 실행하는 순서를 유지했다.
TestClient의 WebSocket 지원에서 send/receive가 동기적으로 동작하므로,
"drain → receive" 순서가 같은 스레드에서 실행되면 정상 동작한다.

### 교훈

WebSocket 테스트에서는 "누가 먼저 보내고, 누가 먼저 받는가"의 순서가
HTTP 테스트보다 훨씬 중요하다.
특히 통합 테스트에서 HTTP와 WebSocket을 섞을 때 주의해야 한다.

## 문제 4: lru_cache와 테스트 격리 (재발)

### 증상

두 번째 테스트 실행에서 이전 테스트의 SECRET_KEY가 남아
JWT 검증이 실패했다.

### 원인

G-ops-lab과 동일한 문제. `get_settings`의 `@lru_cache`가
테스트 간 상태를 공유한다.

### 해결

conftest에서 `get_settings.cache_clear()`를 fixture 시작/종료 시 호출.
`configure_engine()`도 명시적으로 재호출한다.

### 교훈

이 패턴은 이제 모든 lab에서 반복된다.
"Settings + lru_cache + monkeypatch" 조합에서는
cache_clear가 필수라는 것을 프로젝트 표준으로 정해야 한다.
