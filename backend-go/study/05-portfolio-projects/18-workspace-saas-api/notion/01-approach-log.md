# 접근 기록 — 7개 패키지로 구성된 SaaS API

## 패키지 구조

```
internal/
├── auth/       → JWT 서명/검증, 리프레시 토큰 생성
├── cache/      → Redis 클라이언트 (세션, 대시보드 캐시)
├── httpapi/    → HTTP 서버, 라우팅, 미들웨어, 인증 가드
├── platform/   → Config, AppError, Metrics, HTTP 유틸
├── repository/ → 도메인 모델, Store (PostgreSQL)
├── service/    → 비즈니스 로직 전체 조율
└── worker/     → Outbox Processor (알림 생성)
```

`cmd/api`(HTTP 서버)와 `cmd/worker`(백그라운드 프로세서)가 별도 바이너리. 같은 `internal/` 코드를 공유하지만 실행은 독립적.

## auth: 토큰 시스템

### Access Token (JWT)

`SignAccessToken` → `{"alg":"HS256","typ":"JWT"}` + Claims(sub, email, exp) + HMAC 서명
`ParseAccessToken` → 서명 검증 + 만료 검사

직접 구현한 HMAC-SHA256 JWT. 프로젝트 07에서의 경험을 가져옴.

### Refresh Token (Opaque)

```go
func GenerateRefreshToken(sessionID string) (rawToken, hash string, err error)
```

`sessionID.{32바이트 random}` 형태. 저장은 SHA256 해시로. 클라이언트에게 raw를 주고, DB/Redis에는 hash를 저장. raw가 유출돼도 hash에서 역산 불가.

rotation: refresh 사용 시 이전 세션을 무효화하고 새 세션 발급. 탈취된 refresh token 재사용 감지 가능.

## cache: Redis 통합

두 가지 용도:
1. **리프레시 세션**: `SetRefreshSession(sessionID, tokenHash, ttl)` → 세션 유효성 빠른 검증
2. **대시보드 캐시**: `SetDashboardSummary` / `GetDashboardSummary` → 30초 TTL 캐시

Redis 장애 시 fallback: 세션은 PostgreSQL의 `refresh_sessions` 테이블에도 저장. 대시보드는 캐시 미스 시 DB에서 직접 조회.

## platform: 횡단 관심사

### Config

환경 변수 기반 설정. `envString`, `envInt`, `envDuration` 헬퍼. 기본값 포함.

### Metrics

`atomic.Int64` 카운터. Prometheus text format으로 `/metrics`에서 노출.
- `workspace_requests_total`
- `workspace_auth_logins_total`
- `workspace_dashboard_cache_hits_total` / `misses`
- `workspace_worker_processed_events_total`

### AppError

HTTP 상태 코드 + 에러 코드 + 메시지를 포함한 구조화된 에러 타입. `platform.Errorf(http.StatusNotFound, "not_found", "player %s not found", id)`.

## repository: Store + Models

### Models

10개+ 도메인 타입: `User`, `AuthUser`, `Membership`, `Invitation`, `Project`, `Issue`, `Comment`, `RefreshSession`, `OutboxEvent`, `Notification`...

### Store

하나의 `Store` struct에 모든 SQL 접근. `*sql.DB`를 가짐. 트랜잭션이 필요한 메서드는 `*sql.Tx`를 인자로 받음.

## service: 비즈니스 로직

### RegisterOwner

트랜잭션 내에서: 사용자 생성(bcrypt) → 조직 생성 → 멤버십(owner) 생성 → JWT 발급 + refresh 세션 생성

### Login / Refresh / Logout

`bcrypt.CompareHashAndPassword` → 새 access/refresh 발급
`Refresh`: 세션 검증(Redis → DB fallback) → 이전 세션 revoke → 새 세션 발급 (rotation)
`Logout`: 세션 revoke + Redis 삭제

### Invitation Flow

owner/admin만 초대 가능. 이메일 + role → invitation 생성 → accept 시 사용자 생성 + 멤버십 추가.
멱등성: 같은 이메일+조직에 이미 초대가 있으면 이전 초대 반환.

### Issue Update (낙관적 잠금)

`WHERE version = ?` + `RETURNING version`. 프로젝트 14, 17의 패턴 재사용.

## worker: Outbox → Notification

`Processor.RunOnce`:
1. outbox에서 미발행 이벤트 조회
2. 이벤트 타입에 따라 알림 수신자 결정 (`ListRecipients` — 해당 조직의 이벤트 발행자 제외 멤버)
3. `CreateNotification` — 수신자별 알림 INSERT
4. `MarkOutboxPublished`
5. 대시보드 캐시 무효화 (`cache.DeleteDashboardSummary`)

별도 `cmd/worker` 바이너리로 실행. API와 독립적으로 스케일 가능.

## httpapi: Server + 미들웨어

### appHandler 패턴

```go
type appHandler func(http.ResponseWriter, *http.Request) error
```

핸들러가 `error`를 반환하면 `wrap`이 `platform.WriteError`로 변환. 각 핸들러에서 반복적인 에러 처리 코드를 없앰.

### requireAuth 미들웨어

`Authorization: Bearer <jwt>` → `auth.ParseAccessToken` → `Principal{UserID, Email}`을 context에 주입.

### withObservability

요청 카운터 증가 + `X-Trace-ID` 주입 + 구조화 로깅.
