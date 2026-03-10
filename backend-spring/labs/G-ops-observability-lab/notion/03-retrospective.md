# Retrospective — 운영을 분리한 것의 가치와 한계

## 잘한 것: 운영을 별도 skill로 선언하기

가장 중요한 판단은 "운영은 별도 주제이다"라고 명시적으로 분리한 것이다. 다른 랩들에서 SecurityConfig, TraceIdFilter, HealthController가 `global/` 패키지에 조용히 들어가 있다. 이 코드들이 왜 거기 있는지, 각각 무슨 역할을 하는지를 설명하는 장소가 이 랩이다.

JSON logging과 trace ID를 "early concept"으로 도입한 것도 좋았다. capstone 프로젝트에서 로그를 분석해야 할 때, "왜 JSON이고 왜 traceId가 필요한가"를 이미 이해한 상태에서 시작할 수 있다.

Prometheus 컨테이너를 Compose에 포함시킨 것은 작지만 의미 있는 결정이다. `docker compose up` 한 번으로 메트릭 수집 파이프라인이 작동하는 것을 직접 볼 수 있다. "scrape"라는 개념이 코드가 아니라 설정으로 존재한다는 것, Prometheus가 pull 방식으로 메트릭을 가져간다는 것을 compose.yaml과 prometheus.yml로 보여준다.

CI와 Compose를 함께 보는 습관도 이 랩에서 정착되었다. 로컬에서 `docker compose up`으로 통합 환경을 띄우고, CI에서 같은 테스트가 자동으로 돌아간다. 이 연결이 "운영"의 출발점이다.

## 여전히 약한 것

### Alert rules의 부재

메트릭을 수집하지만 "어떤 값이 비정상인가"를 정의하지 않았다. Prometheus에서 `http_server_requests_seconds_count{status="500"}`가 급증해도 아무 알림이 오지 않는다. 메트릭 노출은 관측의 전제이지 관측 자체가 아니다.

### AWS는 문서 방향일 뿐

capstone의 deployment note에 ECS + RDS + ElastiCache 배포 방향이 기록되어 있지만, 이 랩 자체에는 AWS와 관련된 코드나 설정이 없다. `Dockerfile`과 `compose.yaml`이 컨테이너화를 증명하지만, 클라우드 배포와는 별개이다.

### Long-running production operation

서버가 몇 주 동안 돌아가면서 로그가 쌓이고, 메트릭이 변화하고, 디스크가 차는 — 이런 운영 경험은 학습 저장소에서 증명할 수 없다. 이 한계를 인식하는 것 자체가 중요하다.

## 다시 볼 것

1. **Prometheus alert rules 작성**: `config/alert-rules.yml`에 기본 규칙을 넣는다. HTTP 5xx rate > 1%, JVM heap > 80%, response latency p99 > 2s 정도의 예시. Alertmanager 설정까지 하면 Slack/email 통보 파이프라인이 완성된다.

2. **Grafana 대시보드 JSON**: `config/grafana/dashboard.json`에 JVM 메트릭과 HTTP 메트릭을 시각화하는 대시보드를 만들어둔다. Compose에 Grafana 서비스를 추가하고 auto-provisioning으로 연결한다.

3. **분산 트레이싱 도입**: OpenTelemetry SDK를 추가하고, Tempo나 Jaeger 컨테이너를 Compose에 넣는다. `TraceIdFilter`가 생성한 traceId를 W3C Trace Context 형식으로 전파하면 서비스 간 추적이 가능해진다.

4. **ECS 배포 자동화**: `capstone/commerce-backend-v2`의 deployment note를 기반으로, 실제 배포 스크립트나 CDK 코드를 작성한다. 학습 저장소라도 "한 번은 실제로 배포해봤다"는 것은 면접에서 큰 차이를 만든다.

