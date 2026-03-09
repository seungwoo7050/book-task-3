# Capstone: 일곱 개의 랩을 하나의 서비스로 재조립하기

## 왜 이 프로젝트가 필요한가

A부터 G까지의 랩은 각각 하나의 백엔드 역량에 집중한다.
인증, 외부 로그인, 권한, CRUD, 비동기 처리, 실시간 통신, 운영성.
이것들은 개별적으로 의미가 있지만, 실제 서비스에서는 한 코드베이스 안에서 만난다.

workspace-backend는 "SaaS 협업 도구의 백엔드"라는 하나의 도메인 안에서
이 모든 역량을 재조합하는 capstone 프로젝트다.
랩 코드를 import하는 것이 아니라, 같은 개념을 통합된 설계 안에서 다시 만든다.

## 어떤 서비스인가

| 기능 | 대응 랩 | capstone에서의 위치 |
|------|---------|---------------------|
| 회원가입 + 로그인 | A-auth-lab | local auth (email/password + email verification) |
| Google 로그인 | B-federation-security-lab | ExternalIdentity 연동 |
| 워크스페이스 + 멤버 초대 | C-authorization-lab | workspace RBAC (owner → invite → member) |
| 프로젝트/태스크/코멘트 | D-data-api-lab | workspace 경계 안의 CRUD |
| 알림 큐잉 | E-async-jobs-lab | Notification table + drain |
| WebSocket 실시간 전달 | F-realtime-lab | ConnectionManager + PresenceTracker |
| JSON 로깅, health check | G-ops-lab | /health/live, /health/ready, structured logging |

## 핵심 흐름

```
사용자 회원가입 → 이메일 인증 → 로그인 (local 또는 Google)
→ 워크스페이스 생성 → 멤버 초대 → 초대 수락
→ 프로젝트 생성 → 태스크 생성 → 코멘트 작성
→ 코멘트 시 멤버에게 알림 큐잉
→ drain → WebSocket으로 실시간 전달
```

이 흐름이 테스트 하나에 전부 들어간다 (`test_capstone.py`).

## 제약과 경계

| 항목 | 선택 |
|------|------|
| 프레임워크 | FastAPI |
| DB | PostgreSQL 16 (compose), SQLite (test) |
| Redis | compose에 포함, rate limiter에서 사용 |
| WebSocket | Starlette 네이티브, 인메모리 ConnectionManager |
| 인증 | PyJWT access token + cookie + CSRF |
| schema init | lifespan에서 `Base.metadata.create_all()` |
| 프론트엔드 | 없음 |
| 클라우드 배포 | 없음 |

## 불확실한 것

- 모든 concern을 한 서비스에 넣으면 각 랩의 단순함이 사라진다.
  하지만 capstone의 목적은 "통합 설계를 보여주는 것"이다.
- worker 프로세스 분리 없이 drain + WebSocket을 같은 프로세스에서 처리한다.
- 프론트엔드와 클라우드 배포는 범위 밖이다.
