# Problem Framing — 운영은 배포 이후의 문제가 아니다

## 이 랩이 존재하는 이유

백엔드 개발자 면접에서 "운영 경험이 있으신가요?"라는 질문은 AWS 콘솔을 얼마나 다뤄봤느냐를 묻는 것이 아니다. 서비스가 돌아가는 동안 **무엇을 볼 수 있는지**(observability), **어떻게 배포되는지**(delivery), **문제가 생겼을 때 어떤 정보가 남는지**(structured logging)를 묻는 것이다.

이 랩은 그 기본기를 별도 주제로 분리했다. 다른 랩들(A-auth, D-data-jpa, F-cache 등)에는 비즈니스 도메인이 있고, 운영 설정은 `global/` 패키지에 조용히 들어가 있다. 하지만 그 조용한 설정들 — TraceIdFilter, HealthController, logback-spring.xml, actuator 노출, Prometheus 설정 — 이 왜 거기 있는지, 무엇을 위한 것인지를 명시적으로 설명하는 장소가 필요했다.

## 이 랩이 다루는 것

### JSON 구조적 로깅 + Trace ID

`logback-spring.xml`에서 `LogstashEncoder`를 사용하여 모든 로그를 JSON 형식으로 출력한다. `TraceIdFilter`는 매 요청마다 UUID를 생성하여 MDC에 `traceId`로 넣고, 응답 헤더에 `X-Trace-Id`로 반환한다. 로그 한 줄에 traceId가 포함되므로, 하나의 요청이 어떤 경로를 거쳤는지 추적할 수 있다.

### Health Endpoints

`HealthController`는 `/api/v1/health/live`와 `/api/v1/health/ready` 두 엔드포인트를 제공한다. 쿠버네티스의 livenessProbe/readinessProbe에 대응하는 패턴이다. Actuator의 `/actuator/health`도 함께 노출되어 있다.

### Prometheus 메트릭 노출

`application.yml`에서 `management.endpoints.web.exposure.include: health,info,prometheus`로 설정했다. Micrometer가 JVM 메트릭, HTTP 요청 통계 등을 수집하고, `/actuator/prometheus`에서 Prometheus가 긁어갈 수 있는 형식으로 노출한다.

### Prometheus 컨테이너

`compose.yaml`에 `prom/prometheus:v3.4.1` 서비스를 포함했다. `prometheus.yml`에서 15초 간격으로 `app:8080/actuator/prometheus`를 scrape하도록 설정했다. Docker Compose를 올리면 Spring Boot 앱과 Prometheus가 함께 떠서 메트릭 수집이 바로 시작된다.

### Ops Summary 엔드포인트

`OpsController`는 `/api/v1/ops/summary`에서 현재 프로파일, 메트릭 경로, swagger 경로, health 경로를 JSON으로 반환한다. 운영 관련 엔드포인트들의 "안내 데스크" 역할이다.

### CI 워크플로우

GitHub Actions에서 `./gradlew test`, lint, smoke 등을 실행하는 워크플로우가 설정되어 있다. 코드 품질과 운영 설정이 PR 단위로 검증된다.

## 이 랩이 다루지 않는 것

| 미포함 항목 | 이유 |
|------------|------|
| Alert rules | Prometheus alerting rules 작성은 운영 환경에 따라 매우 다르다. 학습 범위를 넘는다 |
| Grafana 대시보드 | 메트릭 시각화는 중요하지만 scaffold 단계에서는 "노출"까지만 증명한다 |
| 외부 로그 수집 (ELK, CloudWatch) | JSON 로깅은 준비되었지만 실제 수집 파이프라인은 인프라 의존적이다 |
| IaC (Terraform, CDK) | AWS 배포는 docs에 방향만 기록했다. 실제 코드는 아직 없다 |
| 분산 트레이싱 (Zipkin, Jaeger) | MDC traceId는 단일 서버 내 추적이다. 서비스 간 추적은 다음 단계 |

## 기술 스택

| 구성 요소 | 선택 |
|----------|------|
| 런타임 | Java 21, Spring Boot 3.4.x |
| 로깅 | Logback + LogstashEncoder (JSON) |
| 메트릭 | Micrometer + micrometer-registry-prometheus |
| Health | Spring Boot Actuator + 커스텀 HealthController |
| 모니터링 | Prometheus v3.4.1 (compose.yaml 내) |
| 컨테이너 | Docker multi-stage (temurin:21), Docker Compose |
| CI | GitHub Actions |
| DB | H2 in-memory (기본), PostgreSQL 16 (docker 프로파일) |

## 성공 기준

- `make test` — OpsApiTest가 `/api/v1/ops/summary`의 응답을 검증한다
- `make smoke` — health check가 통과한다
- `/actuator/prometheus` — Prometheus 형식의 메트릭이 반환된다
- `docker compose up` — Spring Boot + PostgreSQL + Redis + Prometheus가 함께 기동된다
- 아직 미완인 것(alerting, IaC, 외부 로그 수집)을 문서에 숨기지 않는다

## 불확실한 것들

이 랩만으로 "운영 역량이 있다"고 말하기는 어렵다. 하지만 백엔드 채용에서는 structured logging, health endpoint, 메트릭 노출이라는 **기본 언어를 말할 수 있는지**가 첫 번째 관문이다. 이 랩은 그 관문을 통과하기 위한 최소 장비이다.

