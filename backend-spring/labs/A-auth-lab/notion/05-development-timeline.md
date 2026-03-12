# Timeline — A-auth-lab 개발 과정 전체 기록

이 문서는 A-auth-lab을 처음부터 끝까지 재현하는 데 필요한 모든 단계를 순서대로 기록한다. 소스 코드를 읽으면 "무엇이 만들어졌는지"는 알 수 있지만, "어떤 순서로, 어떤 명령어를 써서, 왜 그렇게 만들었는지"는 알 수 없다. 이 문서가 그 빈자리를 채운다.

---

## Phase 1: 프로젝트 초기 설정

### 1-1. Spring Boot 프로젝트 생성

Spring Initializr 또는 기존 scaffold 템플릿에서 아래 의존성으로 프로젝트를 생성했다:

```
Spring Boot 3.4.13 / Java 21 / Gradle (Kotlin DSL)
```

핵심 의존성 목록 (`build.gradle.kts`):
- `spring-boot-starter-web` — REST API 서버
- `spring-boot-starter-security` — Spring Security 필터 체인
- `spring-boot-starter-data-jpa` — JPA (현재 scaffold에서는 H2 인메모리)
- `spring-boot-starter-data-redis` — Redis 연결
- `spring-boot-starter-mail` — 메일 발송 (Mailpit 연동 준비)
- `spring-boot-starter-validation` — Bean Validation
- `spring-boot-starter-actuator` — health check, metrics
- `spring-boot-starter-oauth2-client` — OAuth2 연동 준비 (B랩 대비)
- `flywaydb:flyway-core` + `flyway-database-postgresql` — DB 마이그레이션
- `springdoc-openapi-starter-webmvc-ui` — Swagger UI
- `querydsl-jpa` — QueryDSL (후속 랩 대비)
- `h2` (runtime) — 로컬 인메모리 DB
- `postgresql` (runtime) — Docker 프로필용 PostgreSQL 드라이버

```bash
# 프로젝트 디렉토리 구조 생성
mkdir -p labs/A-auth-lab/spring
cd labs/A-auth-lab/spring
```

### 1-2. Gradle Wrapper 설정

```bash
gradle wrapper --gradle-version 8.x
# gradlew, gradlew.bat, gradle/wrapper/ 생성됨
```

### 1-3. 코드 품질 도구 설정

**Spotless** (자동 포맷팅):
```bash
# build.gradle.kts에 spotless 플러그인 추가
# Google Java Format 적용, misc 파일 trailing whitespace 정리
```

**Checkstyle** (정적 분석):
```bash
mkdir -p config/checkstyle
# config/checkstyle/ 디렉토리에 checkstyle.xml 배치
# Checkstyle 10.17.0 사용
```

### 1-4. Makefile 작성

반복적으로 사용할 명령어를 Makefile에 등록했다:

```makefile
run:     SPRING_PROFILES_ACTIVE=local ./gradlew bootRun
lint:    ./gradlew spotlessCheck checkstyleMain checkstyleTest
test:    ./gradlew test
smoke:   ./gradlew test --tests '*SmokeTest'
```

---

## Phase 2: 인프라 구성 (Docker Compose)

### 2-1. compose.yaml 작성

로컬 개발 환경에 필요한 외부 서비스를 Docker Compose로 구성했다:

```bash
# compose.yaml 생성
# 서비스: app, postgres, redis, mailpit
```

**PostgreSQL 16**:
- DB: `a_auth_lab`, User: `study2`, Password: `study2`
- 호스트 포트: 5540 → 컨테이너 5432
- healthcheck으로 앱 서비스가 DB ready 후에 시작하도록 설정

**Redis 7**:
- 호스트 포트: 6380 → 컨테이너 6379
- 인증 없이 사용 (로컬 개발용)

**Mailpit v1.24**:
- SMTP: 1025, UI: 8125 → 컨테이너 8025
- 브라우저에서 `http://localhost:8125`로 메일 확인 가능

### 2-2. .env 파일 설정

