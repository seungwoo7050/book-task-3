# G-ops-observability-lab evidence ledger

- 작성 기준일: 2026-03-14
- 복원 원칙: 기존 blog 본문은 입력 근거로 쓰지 않고, source, config, tests, 재실행 결과만 사용했다.
- 핵심 근거: `problem/README.md`, `docs/README.md`, `spring/Makefile`, `OpsController.java`, `HealthController.java`, `TraceIdFilter.java`, `application.yml`, `logback-spring.xml`, `prometheus.yml`, `compose.yaml`, `OpsApiTest.java`, `HealthApiTest.java`, `LabInfoApiSmokeTest.java`

## Phase 1. 운영 표면과 테스트 기준 확인

- 목표: 이 lab이 실제로 어떤 운영 표면을 노출하는지 먼저 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/ops/api/OpsController.java`
  - `spring/src/main/java/com/webpong/study2/app/global/api/HealthController.java`
  - `spring/src/test/java/com/webpong/study2/app/OpsApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
- 확인 결과:
  - `/api/v1/ops/summary`는 static link map에 가깝다.
  - custom `/api/v1/health/live|ready`는 dependency probe 없이 항상 `UP`을 반환한다.
  - 테스트는 링크 문자열과 `UP` 상태만 확인한다.
  - `X-Trace-Id`, JSON logging, actuator health divergence는 여기서 직접 matcher로 잠그지 않는다.

## Phase 2. logging/metrics/runtime signal 확인

- 목표: observability 요소 중 실제 runtime signal이 무엇인지 확인한다.
- 확인 파일:
  - `spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java`
  - `spring/src/main/resources/logback-spring.xml`
  - `spring/src/main/resources/application.yml`
  - `spring/prometheus.yml`
- 확인 결과:
  - `X-Trace-Id` response header가 실제로 붙는다.
  - bootRun 로그가 JSON 형태로 출력된다.
  - `/actuator/prometheus`는 실제 metric payload를 반환한다.
  - 위 세 항목은 현재 source와 manual bootRun 재실행이 더 직접적인 근거이고, MockMvc test가 같은 수준으로 잠그는 것은 아니다.

## Phase 3. compose/CI 근거 차이 확인

- 목표: 문서가 말하는 운영 기본기 중 무엇이 파일로 존재하고 무엇이 아직 문서 주장인지 분리한다.
- 확인 파일:
  - `spring/compose.yaml`
  - `spring/prometheus.yml`
- 확인 결과:
  - compose와 Prometheus scrape 파일은 실제로 있다.
  - `app`이 `prometheus`에 `depends_on`을 거는 등 wiring이 아직 투박하다.
  - `POSTGRES_DB:-a_auth_lab` 기본값은 이 lab 맥락과 맞지 않는 복사 흔적이다.
  - `backend-spring` 아래 `.github/workflows` 검색 결과는 `0`개였다.

## Phase 4. 2026-03-14 재실행 검증

- lint:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
```

- 결과: `BUILD SUCCESSFUL in 1m 39s`

- test:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'
```

- 결과: `BUILD SUCCESSFUL in 1m 24s`

- smoke:

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test --tests "*SmokeTest"'
```

- 결과: `BUILD SUCCESSFUL in 1m 19s`

- manual boot run:

```bash
docker run --rm -u $(id -u):$(id -g) -p 18086:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

- manual HTTP checks:
  - `GET /api/v1/health/live` -> `200`, `X-Trace-Id` 포함
  - `GET /api/v1/health/ready` -> `200`, custom `UP`
  - `GET /api/v1/ops/summary` -> `profile`, `metrics`, `docs`, `health` 링크 반환
  - `GET /actuator/prometheus` -> `200`, metrics payload 반환
  - `GET /actuator/health/readiness` -> `200 {"status":"UP"}`
  - `GET /actuator/health/liveness` -> `200 {"status":"UP"}`
  - `GET /actuator/health` -> `503 {"status":"DOWN","groups":["liveness","readiness"]}`
  - bootRun log -> `Mail health check failed`, `Redis health check failed`, both `Connection refused` on localhost defaults

## 이번 Todo의 결론

- 이 lab은 observability surface를 모아 두는 데는 성공했지만, 모든 surface가 같은 깊이의 운영 의미를 갖는 건 아니다.
- 문서에 반드시 남겨야 할 현재 한계:
  - custom ready와 actuator health 사이의 의미 차이
  - automated test coverage는 custom health/ops summary 쪽에 더 가깝고, trace/logging/actuator 차이는 source/manual 관찰에 더 의존한다는 점
  - compose wiring의 미세한 어색함
  - workspace-local CI workflow 파일 부재
