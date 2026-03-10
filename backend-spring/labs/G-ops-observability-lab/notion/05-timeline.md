# Timeline — 소스코드에서는 드러나지 않는 것들

## 프로젝트 초기화

이 랩은 다른 랩들과 동일한 scaffold 기반으로 시작했다. `global/` 패키지에 SecurityConfig, GlobalExceptionHandler, TraceIdFilter, HealthController, LabInfoController, OpenApiConfig, AppProperties가 배치된다.

```bash
./gradlew --version    # Gradle 8.13
./gradlew build        # 초기 scaffold 컴파일 확인
```

특이한 점은 이 랩에서 `global/` 패키지의 코드들이 **주인공**이라는 것이다. 다른 랩에서는 비즈니스 도메인(auth, data, cache 등)이 핵심이고 global은 지원 역할이지만, 여기서는 TraceIdFilter, HealthController, logback-spring.xml 같은 운영 설정이 랩의 본체이다.

## logback-spring.xml 작성

```xml
<configuration>
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
  </appender>
  <root level="INFO">
    <appender-ref ref="JSON"/>
  </root>
</configuration>
```

이 설정 파일 하나로 모든 로그 출력이 JSON 형식으로 바뀐다. `logstash-logback-encoder` 의존성이 `build.gradle.kts`에 포함되어 있어야 한다.

설정 후 확인:
```bash
./gradlew bootRun
# 콘솔에 JSON 형식 로그가 출력되는지 확인
# {"@timestamp":"...","level":"INFO","message":"Started Study2Application..."}
```

## Docker Compose 설정

이 랩의 compose.yaml은 다른 랩과 구별되는 서비스가 하나 있다: **Prometheus**.

```bash
docker compose up -d   # PostgreSQL + Redis + Mailpit + Prometheus + App

# 각 서비스 확인
docker compose ps
# postgres   → 5540:5432
# redis      → 6380:6379
# mailpit    → 1025:1025, 8125:8025
# prometheus → 9096:9090
# app        → 8100:8080
```

Prometheus UI는 `http://localhost:9096`에서 접근 가능하다. Targets 페이지에서 `study2-ops-lab` job이 `UP` 상태인지 확인한다.

## prometheus.yml 작성

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: study2-ops-lab
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ["app:8080"]
```

이 파일은 `spring/` 디렉토리 루트에 위치하며, compose.yaml에서 볼륨 마운트로 Prometheus 컨테이너에 전달된다.

## Actuator 설정

application.yml에서 Actuator endpoint를 선별적으로 노출한다:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      probes:
        enabled: true
  metrics:
    tags:
      application: ${APP_NAME:study2-lab}
```

`probes.enabled: true`는 `/actuator/health/liveness`와 `/actuator/health/readiness`를 활성화한다. `metrics.tags.application`은 모든 메트릭에 `application` 라벨을 추가하여 Prometheus에서 서비스별 필터링이 가능하게 한다.

```bash
# Actuator 엔드포인트 확인
curl localhost:8080/actuator/health
# {"status":"UP","groups":["liveness","readiness"]}

curl localhost:8080/actuator/prometheus | head -20
# jvm_memory_used_bytes{area="heap",...} 1.234567E8
# http_server_requests_seconds_count{...} 5.0
```

## 테스트 작성과 실행

```bash
./gradlew test
# OpsApiTest > summaryExposesOperationalLinks() PASSED
# HealthApiTest > ... PASSED
# LabInfoApiSmokeTest > ... PASSED
```

`OpsApiTest`는 `/api/v1/ops/summary`의 응답에서 `$.metrics`가 `/actuator/prometheus`이고 `$.health`가 `/api/v1/health/ready`인지 검증한다. 운영 엔드포인트의 "계약"을 테스트하는 것이다.

## Makefile 활용

```bash
make run       # docker compose up + bootRun
make test      # ./gradlew test
make lint      # Spotless + Checkstyle
make smoke     # 서버 기동 후 health check curl
```

`make smoke`는 서버가 기동된 상태에서 health endpoint를 curl로 호출한다. CI에서도 같은 명령어로 검증한다.

## Dockerfile: 멀티 스테이지 빌드

```dockerfile
FROM eclipse-temurin:21-jdk AS build
# ... 빌드

FROM eclipse-temurin:21-jre
COPY --from=build /workspace/build/libs/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

JDK로 빌드하고 JRE로 실행하는 멀티 스테이지 빌드이다. 최종 이미지에 컴파일러(javac)가 포함되지 않으므로 이미지 크기가 줄어든다. ECS나 쿠버네티스에 배포할 때 이 이미지를 그대로 사용한다.

## 아직 실행하지 않은 것들

```bash
# Grafana 대시보드 접근 — 아직 Grafana 서비스 미포함
# http://localhost:3000

# Prometheus alert rules 확인
# curl localhost:9090/api/v1/rules

# 분산 트레이싱 Jaeger UI
# http://localhost:16686

# AWS ECS 배포
# aws ecs update-service --cluster study2 --service ops-lab --force-new-deployment
```

이 명령어들은 next step에 해당한다.
