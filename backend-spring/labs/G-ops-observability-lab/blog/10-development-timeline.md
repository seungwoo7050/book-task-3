# G-ops-observability-lab: 운영 표면은 열려 있지만 그 의미는 아직 꽤 얇은 observability scaffold

`G-ops-observability-lab`은 운영성을 별도 주제로 떼어 냈다는 점에서 중요한 랩이지만, 실제 구현을 읽을 때는 "무엇이 진짜 signal인가"를 더 조심해서 봐야 했다. health, trace ID, JSON logs, Prometheus endpoint는 실제로 존재한다. 반면 readiness는 custom endpoint와 actuator health가 서로 다른 판단을 내리고, docs가 강조하는 CI는 workspace 안의 workflow 파일로는 확인되지 않았다. 즉 이 lab은 운영성을 배우기 위한 표면을 제공하지만, 그 표면이 모두 같은 깊이의 증거를 갖는 건 아니다.

2026-03-14에는 기존 blog를 입력 근거에서 제외하고, `OpsController`, `HealthController`, `TraceIdFilter`, `application.yml`, `logback-spring.xml`, `prometheus.yml`, `compose.yaml`, 테스트, 컨테이너 재실행 결과만으로 문서를 다시 썼다. 다시 보니 이 lab의 핵심 질문은 "운영 요소가 있다"보다 "그 운영 요소가 실제 상태를 얼마나 정확하게 말해 주는가"였다.

## Phase 1. summary와 custom health는 먼저 생겼지만, 둘 다 mostly static surface다

[`OpsController`](../spring/src/main/java/com/webpong/study2/app/ops/api/OpsController.java)는 `/api/v1/ops/summary`에서 운영 링크를 한 번에 보여 준다.

```java
return Map.of(
    "profile", activeProfile,
    "metrics", "/actuator/prometheus",
    "docs", "/swagger-ui.html",
    "health", "/api/v1/health/ready");
```

이건 유용한 출발점이지만, summary 자체는 runtime introspection이라기보다 static link directory에 가깝다. metrics path, docs path, health path를 문자열로 돌려줄 뿐, 그 endpoint들이 실제로 usable한지 검증하진 않는다.

custom health도 비슷하다. [`HealthController`](../spring/src/main/java/com/webpong/study2/app/global/api/HealthController.java)는 `/live`와 `/ready` 모두 단순히 `Map.of("status", "UP", ...)`를 반환한다.

```java
@GetMapping("/ready")
public Map<String, Object> ready() {
  return Map.of("status", "UP", "kind", "ready", "checkedAt", Instant.now().toString());
}
```

2026-03-14 수동 재검증에서도 `/api/v1/health/live`와 `/api/v1/health/ready`는 둘 다 `200 UP`이었다. 하지만 이 endpoint들은 datasource, Redis, mail, Prometheus readiness를 실제로 확인하지 않는다. ready의 의미가 "의존성이 준비됨"이 아니라 "이 컨트롤러가 지금 UP이라고 말한다"에 더 가깝다.

## Phase 2. actuator와 비교하면 custom ready의 한계가 더 분명해진다

이 lab의 더 흥미로운 부분은 actuator를 같이 켜 뒀다는 점이다. `application.yml`은 `management.endpoints.web.exposure.include: health,info,prometheus`와 `management.endpoint.health.probes.enabled: true`를 설정한다. 그래서 actuator health 계열 endpoint도 함께 살아 있다.

2026-03-14 수동 재검증 결과는 이랬다.

- `GET /api/v1/health/ready` -> `200 {"status":"UP","kind":"ready",...}`
- `GET /actuator/health/readiness` -> `200 {"status":"UP"}`
- `GET /actuator/health/liveness` -> `200 {"status":"UP"}`
- `GET /actuator/health` -> `503 {"status":"DOWN","groups":["liveness","readiness"]}`

즉 custom ready는 항상 `UP`이고, actuator readiness/liveness group도 `UP`이었지만, 전체 actuator health는 `DOWN`이었다. 이 차이는 꽤 중요하다. 현재 앱에는 "health endpoint가 있다"가 아니라 "서로 다른 기준의 health endpoint가 공존한다"가 더 정확하다.

부트 로그까지 같이 보면 원인도 어느 정도 드러난다. 같은 재실행에서 actuator는 `Mail health check failed`와 `Redis health check failed`를 남겼고, 각각 `localhost:1025`, `localhost:6379` 연결 거부가 찍혔다. 즉 custom ready는 외부 의존성을 보지 않지만, actuator 전체 health는 실제 연결 실패를 반영하고 있었다.

문서에서 readiness를 단일 개념처럼 적으면 이 미묘한 차이를 놓치기 쉽다. 지금 구현은 probe surface를 만드는 단계이지, 운영 판정을 하나로 수렴한 단계는 아니다.

## Phase 3. trace header와 JSON log는 실제로 붙어 있고, 이건 문서보다 런타임 근거가 강하다

반대로 더 확실한 운영 signal도 있다. [`TraceIdFilter`](../spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java)는 각 요청마다 UUID를 생성해 `MDC`에 넣고 `X-Trace-Id` response header로 돌려준다.

```java
String traceId = UUID.randomUUID().toString();
MDC.put("traceId", traceId);
response.setHeader("X-Trace-Id", traceId);
```

