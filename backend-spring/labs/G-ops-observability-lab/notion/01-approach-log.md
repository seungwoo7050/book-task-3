# Approach Log — 운영을 독립 랩으로 분리한 판단

## 세 가지 선택지

운영 관련 내용을 어디에 어떻게 둘 것인가. 세 가지 방향이 있었다.

**첫 번째 길: capstone 부록으로 붙이기.** 가장 자연스럽다. 실제 서비스에서 운영 설정은 애플리케이션과 함께 존재하니까. 하지만 이렇게 하면 "운영은 나중에 한다"는 인식이 강화된다. health endpoint가 왜 필요한지, structured logging이 무슨 의미인지를 독립적으로 설명할 장소가 없어진다.

**두 번째 길: full observability stack을 한 랩에 넣기.** Prometheus + Grafana + Loki + Tempo. 서비스 메시 위에 distributed tracing까지. ECS에 배포하고 CloudWatch Logs로 연결. 풍부하지만 이 저장소의 범위를 완전히 벗어난다. 한 랩이 인프라 교과서가 되어버린다.

**세 번째 길: 운영 기본기만 분리해서 "이것은 별도 skill이다"를 선언하기.** health, logging, metrics, CI — 이 네 가지를 하나의 랩으로 묶고, alerting과 IaC는 next step으로 구분한다.

세 번째 길을 택했다.

## 선택한 설계 방향
### 도메인 없는 랩

다른 랩들에는 비즈니스 도메인이 있다. A-auth-lab에는 인증 flow가, D-data-jpa-lab에는 상품 엔티티가, F-cache-concurrency-lab에는 재고 시나리오가 있다. 하지만 ops lab에는 비즈니스 도메인이 없다. 대신 `OpsController`가 운영 엔드포인트들의 위치를 안내하는 역할을 한다.

```java
@GetMapping("/summary")
public Map<String, Object> summary() {
    return Map.of(
        "profile", activeProfile,
        "metrics", "/actuator/prometheus",
        "docs", "/swagger-ui.html",
        "health", "/api/v1/health/ready");
}
```

이 엔드포인트가 반환하는 것은 데이터가 아니라 **다른 엔드포인트의 위치**이다.

### Structured Logging + Trace ID

`logback-spring.xml`에서 `LogstashEncoder`로 JSON 로깅, `TraceIdFilter`에서 MDC 기반 traceId 주입. 응답 헤더 `X-Trace-Id`로 클라이언트에 반환한다.

### Prometheus 메트릭

Actuator + Micrometer가 `/actuator/prometheus`에서 메트릭을 노출하고, Compose의 Prometheus 컨테이너가 15초 간격으로 scrape한다.

### CI

GitHub Actions에서 test, lint, smoke를 PR 단위로 실행한다.

## 폐기한 아이디어들

- **Alerting + Dashboard를 core 범위에 포함시키기**: alert rules는 운영 환경마다 다르다
- **AWS live deploy 필수화**: 비용과 복잡도가 학습 범위를 넘는다

## 근거 자료

docs/README.md에서 현재 구현 범위를 확인했다. problem/README.md는 "Treat operations as a first-class backend skill"로 이 랩의 존재 이유를 정의하고 있다.