```bash
cp .env.example .env
# SERVER_PORT, POSTGRES_*, REDIS_*, MAILPIT_* 환경변수 설정
```

### 2-3. Dockerfile (멀티스테이지 빌드)

```dockerfile
# Stage 1: eclipse-temurin:21-jdk로 빌드
#   ./gradlew bootJar --no-daemon
# Stage 2: eclipse-temurin:21-jre로 실행
#   java -jar /app/app.jar
```

### 2-4. Docker 환경 검증

```bash
docker compose up --build
# postgres healthcheck 대기 → app 기동 확인
# http://localhost:8100/api/v1/lab/info 접속하여 응답 확인
# http://localhost:8125 에서 Mailpit UI 접근 확인
docker compose down
```

---

## Phase 3: 데이터베이스 마이그레이션

### 3-1. Flyway 초기 마이그레이션

```bash
mkdir -p src/main/resources/db/migration
```

`V1__init.sql` — scaffold용 최소 마커 테이블:
```sql
create table if not exists study2_marker (
    id bigint primary key,
    context varchar(100) not null
);
```

이 테이블은 실제 비즈니스 로직에는 사용되지 않는다. Flyway가 정상 동작하는지 확인하는 용도이며, 이후 랩에서 실제 엔티티 테이블로 마이그레이션을 추가할 때의 기반이 된다.

**로컬 환경**에서는 H2 인메모리 DB(`jdbc:h2:mem:study2-lab;MODE=PostgreSQL`)가 Flyway를 실행한다.
**Docker 환경**에서는 PostgreSQL 16에 직접 적용된다.

---

## Phase 4: Spring Security 설정

### 4-1. SecurityConfig 작성

`SecurityConfig.java`에서 `SecurityFilterChain`을 구성했다:

- **CSRF disable**: Spring Security의 내장 CSRF 보호를 비활성화. 대신 애플리케이션 레벨에서 `X-CSRF-TOKEN` 헤더로 직접 검증한다.
- **모든 경로 permitAll**: 이 랩에서는 Spring Security의 인증/인가를 사용하지 않고, 애플리케이션 코드에서 직접 인증 로직을 구현한다. 이렇게 한 이유는 Spring Security의 자동 설정 뒤에 숨은 동작을 먼저 이해하기 위해서다.

### 4-2. application.yml 프로필 구성

- **기본 프로필**: H2 인메모리 DB, localhost Redis/Mail/Kafka
- **docker 프로필**: PostgreSQL 연결 (`spring.config.activate.on-profile: docker`)
- Actuator: health, info, prometheus 엔드포인트 노출
- JPA: `ddl-auto: validate` (Flyway가 스키마 관리)

---

## Phase 5: 인증 도메인 구현

### 5-1. AuthDemoService — 인메모리 인증 서비스

`auth/application/AuthDemoService.java` 작성:

- `ConcurrentHashMap<String, UserProfile> users` — 유저 저장소
- `ConcurrentHashMap<String, SessionSnapshot> sessions` — 세션 저장소
- `register()` — 이메일 중복 체크 후 유저 생성, verificationToken 발급
- `login()` — 비밀번호 검증 후 access/refresh/csrf 토큰 세트 발급
- `refresh()` — 기존 refresh token 폐기 + 새 토큰 세트 발급 (rotation)
- `logout()` — CSRF 검증 후 세션 제거
- `me()` — 이메일로 유저 프로필 조회

비밀번호 해싱은 `"bcrypt$" + password` 문자열 연결로 모델링했다. 실제 BCrypt를 돌리지 않은 이유는, 이 랩에서 검증하려는 대상이 "해싱 알고리즘"이 아니라 "인증 흐름의 구조"이기 때문이다.

### 5-2. AuthController — REST 엔드포인트

