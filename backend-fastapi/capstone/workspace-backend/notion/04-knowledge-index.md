# 지식 인덱스: Capstone 통합 설계 정리

## 아키텍처 개요

```
Client (Browser/Test)
  │
  ├── HTTP ──→ FastAPI ──→ AuthService ────→ auth tables
  │                   └──→ PlatformService ──→ platform tables
  │                            │
  │                            ├── 코멘트 생성 시 Notification 큐잉
  │                            └── drain 시 ConnectionManager로 전달
  │
  └── WS  ──→ /ws/notifications ──→ ConnectionManager (인메모리)
                                        ↑
                                  PresenceTracker (인메모리)
```

## Cookie 기반 인증

### Token 종류

| 이름 | 저장 위치 | httpOnly | 용도 |
|------|-----------|----------|------|
| access_token | cookie | Yes | API 인증 (15분 TTL) |
| refresh_token | cookie | Yes | access token 갱신 (14일 TTL) |
| csrf_token | cookie | No | CSRF double-submit |

### CSRF Double-Submit 패턴

1. 로그인 시 서버가 `csrf_token` cookie를 발행한다 (httpOnly=False)
2. 클라이언트(JS)가 cookie에서 csrf_token을 읽는다
3. 상태 변경 요청(refresh, logout)에서 `X-CSRF-Token` 헤더로 보낸다
4. 서버가 cookie의 값과 헤더의 값을 `secrets.compare_digest`로 비교한다

왜 이래야 하는가:
- httpOnly cookie는 JS에서 읽을 수 없으므로 CSRF 공격에 안전하다
- 하지만 CSRF 공격자도 cookie를 자동으로 보낼 수 있다
- 따라서 "cookie 값을 알고 있다는 것"을 증명하기 위해 헤더로도 보내야 한다

## Refresh Token Rotation

```
login → (access + refresh₁ + csrf) 발급
         ↓
refresh 요청 → refresh₁ revoke → (access + refresh₂ + csrf) 발급
         ↓
refresh₂ 재사용 → family 전체 revoke → 401
```

`family_id`로 같은 세션의 refresh token들을 묶는다.
이전 token이 재사용되면 전체 family를 revoke하고 401을 반환한다.
이것은 refresh token 탈취 시 피해를 제한하는 패턴이다.

## Workspace RBAC 모델

```
User → Membership(role) → Workspace → Project → Task → Comment
                                                          ↓
                                                    Notification
```

- owner: 워크스페이스 생성자, 멤버 초대 가능
- member: invited + accepted, 프로젝트/태스크/코멘트 CRUD 가능
- 모든 CRUD는 `_require_member()`로 멤버십을 먼저 확인한다

## Notification Pipeline

```
Comment 생성
  └── 같은 workspace의 다른 멤버마다 Notification(status="queued") 생성
         └── POST /notifications/drain
                └── queued 알림 조회
                      └── ConnectionManager.send_notification(user_id, payload)
                            └── 해당 user의 모든 WebSocket에 JSON 전송
                                  └── notification.status = "sent"
```

E-async-jobs-lab과의 차이:
- Celery worker 없이 같은 프로세스에서 drain한다
- outbox event 대신 Notification 테이블이 직접 queue 역할을 한다
- idempotency key 없음 (코멘트 생성이 자연스럽게 1:1이므로)

## Rate Limiter

```python
class RateLimiter:
    # Redis가 있으면 INCR + EXPIRE
    # Redis가 없으면 인메모리 dict + threading.Lock
```

dual backend 설계: Redis가 configure되지 않은 환경에서도 동작한다.
`client_ip` 기반으로 rate를 계산하고, 초과 시 429를 반환한다.

## Schema Bootstrapping

```python
@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_schema()  # Base.metadata.create_all(bind=engine)
    yield
```

Alembic migration 대신 direct schema creation을 사용한다.
장점: smoke test와 CI에서 별도 migration 단계 없이 바로 동작한다.
단점: schema 변경 이력이 없다.

## 통합 테스트 구조

`test_capstone.py` 하나의 테스트 함수에 전체 흐름이 들어간다:

```
1. owner 회원가입 + 이메일 인증 + 로그인
2. collaborator Google 로그인
3. workspace 생성 → invite → accept
4. collaborator WebSocket 연결
5. project → task → comment 생성
6. drain → WebSocket 수신 확인
7. /me 엔드포인트로 인증 상태 확인
```

## 용어 정리

| 용어 | 의미 |
|------|------|
| capstone | 교과 과정의 최종 통합 프로젝트 |
| double-submit | CSRF 방어: cookie + header에 같은 값을 보내 증명 |
| family rotation | refresh token을 family로 묶어 재사용 탐지 |
| drain | queued 알림을 꺼내 실시간 전달하는 작업 |
| bootstrap | 앱 시작 시 schema를 자동 생성하는 초기화 |
| fan-out | 하나의 알림을 여러 WebSocket에 동시 전달 |

## 참고 자료

| 제목 | 출처 | 확인 | 비고 |
|------|------|------|------|
| OAuth 2.0 Security Best Practices | IETF RFC 6819 | 2025-01 | refresh token rotation |
| CSRF Prevention Cheat Sheet | OWASP | 2025-01 | double-submit cookie |
| FastAPI Cookie Auth | fastapi.tiangolo.com | 2025-01 | httpOnly cookie 설정 |
| SQLAlchemy Metadata | docs.sqlalchemy.org | 2025-01 | create_all, drop_all |
