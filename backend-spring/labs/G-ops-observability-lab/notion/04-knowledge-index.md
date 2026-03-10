# Knowledge Index — 운영과 관측의 핵심 개념 사전

## 핵심 개념

### Health vs Readiness

**Liveness**(생존)와 **Readiness**(준비)는 다른 질문이다.

- **Liveness**: "이 프로세스가 살아있는가?" — JVM이 응답하는지 확인한다. 응답이 없으면 컨테이너를 재시작한다.
- **Readiness**: "이 프로세스가 트래픽을 받을 준비가 되었는가?" — DB 커넥션 풀이 초기화되었는지, 캐시가 워밍업되었는지 확인한다. 준비되지 않았으면 로드밸런서에서 제외한다.

이 랩의 `HealthController`는 `/api/v1/health/live`와 `/api/v1/health/ready` 두 엔드포인트를 제공한다. 현재는 둘 다 무조건 `UP`을 반환하지만, 실제 서비스에서는 readiness에 DB 연결 확인 등을 추가한다.

쿠버네티스에서는 이것을 `livenessProbe`와 `readinessProbe`로 설정한다. Spring Boot Actuator에서도 `management.endpoint.health.probes.enabled: true`로 같은 패턴을 지원한다.

### Structured JSON Logging

"사람이 읽기 좋은 로그"와 "기계가 처리하기 좋은 로그"는 다르다.

```
# 전통적인 로그 (사람용)
2025-01-15 10:23:45 INFO  OpsController - summary requested

# 구조적 로그 (기계용)
{"@timestamp":"2025-01-15T10:23:45.123Z","level":"INFO","logger_name":"OpsController","message":"summary requested","traceId":"a1b2c3d4"}
```

JSON 형식의 로그는:
- **필터링**: `jq '.level == "ERROR"'`로 에러만 추출
- **검색**: Elasticsearch에서 `traceId: a1b2c3d4`로 특정 요청의 전체 흐름 추적
- **집계**: CloudWatch Logs Insights에서 `stats count(*) by level` 같은 쿼리

이 랩에서는 `logback-spring.xml`에 `LogstashEncoder`를 설정하여 구현했다. Logstash 없이도 동작한다 — 이름이 `LogstashEncoder`인 이유는 ELK 스택의 Logstash가 기대하는 형식으로 출력하기 때문이다.

### Trace ID와 MDC

MDC(Mapped Diagnostic Context)는 SLF4J가 제공하는 스레드 로컬 컨텍스트이다. `MDC.put("traceId", value)`로 넣으면 같은 스레드에서 발생하는 모든 로그에 이 값이 자동으로 포함된다.

`TraceIdFilter`의 동작:
1. 요청 수신 → `UUID.randomUUID()` 생성
2. `MDC.put("traceId", traceId)` — 이후 모든 로그에 traceId가 포함됨
3. 응답 헤더 `X-Trace-Id: <traceId>` — 클라이언트에게도 전달
4. `finally`에서 `MDC.remove("traceId")` — 스레드 풀 오염 방지

서비스 간 추적(distributed tracing)에서는 이 traceId를 HTTP 헤더(`traceparent`, W3C Trace Context)로 다음 서비스에 전달한다. 현재 랩에서는 단일 서버 내 추적만 구현했다.

### Prometheus-style Metrics

Prometheus는 **pull 방식**의 메트릭 수집 시스템이다. 애플리케이션이 메트릭을 push하는 것이 아니라, Prometheus가 설정된 간격(이 랩에서는 15초)마다 `/actuator/prometheus`를 호출하여 메트릭을 가져간다.

주요 메트릭 타입:
- **Counter**: 단조 증가하는 값. HTTP 요청 수, 에러 수 (예: `http_server_requests_seconds_count`)
- **Gauge**: 올라갔다 내려갔다 하는 값. JVM 힙 사용량, 활성 스레드 수 (예: `jvm_memory_used_bytes`)
- **Histogram**: 분포를 측정하는 값. 응답 시간 분포 (예: `http_server_requests_seconds_bucket`)

Micrometer는 이 메트릭들을 수집하는 facade이고, `micrometer-registry-prometheus`가 Prometheus 형식으로 변환한다. `@Timed` 어노테이션으로 커스텀 메트릭을 추가할 수도 있다.

### Scrape Target

메트릭 수집기(Prometheus)가 주기적으로 읽어 가는 endpoint이다. `prometheus.yml`에서 target을 정의한다:

```yaml
scrape_configs:
  - job_name: study2-ops-lab
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ["app:8080"]
```

`targets`에 서비스 주소를 넣는다. 쿠버네티스에서는 Service Discovery로 자동 등록되고, ECS에서는 CloudMap이나 수동 설정을 사용한다.

### Observability의 세 기둥

완전한 observability는 세 가지 시그널의 조합이다:

| 기둥 | 질문 | 도구 | 이 랩에서의 상태 |
|------|------|------|----------------|
| Logs | "무슨 일이 일어났는가?" | ELK, CloudWatch | ✅ JSON + traceId |
| Metrics | "얼마나 자주, 얼마나 느린가?" | Prometheus, Grafana | ⚠️ 노출만, alert/dashboard 없음 |
| Traces | "어떤 경로를 거쳤는가?" | Jaeger, Tempo | ❌ 단일 서버 MDC만 |

## 참고 자료

| 출처 | 확인 내용 | 날짜 |
|------|----------|------|
| docs/README.md | 현재 구현 범위: JSON logging, health, Prometheus, CI | 작성 시점 |
| problem/README.md | "operations as a first-class backend skill" | 작성 시점 |
| Spring Boot Actuator Docs | management.endpoints 설정, health probes | 작성 시점 |
| Prometheus Docs | scrape_config, metric types, pull model | 작성 시점 |

