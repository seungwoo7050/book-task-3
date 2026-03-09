# 지식 인덱스 — Workspace SaaS API에서 다룬 개념들

## Multi-Tenant Architecture

하나의 API가 여러 조직(tenant)을 서비스하는 구조. `organization_id`로 데이터를 격리. 모든 쿼리에 조직 ID 필터 적용. 이 프로젝트에서는 shared-schema 방식(하나의 DB, 조직별 행 분리).

## JWT Access Token + Opaque Refresh Token

Access token: 짧은 수명(15분), 서버에 상태 없음(stateless), HMAC-SHA256 서명.
Refresh token: 긴 수명(7일), 서버에 세션 저장(stateful), SHA256 해시로 저장.
둘을 조합해 보안(짧은 Access)과 UX(길게 유지되는 세션)를 모두 확보.

## Refresh Token Rotation

Refresh token 사용 시 이전 토큰을 즉시 무효화하고 새 토큰 발급. 토큰 탈취 시 정상 사용자와 공격자의 동시 사용을 감지 가능. `replaced_by`, `revoked_at` 필드로 세션 이력 추적.

## RBAC (Role-Based Access Control)

owner/admin/member 3단계 역할. 조직 생성자가 owner. admin은 초대 가능. member는 읽기/쓰기만. Membership 테이블에 user_id + organization_id + role로 관리.

## Invitation Flow

초대 토큰 기반 가입. owner/admin이 이메일로 초대 → 수신자가 토큰으로 가입 → 자동 멤버십 생성. 이미 등록된 사용자도 새 조직에 합류 가능. 멱등: 같은 이메일+조직에 중복 초대 방지.

## appHandler Pattern

`func(w, r) error` 시그니처의 핸들러. 에러를 명시적으로 반환하고, 미들웨어(wrap)에서 일괄 처리. 각 핸들러의 에러 처리 코드를 중앙화. Go 웹 프레임워크에서 흔히 사용되는 패턴.

## Platform Package (횡단 관심사)

Config(환경 변수), AppError(구조화 에러), Metrics(atomic 카운터), HTTP 유틸(WriteJSON, DecodeJSON)을 하나의 package에 모음. 도메인과 무관한 인프라 코드의 집합.

## Redis as Optional Dependency

Redis 장애 시에도 서비스가 동작하도록 설계. 세션: DB fallback. 대시보드 캐시: DB 직접 쿼리. readyz에서 Redis 상태 노출. "없으면 느리지만 죽지 않는" 선택적 의존.

## Outbox-Driven Notification

이슈 생성/변경 시 outbox 테이블에 이벤트 INSERT (트랜잭션 내). Worker가 폴링하여 조직 멤버들에게 알림 생성. 캐시 무효화도 함께 수행.

## Prometheus Text Format

```
workspace_requests_total 42
workspace_auth_logins_total 5
```

Counter 이름 + 공백 + 값. 한 줄에 하나의 메트릭. `Content-Type: text/plain; version=0.0.4`. 외부 라이브러리 없이 `atomic.Int64` + `fmt.Fprintf`로 구현 가능.

## Separate Binary (API + Worker)

같은 코드베이스에서 두 개의 `main`을 가진 구조. `cmd/api`는 HTTP 서버, `cmd/worker`는 outbox 폴러. 배포, 스케일링, 장애 격리를 독립적으로 관리 가능.

## contextKey Type

`type contextKey string` — context.WithValue에서 키 충돌을 방지하기 위한 타입 정의. 같은 문자열이라도 타입이 다르면 다른 키로 취급. Go context 사용의 모범 사례.

## OpenAPI Specification

`api/openapi.yaml`로 API 엔드포인트, 요청/응답 스키마, 인증 방식을 선언적으로 문서화. E2E 테스트와 smoke 테스트에서 실제 응답 필드를 이 스펙과 대조.