`logback-spring.xml`은 console appender를 `LogstashEncoder` 기반 JSON으로 고정한다.

```xml
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
  <encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
</appender>
```

이건 수동 `bootRun`에서도 바로 확인됐다. 부팅 로그와 shutdown 로그가 plain text가 아니라 JSON object 형태로 출력됐다. 그리고 `GET /api/v1/health/live`, `GET /api/v1/ops/summary`, `GET /actuator/prometheus` 응답에는 모두 `X-Trace-Id`가 붙었다. 즉 trace header와 structured logging은 이 lab에서 말뿐인 개념이 아니라 실제 runtime signal이다.

다만 여기서도 자동 검증과 manual 확인을 분리해 두는 편이 정확했다. 현재 `HealthApiTest`, `OpsApiTest`, `LabInfoApiSmokeTest`는 custom health/status와 ops summary 링크, lab metadata까지만 직접 잠근다. `X-Trace-Id` header 자체, JSON log payload shape, actuator 전체 health가 `DOWN`으로 보이는 차이는 MockMvc matcher가 아니라 source와 bootRun 재실행에서 더 직접적으로 확인한 사실이다.

## Phase 4. metrics endpoint와 Prometheus scrape 파일은 실제로 동작하지만, compose wiring은 다듬어지지 않았다

metrics 쪽도 코드 근거는 확실하다. `application.yml`이 Prometheus registry를 포함한 actuator exposure를 설정하고, `prometheus.yml`은 `app:8080`의 `/actuator/prometheus`를 scrape target으로 둔다.

```yaml
scrape_configs:
  - job_name: study2-ops-lab
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ["app:8080"]
```

수동 `GET /actuator/prometheus`는 실제로 `200 text/plain`과 함께 `application_ready_time_seconds`, `application_started_time_seconds`, `disk_free_bytes` 같은 metric을 반환했다. 이 부분은 확실히 살아 있다.

다만 compose wiring은 그대로 운영 설계라고 부르기엔 아직 투박하다. [`compose.yaml`](../spring/compose.yaml)에서 `app`은 `postgres`, `redis`, `mailpit`뿐 아니라 `prometheus`까지 `depends_on`으로 둔다. scrape consumer인 Prometheus를 app startup 선행조건처럼 둔 건 운영 의미상 자연스럽지 않다. 게다가 `postgres`의 기본 DB 이름은 `${POSTGRES_DB:-a_auth_lab}`로 남아 있어, 이 lab 이름과 맞지 않는 복사 흔적도 보인다.

즉 이 lab은 observability component를 소개하는 데는 성공했지만, compose contract 자체가 세밀하게 정리된 건 아니다.

## Phase 5. CI는 문제 정의와 docs에 있지만, 현재 workspace 파일 근거는 없다

문제 문서와 README, docs는 여러 번 "GitHub Actions"와 "CI hooks"를 언급한다. 하지만 2026-03-14에 `backend-spring` 아래 `.github/workflows`를 직접 찾았을 때 결과는 `0`개였다. 현재 workspace-local 코드 기준으로는 CI workflow 파일이 확인되지 않는다.

이건 문서를 비판하려는 뜻보다, 근거 수준을 분리하려는 뜻에 가깝다.

- health controller, trace filter, logback, Prometheus endpoint, prometheus.yml, compose.yaml: 실제 코드/설정 근거 있음
- GitHub Actions CI: 현재 이 workspace 안에서는 문서 주장과 실행 명령 수준의 근거만 있음

이 차이를 적어 두어야 "운영성 랩"이라는 이름이 과장되지 않는다.

## Phase 6. 이번 Todo는 lint/test/smoke 통과와 운영 의미의 차이를 같이 남겼다

이번 검증은 모두 2026-03-14에 다시 실행했다. 로컬 JRE가 없어서 host `make` 대신 `eclipse-temurin:21-jdk` 컨테이너를 사용했다.

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

세 명령 모두 `BUILD SUCCESSFUL`이었다. 이어서 `bootRun`을 18086 포트로 띄워 custom live/ready, actuator health/readiness/liveness, ops summary, `/actuator/prometheus`를 직접 확인했다. 이 재실행 덕분에 "health endpoint가 있다"보다 더 중요한 사실이 드러났다. 그 health endpoint들이 서로 같은 말을 하고 있지는 않다는 점이다.

이번 후속 보강에서는 그 차이를 더 노골적으로 적었다. 자동 테스트 기준으로는 이 lab이 아직 "ops link와 custom ready가 응답한다"를 보여 주는 단계이고, actuator/trace/logging 쪽 깊은 의미는 source와 수동 재실행이 채워 준다. 이 층위를 섞지 않아야 observability scaffold라는 현재 위치가 더 정확하게 보인다.

그래서 지금의 `G-ops-observability-lab`을 가장 정확하게 부르면 "운영 표면을 모아 둔 observability scaffold"다. structured logging, trace header, metrics endpoint, Prometheus scrape config는 실제로 있다. 반면 readiness semantics는 아직 얕고, compose wiring은 다듬어지지 않았으며, CI는 현재 workspace 기준으론 문서 주장에 더 가깝다. 이 경계를 분명히 적는 편이 capstone으로 넘어갈 때 훨씬 믿을 만한 기준선이 된다.
