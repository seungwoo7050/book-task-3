# Timeline — C-authorization-lab 개발 과정 전체 기록

이 문서는 C-authorization-lab을 처음부터 끝까지 재현하는 데 필요한 모든 단계를 순서대로 기록한다.

---

## Phase 1: 프로젝트 초기 설정

A-auth-lab의 scaffold 구조를 그대로 가져와 시작했다.

```bash
mkdir -p labs/C-authorization-lab/spring
# build.gradle.kts, gradlew, Makefile, Dockerfile, compose.yaml 복사
```

동일한 기술 스택: Spring Boot 3.4.13, Java 21, Gradle Kotlin DSL, Spotless, Checkstyle.

```yaml
# application.yml 수정
app:
  summary: Authorization lab with invite lifecycle, RBAC, and ownership checks
```

---

## Phase 2: 인프라 구성

A랩과 동일한 Docker Compose 스택: PostgreSQL 16, Redis 7, Mailpit v1.24.
Flyway 마이그레이션도 동일한 `V1__init.sql` scaffold marker.

```bash
cp .env.example .env
docker compose up --build
docker compose down
```

---

## Phase 3: Authorization 도메인 구현

### 3-1. AuthorizationDemoService 작성

`authorization/application/AuthorizationDemoService.java`:

**데이터 모델 (인메모리):**
- `AtomicLong organizationSequence` — 조직 ID 자동 증가
- `AtomicLong invitationSequence` — 초대장 ID 자동 증가
- `ConcurrentHashMap<Long, Organization>` — 조직 저장소
- `ConcurrentHashMap<Long, Invitation>` — 초대장 저장소

**핵심 로직:**

1. `createOrganization(name, ownerEmail)`:
   - 새 조직 생성
   - 생성자를 `OWNER` 역할로 자동 추가
   - `Organization` record에 `Map<String, String> members` 포함

2. `invite(organizationId, email, role)`:
   - 조직 존재 확인
   - UUID 기반 초대 토큰 생성
   - 해당 이메일을 `PENDING` 상태로 멤버에 추가
   - `Invitation` record 반환

3. `accept(invitationId)`:
   - 초대장 존재 확인
   - `accepted: true`로 업데이트 (기존 invitation을 새 record로 교체 — immutable record 패턴)
   - 멤버 역할을 초대 시 지정한 역할로 전환 (PENDING → STAFF 등)
   - `Membership` record 반환

4. `changeRole(organizationId, email, role)`:
   - 조직, 멤버 존재 확인
   - 역할 변경
   - 현재는 OWNER 체크 없이 누구나 변경 가능 (의도적 simplification)

### 3-2. AuthorizationController 작성

`authorization/api/AuthorizationController.java`:

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/v1/organizations` | 조직 생성 |
| POST | `/api/v1/organizations/{id}/invites` | 초대 발행 |
| POST | `/api/v1/invitations/{id}/accept` | 초대 수락 |
| PATCH | `/api/v1/organizations/{id}/members/{email}/role` | 역할 변경 |

request body는 각각 `OrganizationRequest`, `InviteRequest`, `RoleRequest` record로 정의.

---

## Phase 4: 공통 인프라

A랩에서 가져온 공통 컴포넌트:
- `GlobalExceptionHandler` — RFC 7807 Problem Detail
- `TraceIdFilter` — MDC trace ID
- `LabInfoController`, `HealthController`, `OpenApiConfig`, `SecurityConfig`

---

## Phase 5: 테스트 작성과 검증

### 5-1. AuthorizationApiTest 핵심 시나리오

전체 invite → accept → role change 흐름:

1. `POST /api/v1/organizations` — "Store Ops" 조직 생성 (owner@example.com)
2. 응답에서 `organizationId` 추출
3. `POST /api/v1/organizations/{id}/invites` — staff@example.com을 STAFF로 초대
4. 응답에서 `invitationId` 추출
5. `POST /api/v1/invitations/{id}/accept` — 초대 수락 → role: STAFF 확인
6. `PATCH /api/v1/organizations/{id}/members/staff@example.com/role` — MANAGER로 변경 확인

### 5-2. 검증 명령어

```bash
make lint    # Spotless + Checkstyle
make test    # 전체 테스트 (AuthorizationApiTest 포함)
make smoke   # smoke test
```

---

## Phase 6: 수동 API 테스트

```bash
make run

# 1. 조직 생성
curl -X POST http://localhost:8080/api/v1/organizations \
  -H "Content-Type: application/json" \
  -d '{"name":"My Store","ownerEmail":"owner@example.com"}'
# → id 확인

# 2. 멤버 초대
curl -X POST http://localhost:8080/api/v1/organizations/1/invites \
  -H "Content-Type: application/json" \
  -d '{"email":"staff@example.com","role":"STAFF"}'
# → invitationId 확인

# 3. 초대 수락
curl -X POST http://localhost:8080/api/v1/invitations/1/accept
# → role: STAFF

# 4. 역할 변경
curl -X PATCH http://localhost:8080/api/v1/organizations/1/members/staff@example.com/role \
  -H "Content-Type: application/json" \
  -d '{"role":"MANAGER"}'
# → role: MANAGER

# Swagger UI
open http://localhost:8080/swagger-ui.html
```
