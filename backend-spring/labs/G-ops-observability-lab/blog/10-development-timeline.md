# G-ops-observability-lab: 운영성을 부록이 아니라 기본기로 분리한 과정

`G-ops-observability-lab`은 앞선 기능 랩들과 역할이 다르다. 인증, 인가, 데이터, 이벤트, 캐시를 만든 뒤에야 붙는 부록이 아니라, 앱이 스스로를 어떻게 설명하고 관찰 가능하게 만드는지를 따로 떼어 다루는 랩이다.

구현 순서는 세 단계로 읽힌다. `problem/README.md`에서 운영성을 독립 주제로 고정하고, `OpsApiTest`와 `HealthApiTest`로 health와 summary surface를 먼저 검증했다. 그다음 `TraceIdFilter`, `logback-spring.xml`, `application.yml`, `prometheus.yml`, `compose.yaml`로 trace, logs, metrics를 연결하고, 마지막에 docs와 검증 기록으로 아직 하지 않은 alert, dashboard, live infra를 정리했다.

## Phase 1. health와 summary surface를 먼저 고정했다

운영성을 별도 주제로 다루려면 가장 먼저 앱이 어디를 보면 되는지 스스로 말할 수 있어야 한다. [`OpsApiTest`](../spring/src/test/java/com/webpong/study2/app/OpsApiTest.java)와 [`HealthApiTest`](../spring/src/test/java/com/webpong/study2/app/HealthApiTest.java)가 바로 그 기준을 고정한다.

```java
mockMvc.perform(get("/api/v1/ops/summary"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.metrics").value("/actuator/prometheus"))
    .andExpect(jsonPath("$.health").value("/api/v1/health/ready"));

mockMvc.perform(get("/api/v1/health/ready"))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.status").value("UP"));
```

왜 이 코드가 중요했는가. 운영성의 첫걸음이 도구 목록이 아니라, 앱이 외부에 어떤 관찰 링크와 health 판단을 내놓는지라는 점을 이 테스트가 바로 보여 주기 때문이다.

CLI도 그래서 간단하다.

```bash
cd spring
make test
```

`2026-03-13` 테스트 XML 기준으로 `OpsApiTest` 1개 테스트와 `HealthApiTest` 2개 테스트가 모두 통과했다. summary surface와 liveness/readiness가 함께 baseline에 들어왔다는 뜻이다.

여기서 새로 선명해진 개념은 관찰 가능성의 최소 계약이었다. health와 summary 링크가 있어야 metrics나 logs도 따라 읽을 수 있다.

## Phase 2. trace id, JSON logging, metrics를 설정과 코드에 같이 묶었다

surface를 고정한 뒤에는 실제 관찰 신호를 어떤 형식으로 남길지가 중요해진다. [`TraceIdFilter`](../spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java)는 모든 요청에 `traceId`를 심고 응답 헤더 `X-Trace-Id`에도 같은 값을 실어 보낸다.

```java
String traceId = UUID.randomUUID().toString();
MDC.put("traceId", traceId);
response.setHeader("X-Trace-Id", traceId);
try {
  filterChain.doFilter(request, response);
} finally {
  MDC.remove("traceId");
}
```

로그 포맷은 [`logback-spring.xml`](../spring/src/main/resources/logback-spring.xml)에서 JSON으로 고정되고, [`application.yml`](../spring/src/main/resources/application.yml)은 actuator의 `health,info,prometheus` 노출을 설정한다. Prometheus는 [`prometheus.yml`](../spring/prometheus.yml)과 [`compose.yaml`](../spring/compose.yaml)로 함께 묶여 있다.

왜 이 코드와 설정이 중요했는가. observability가 "나중에 붙는 스택"이 아니라 app config, request correlation, log format이 한꺼번에 맞물리는 계약이라는 점을 여기서 비로소 설명할 수 있기 때문이다.

이 단계의 CLI는 smoke와 Compose가 핵심이다.

```bash
cd spring
make smoke
docker compose up --build
```

`docs/verification-report.md`는 `2026-03-09`에 lint, test, smoke, Compose health 확인이 모두 통과했다고 적고 있다. `LabInfoApiSmokeTest` XML도 1개 테스트가 실패 없이 끝났다.

여기서 배운 건 trace id와 JSON logging의 관계였다. 둘 중 하나만 있어서는 같은 요청을 이어 보기 어렵고, 같이 있어야 운영 surface가 된다.

## Phase 3. 운영 완성본이 아니라 baseline이라는 점을 문서로 닫았다

이 랩이 health와 metrics를 갖췄다고 해서 alert, dashboard, live cloud deployment까지 끝난 건 아니다. [`docs/README.md`](../docs/README.md)는 alert rule, dashboard, 외부 log platform, live AWS가 아직 비어 있다고 분명히 적는다.

```bash
cd spring
make lint
make test
make smoke
```

검증 신호는 아래처럼 정리된다.

- `2026-03-13` 기준 테스트 XML 4개 suite, 총 5개 테스트, 실패 0
- `2026-03-09` 검증 보고서 기준 lint, test, smoke, Compose health 확인 통과
- docs에 alert/dashboard/live AWS가 아직 미완이라고 명시돼 있음

이 랩이 남긴 핵심은 "무엇이 보이는가"와 "무엇은 아직 보이지 않는가"를 함께 적는 태도였다. 그 경계가 분명하기 때문에, 이 운영 baseline을 실제 도메인으로 옮길 때도 과장 없이 설명할 수 있다. 다음 프로젝트인 `commerce-backend`가 바로 그 첫 통합 실험이다.