`auth/api/AuthController.java` 작성:

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/v1/auth/register` | 회원가입 |
| POST | `/api/v1/auth/login` | 로그인 (토큰 세트 발급) |
| POST | `/api/v1/auth/refresh` | 토큰 갱신 (X-CSRF-TOKEN 필수) |
| POST | `/api/v1/auth/logout` | 로그아웃 (X-CSRF-TOKEN 필수) |
| GET | `/api/v1/auth/me` | 프로필 조회 |

### 5-3. GlobalExceptionHandler — 에러 응답 표준화

`global/error/GlobalExceptionHandler.java` 작성:

- `IllegalArgumentException` → 400 Bad Request (RFC 7807 Problem Detail)
- `MethodArgumentNotValidException` → 400 + 필드별 에러 목록
- 모든 에러 응답에 `traceId` 포함 (MDC 기반)

---

## Phase 6: 공통 인프라

### 6-1. LabInfoController

`/api/v1/lab/info` — 앱 이름, 트랙, 요약 정보를 반환하는 엔드포인트. Smoke 테스트의 기본 대상이다.

### 6-2. HealthController

Actuator의 health endpoint와 별도로 커스텀 health check을 제공한다.

### 6-3. TraceIdFilter

모든 요청에 UUID 기반 traceId를 MDC에 설정. 로그와 에러 응답에서 요청을 추적할 수 있게 한다.

### 6-4. OpenApiConfig

SpringDoc 설정으로 Swagger UI (`/swagger-ui.html`)를 통해 API를 브라우저에서 테스트할 수 있다.

---

## Phase 7: 테스트 작성과 검증

### 7-1. 테스트 파일 구성

| 테스트 | 검증 대상 |
|--------|----------|
| `Study2ApplicationTests` | Spring context 로딩 |
| `HealthApiTest` | health 엔드포인트 응답 |
| `LabInfoApiSmokeTest` | `/api/v1/lab/info` 응답 (smoke) |
| `AuthFlowApiTest` | register→login→refresh 전체 흐름 + CSRF 불일치 거절 |

### 7-2. 테스트 실행

```bash
# 전체 테스트
make test
# 또는
./gradlew test

# smoke 테스트만
make smoke
# 또는
./gradlew test --tests '*SmokeTest'
```

### 7-3. 코드 품질 검증

```bash
# Spotless 포맷 체크
./gradlew spotlessCheck

# Checkstyle 정적 분석
./gradlew checkstyleMain checkstyleTest

# 한 번에 실행
make lint
```

포맷이 맞지 않으면 아래 명령으로 자동 수정:
```bash
./gradlew spotlessApply
```

---

## Phase 8: 수동 검증 (E2E)

### 8-1. 로컬 실행

```bash
# 로컬 프로필로 앱 실행 (H2 인메모리)
make run
# 또는
SPRING_PROFILES_ACTIVE=local ./gradlew bootRun
```

### 8-2. API 수동 테스트

```bash
# 1. 회원가입
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pw-1234"}'

# 2. 로그인
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pw-1234"}'
# → refreshToken, csrfToken 값을 메모

# 3. 토큰 갱신 (CSRF 헤더 필수)
curl -X POST http://localhost:8080/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: <위에서 받은 csrfToken>" \
  -d '{"refreshToken":"<위에서 받은 refreshToken>"}'

# 4. CSRF 불일치 테스트 (400 에러 예상)
curl -X POST http://localhost:8080/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: wrong-token" \
  -d '{"refreshToken":"<refreshToken>"}'

# 5. 프로필 조회
curl "http://localhost:8080/api/v1/auth/me?email=test@example.com"

# 6. 로그아웃
curl -X POST http://localhost:8080/api/v1/auth/logout \
  -H "Content-Type: application/json" \
  -H "X-CSRF-TOKEN: <csrfToken>" \
  -d '{"refreshToken":"<refreshToken>"}'
```

### 8-3. Swagger UI 확인

```
http://localhost:8080/swagger-ui.html
```

### 8-4. Docker Compose 전체 스택 검증

```bash
cp .env.example .env
docker compose up --build

# 앱 상태 확인
curl http://localhost:8100/api/v1/lab/info

# Mailpit UI
open http://localhost:8125

# 종료
docker compose down
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
