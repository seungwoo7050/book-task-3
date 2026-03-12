# Timeline — B-federation-security-lab 개발 과정 전체 기록

이 문서는 B-federation-security-lab을 처음부터 끝까지 재현하는 데 필요한 모든 단계를 순서대로 기록한다.

---

## Phase 1: 프로젝트 초기 설정

### 1-1. A-auth-lab scaffold 기반 확장

B 랩은 A-auth-lab의 Spring workspace scaffold를 기반으로 시작했다. 동일한 build.gradle.kts, Makefile, Dockerfile, compose.yaml 구조를 공유한다.

```bash
# A-auth-lab scaffold를 복사하여 B 랩 디렉토리 구성
mkdir -p labs/B-federation-security-lab/spring
# build.gradle.kts, gradlew, Makefile, Dockerfile, compose.yaml 등 복사
```

핵심 의존성은 A랩과 동일하다:
- Spring Boot 3.4.13 / Java 21 / Gradle (Kotlin DSL)
- `spring-boot-starter-security`, `spring-boot-starter-oauth2-client` — OAuth2 연동 기반
- `spring-boot-starter-data-redis` — 향후 rate limiting 백엔드
- Flyway, H2, PostgreSQL, Spotless, Checkstyle

### 1-2. application.yml 수정

```yaml
app:
  summary: Federation and second-factor security lab with audit-friendly flows
```

A랩과의 차이는 거의 summary 뿐이다. DB, Redis, Mail 설정은 동일한 구조를 유지한다.

---

## Phase 2: 인프라 구성

### 2-1. Docker Compose

A랩과 동일한 서비스 구성: PostgreSQL 16, Redis 7, Mailpit v1.24

```bash
cp .env.example .env
docker compose up --build
```

### 2-2. Flyway 마이그레이션

A랩과 동일한 `V1__init.sql` (scaffold marker table).

---

## Phase 3: Federation 도메인 구현

### 3-1. FederationSecurityDemoService 작성

`federation/application/FederationSecurityDemoService.java`:

**Google OAuth2 시뮬레이션:**
- `authorize()` — Google authorize URL 생성 (state, nonce 포함). 실제 Google API를 호출하지 않고 URL 형태만 생성한다.
- `callback()` — email과 provider subject를 받아 `linkedIdentities`에 매핑. 실제 OAuth2 흐름에서는 authorization code를 access token으로 교환하는 단계가 있지만, 이 scaffold에서는 생략했다.

**2FA (TOTP) 흐름:**
- `setupTotp()` — UUID 기반 secret 생성, recovery code 3개 발급, 예상 검증 코드 반환
- `verifyTotp()` — 제출된 코드와 저장된 기댓값 비교

**Audit Logging:**
- 모든 주요 메서드에서 `auditEvents.add(new AuditEvent(...))` 호출
- `auditEvents()` — 기록된 이벤트 목록 반환 (불변 복사본)

저장소:
- `ConcurrentHashMap<String, String> linkedIdentities` — email → provider subject
- `ConcurrentHashMap<String, String> totpSecrets` — email → expected TOTP code
- `ArrayList<AuditEvent> auditEvents` — audit 이벤트 목록

### 3-2. FederationSecurityController 작성

`federation/api/FederationSecurityController.java`:

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/v1/auth/google/authorize` | Google OAuth2 authorize URL 생성 |
| POST | `/api/v1/auth/google/callback` | Google callback 수신 (identity linking) |
| POST | `/api/v1/auth/2fa/setup` | TOTP 설정 (secret + recovery codes) |
| POST | `/api/v1/auth/2fa/verify` | TOTP 코드 검증 |
| GET | `/api/v1/audit-events` | audit event 목록 조회 |

### 3-3. SecurityConfig

A랩과 동일한 구성: CSRF disable, 모든 경로 permitAll. 이 랩에서도 Spring Security의 자동 인증/인가를 사용하지 않고 애플리케이션 레벨에서 직접 흐름을 구현한다.

---

## Phase 4: 공통 인프라

A랩에서 가져온 공통 컴포넌트:
- `GlobalExceptionHandler` — RFC 7807 Problem Detail 기반 에러 응답
- `TraceIdFilter` — MDC 기반 trace ID
- `LabInfoController` — `/api/v1/lab/info` 엔드포인트
- `HealthController` — health check
- `OpenApiConfig` — Swagger UI

---

## Phase 5: 테스트 작성과 검증

### 5-1. 테스트 파일 구성

| 테스트 | 검증 대상 |
|--------|----------|
| `Study2ApplicationTests` | Spring context 로딩 |
| `HealthApiTest` | health 엔드포인트 |
| `LabInfoApiSmokeTest` | smoke test |
| `FederationSecurityApiTest` | Google callback + audit, TOTP setup + verify |

### 5-2. FederationSecurityApiTest 핵심 시나리오

**Google callback + audit 흐름:**
1. `GET /api/v1/auth/google/authorize` → URL에 "google" 포함 확인
2. `POST /api/v1/auth/google/callback` → provider "google" 확인
3. `GET /api/v1/audit-events` → 이벤트 기록 존재 확인

**TOTP setup + verify 흐름:**
1. `POST /api/v1/auth/2fa/setup` → recovery codes 존재 확인
2. 응답에서 `expectedCode` 추출
3. `POST /api/v1/auth/2fa/verify` → `verified: true` 확인

### 5-3. 검증 명령어

```bash
make lint    # Spotless + Checkstyle
make test    # 전체 테스트
make smoke   # smoke test만

# Docker 환경 전체 검증
docker compose up --build
curl http://localhost:8100/api/v1/lab/info
docker compose down
```

---

## Phase 6: 수동 API 테스트

```bash
# 로컬 실행
make run

# Google OAuth2 시뮬레이션
curl http://localhost:8080/api/v1/auth/google/authorize
# → authorize URL 반환

curl -X POST http://localhost:8080/api/v1/auth/google/callback \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","subject":"google-sub-123"}'

# 2FA 설정
curl -X POST http://localhost:8080/api/v1/auth/2fa/setup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
# → secret, recoveryCodes, expectedCode 반환

# 2FA 검증
curl -X POST http://localhost:8080/api/v1/auth/2fa/verify \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","code":"<expectedCode>"}'

# Audit 이벤트 확인
curl http://localhost:8080/api/v1/audit-events

# Swagger UI
open http://localhost:8080/swagger-ui.html
```

---

## 환경별 포트 정리

| 서비스 | 로컬 실행 | Docker Compose |
|--------|----------|---------------|
| App | 8080 | 8100 |
| PostgreSQL | - (H2 사용) | 5540 |
| Redis | 6379 | 6380 |
| Mailpit SMTP | 1025 | 1025 |
| Mailpit UI | - | 8125 |
