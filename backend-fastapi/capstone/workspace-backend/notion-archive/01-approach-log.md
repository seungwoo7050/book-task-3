# 접근 기록: 교과서 조각들을 서비스로 묶기

## 선택지들

**1) 랩 코드를 그대로 import해서 조립한다**
빠르지만, capstone 자체의 설계 판단이 보이지 않는다.
"import해서 붙였다"는 증거는 약하다.

**2) 전혀 다른 도메인으로 새 서비스를 만든다**
재미있지만, 랩에서 배운 것과의 연결이 끊어진다.

**3) SaaS 협업 도구 백엔드로 재설위한다**
auth(사용자), workspace(조직), project/task/comment(데이터),
notification(비동기), WebSocket(실시간)이 자연스럽게 맞물린다.
각 랩의 개념이 억지 없이 통합된다.

세 번째를 선택했다.

## 핵심 설계 결정

### 도메인 모델 통합

랩별로 분리되어 있던 모델들이 하나의 DB에 들어간다:

**auth 쪽** — `User`, `ExternalIdentity`, `RefreshToken`, `EmailToken`
A-auth-lab의 local auth 모델 + B-federation-security-lab의 external identity.
refresh token은 family rotation 패턴을 유지한다.

**platform 쪽** — `Workspace`, `Membership`, `Invite`, `Project`, `Task`, `Comment`, `Notification`
C-authorization-lab의 RBAC 구조 위에 D-data-api-lab의 CRUD 모델을 얹고,
E-async-jobs-lab의 notification queue를 붙였다.

### 서비스 레이어 분리

`AuthService`와 `PlatformService` 두 개로 나눴다.

- `AuthService`: 회원가입, 이메일 인증, local/Google 로그인, session 발급/갱신
- `PlatformService`: workspace CRUD, invite, project/task/comment, notification drain, presence

PlatformService는 `ConnectionManager`와 `PresenceTracker`를 생성자 인자로 받는다.
이 둘은 `app.state`에 저장되어 있고, deps.py에서 주입된다.

### Cookie 기반 인증 + CSRF

access token을 httpOnly cookie에 넣고,
state 변경 요청(refresh, logout)에는 CSRF token을 요구한다.

- `access_token` cookie: httpOnly, SameSite=lax
- `refresh_token` cookie: httpOnly, SameSite=lax
- `csrf_token` cookie: httpOnly=False (JS에서 읽어서 헤더로 보내야 하므로)
- `X-CSRF-Token` 헤더: CSRF cookie 값과 대조

### WebSocket 인증

WebSocket은 cookie를 자동으로 보내지 않으므로,
query parameter `?access_token=`으로 JWT를 전달한다.
`decode_access_token`으로 검증 후 user_id를 추출한다.

### Notification + Drain + WebSocket 연결

코멘트 생성 시 같은 워크스페이스의 다른 멤버에게 `Notification` record를 만든다.
`drain_notifications`를 호출하면 queued 상태의 알림을 꺼내
ConnectionManager를 통해 WebSocket으로 전달하고 `sent`로 바꾼다.

이것은 E-async-jobs-lab의 outbox 패턴과 F-realtime-lab의 WebSocket 전달을
하나의 흐름으로 합친 것이다.

### Schema Bootstrapping

`lifespan` context manager에서 `initialize_schema()`가 `Base.metadata.create_all()`을 호출한다.
Alembic migration이 아니라 direct schema creation이므로,
`make smoke`이나 테스트에서 별도의 migration 단계 없이 바로 동작한다.

## 버린 아이디어

- lab 패키지를 직접 import하는 방식: 설계 증거가 약하다.
- Celery worker를 capstone에 넣는 방식: drain + WebSocket으로 충분하다.
- Alembic migration을 capstone에서 유지하는 방식: 학습 저장소에서는 auto-create가 더 편하다.
