# 디버그 기록 — 실 서비스 수준의 문제들

## Refresh Token Rotation — 동시 사용 감지

Refresh token을 탈취당한 경우: 공격자와 정상 사용자가 동시에 refresh를 시도하면?

1. 정상 사용자가 refresh → 새 세션 발급, 이전 세션 revoke
2. 공격자가 이전 refresh로 시도 → Redis에서 해시 불일치 → 실패

만약 공격자가 먼저 refresh에 성공하면? 정상 사용자의 다음 refresh에서 실패 → 로그인 화면으로 → 모든 세션 무효화를 유도.

이 "rotation detection" 패턴이 DB의 `replaced_by`, `revoked_at` 필드와 Redis 캐시를 같이 쓰는 이유다.

## Redis 장애 시 Graceful Degradation

Redis가 다운되면?
- **리프레시 세션**: Redis miss → PostgreSQL `refresh_sessions` 테이블로 fallback
- **대시보드 캐시**: Redis miss → DB에서 직접 집계 (`GetDashboardSummary`)
- **readyz**: Redis ping 실패 → readyz 실패 → 로드밸런서가 트래픽 차단

Redis는 "있으면 빠르고, 없어도 동작"하는 선택적 의존성으로 설계.

## bcrypt Cost와 응답 시간

`bcrypt.GenerateFromPassword(password, bcrypt.DefaultCost)` — DefaultCost는 10. 해싱에 ~100ms 소요. Register와 Login에서 이 시간이 응답에 추가된다.

Cost를 올리면 보안은 강해지지만 응답이 느려진다. 포트폴리오 프로젝트에서는 DefaultCost(10)로 충분.

## AppError 패턴의 이점

```go
func Errorf(status int, code, format string, args ...any) error {
    return &AppError{Status: status, Code: code, Message: fmt.Sprintf(format, args...)}
}
```

서비스에서 `platform.Errorf(404, "not_found", ...)`를 던지면, `wrap` 미들웨어가 상태 코드와 JSON 에러 본문을 자동으로 생성. 프로젝트 17에서의 `errors.Is` 기반 switch보다 훨씬 깔끔.

## Context에 Principal 넣기

```go
ctx := context.WithValue(r.Context(), principalContextKey, principal)
```

`contextKey` 타입을 string으로 정의해 키 충돌을 방지. `"workspace-principal"`이라는 값 자체보다 **타입**이 중요. 다른 패키지에서 같은 문자열을 쓰더라도 타입이 다르면 충돌하지 않음.

## 대시보드 캐시 무효화 타이밍

Worker가 outbox 이벤트를 처리한 후 `cache.DeleteDashboardSummary(orgID)` 호출. 이벤트가 발생한 조직의 캐시만 무효화. 다음 대시보드 요청 시 DB에서 재집계하고 캐시에 다시 저장.

TTL(30초)과 이벤트 기반 무효화를 병행: 이벤트 없이도 30초 후 자동 갱신.

## Worker의 알림 수신자 결정

`ListRecipients(orgID, excludeUserID)` — 이벤트를 발생시킨 사용자를 제외한 조직 멤버 전원에게 알림. "내가 만든 이슈에 대해 나한테 알림이 오면 안 된다."

## Migration 분리

`cmd/migrate` 바이너리로 SQL 마이그레이션을 실행. API 서버 시작 전에 `make migrate`로 스키마를 적용. 서버가 마이그레이션을 직접 실행하지 않음 — 여러 인스턴스가 동시에 마이그레이션을 실행하는 것을 방지.
