# Timeline — 소스코드에서는 드러나지 않는 것들

## 프로젝트 초기화

이 랩은 다른 랩들과 동일한 scaffold 기반으로 시작했다. Spring Initializr에서 생성한 뒤, 공통 모듈(SecurityConfig, GlobalExceptionHandler, TraceIdFilter 등)을 `global/` 패키지에 배치하는 과정은 이미 익숙해진 상태였다.

```bash
# Gradle wrapper 확인 및 빌드 테스트
./gradlew --version    # Gradle 8.13
./gradlew build        # 초기 scaffold 컴파일 확인
```

`settings.gradle.kts`에서 프로젝트 이름을 `F-cache-concurrency-lab`으로 설정하고, `build.gradle.kts`에 `spring-boot-starter-data-redis` 의존성을 추가했다. 이 시점에서는 Redis를 실제로 사용할 계획이 있었다.

## Docker Compose 설정

```yaml
# compose.yaml — Redis 서비스 정의
services:
  postgres:
    image: postgres:16
    ports: ["5432:5432"]
  redis:
    image: redis:7
    ports: ["6379:6379"]
  mailpit:
    image: axllent/mailpit:v1.24
    ports: ["1025:1025", "8025:8025"]
```

PostgreSQL과 Redis, Mailpit을 함께 올리는 구성이다. 하지만 실제로 Redis에 연결하는 코드는 작성하지 않았다. `CacheConfig`에서 `ConcurrentMapCacheManager`를 `@Primary`로 등록하여 Redis auto-configuration을 우회했다.

```bash
docker compose up -d   # PostgreSQL + Redis + Mailpit 컨테이너 실행
docker compose ps      # 세 서비스 모두 running 확인
```

## Flyway 마이그레이션

이 랩은 JPA 엔티티가 없으므로 마이그레이션이 최소한이다.

```
src/main/resources/db/migration/
└── V1__init.sql       # 빈 마커 파일 — Flyway 초기화만 수행
```

다른 랩들(D-data-jpa-lab, E-event-messaging-lab)과 달리 V2 마이그레이션이 없다. 재고와 idempotency 데이터가 모두 ConcurrentHashMap에 저장되기 때문이다.

## CacheConfig 작성 과정

처음에는 `RedisCacheManager`를 설정하려 했으나, 테스트에서 Redis 컨테이너를 띄우는 복잡도를 고려하여 in-memory 캐시로 전환했다.

```java
@Configuration
public class CacheConfig {
    @Bean
    @Primary
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager("inventory-status");
    }
}
```

`@Primary`를 붙인 이유: `spring-boot-starter-data-redis`가 classpath에 있으면 Spring Boot가 자동으로 `RedisCacheManager`를 설정하려 한다. `@Primary`로 in-memory 구현이 우선되도록 했다.

## 테스트 작성과 실행

```bash
# 테스트 실행
./gradlew test

# 특정 테스트만 실행
./gradlew test --tests "*.CacheConcurrencyApiTest"
```

테스트는 `@SpringBootTest(webEnvironment = RANDOM_PORT)`로 실행된다. H2 in-memory DB를 사용하므로 PostgreSQL이 없어도 테스트가 통과한다.

테스트 시나리오:
1. SKU-1을 수량 2로 예약 (Idempotency-Key: reserve-1) → remaining: 8
2. 같은 키로 다시 예약 → remaining: 8 (멱등성 확인, 재고 추가 차감 없음)
3. GET /api/v1/inventory/SKU-1 → available: 8 (상태 확인)

```bash
# 전체 빌드 + lint + 테스트
make test      # ./gradlew test 래핑
make lint      # Spotless + Checkstyle
```

## Makefile 활용

```bash
make run       # docker compose up + bootRun (local 프로파일)
make test      # ./gradlew test
make lint      # Spotless 포맷 체크 + Checkstyle
make smoke     # 서버 기동 후 health check curl
```

로컬 개발 시에는 `make run`으로 Docker 컨테이너와 Spring Boot를 함께 실행한다. `SPRING_PROFILES_ACTIVE=local`이 자동 설정되어 H2가 아닌 PostgreSQL에 연결된다.

## Git 이력에서 주목할 커밋들

이 랩의 git 이력을 보면 다음과 같은 순서로 발전했을 것이다:

1. **scaffold 생성**: 공통 모듈 + build.gradle.kts + compose.yaml
2. **CacheConfig 추가**: in-memory CacheManager 등록
3. **서비스 구현**: CacheConcurrencyDemoService — inventory + idempotency + synchronized
4. **컨트롤러 추가**: POST /reservations + GET /{sku}
5. **테스트 작성**: idempotentReservationReturnsSameResult
6. **문서화**: docs/README.md에 simplification 범위 명시

## 아직 실행하지 않은 것들

```bash
# Redis CLI로 캐시 확인 — 현재 코드에서는 Redis를 사용하지 않으므로 의미 없음
# docker exec -it <redis-container> redis-cli
# KEYS *                    # 캐시 키 목록
# GET inventory-status::SKU-1  # 특정 SKU의 캐시 값

# Redisson 의존성 추가 — 아직 미구현
# implementation("org.redisson:redisson-spring-boot-starter:3.27.0")
```

이 명령어들은 Redis 캐시와 분산 락을 실제로 구현한 뒤에 의미가 있다. 현재의 in-memory 구현에서는 캐시 상태를 Redis CLI가 아닌 디버거나 로그로 확인해야 한다.
