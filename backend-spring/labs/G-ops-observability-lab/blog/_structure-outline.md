# G-ops-observability-lab structure outline

## 글 목표

- 이 lab을 "운영 다 된다"가 아니라 "운영 표면을 분리해 모아 둔 scaffold"로 다시 쓴다.
- custom health와 actuator health의 차이를 본문 중심으로 둔다.
- code-backed observability와 docs-only CI claims를 분리해 적는다.

## 글 순서

1. ops summary와 custom health surface가 무엇을 보여 주는지 먼저 정리한다.
2. trace header, JSON logs, Prometheus endpoint를 실제 runtime signal로 묶는다.
3. actuator health, compose wiring, CI file search 결과를 통해 현재 한계를 닫는다.

## 반드시 넣을 코드 앵커

- `OpsController.summary()`
- `HealthController.ready()`
- `TraceIdFilter.doFilterInternal()`
- `application.yml`의 actuator exposure
- `logback-spring.xml`
- `prometheus.yml`
- `compose.yaml`

## 반드시 넣을 검증 신호

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) -p 18086:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/labs/G-ops-observability-lab/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

## 반드시 남길 한계

- custom ready가 real dependency readiness를 대표하지 않는 점
- `/actuator/health`와 custom health 결과가 다를 수 있는 점
- CI가 현재 workspace에서는 workflow 파일로 확인되지 않는 점
