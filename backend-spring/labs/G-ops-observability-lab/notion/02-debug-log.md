# Debug Log — 키워드가 증명 범위보다 커 보이는 문제

## 장애 상황: "Observability Lab"이라는 이름의 무게

이 랩에는 런타임 장애가 없었다. `make test`도 통과하고 `make smoke`도 통과한다. 문제는 코드가 아니라 **기대치의 불일치**에 있었다.

"Ops & Observability Lab"이라는 이름을 보면 Prometheus 대시보드에서 알림이 울리고, 분산 트레이싱으로 마이크로서비스 간 호출을 추적하고, Terraform으로 인프라를 프로비저닝하는 장면을 떠올린다. 하지만 실제 구현은:

- JSON 로깅 (LogstashEncoder)
- Trace ID 주입 (MDC + UUID)
- Health endpoint 두 개 (live, ready)
- Actuator Prometheus endpoint 노출
- Prometheus 컨테이너 설정 (compose.yaml)
- OpsController의 summary endpoint

이것들은 모두 정당한 운영 기본기이다. 하지만 "observability"라는 단어가 암시하는 수준과는 거리가 있다.

## 잘못된 첫 번째 가정

"메트릭이 노출되고 로그가 구조화되면 observability가 충분하다"는 생각은 위험하다. Observability의 세 기둥(Three Pillars)은 **로그**(Logs), **메트릭**(Metrics), **트레이스**(Traces)이다. 이 랩에서 구현된 것은:

- **로그**: ✅ LogstashEncoder로 JSON 형식 출력, traceId 포함
- **메트릭**: ⚠️ Micrometer가 수집하고 Prometheus가 긁어가는 구조는 있지만, alert rules와 대시보드는 없다
- **트레이스**: ❌ MDC의 traceId는 단일 서버 내 추적이다. 서비스 간 분산 트레이싱(Zipkin, Jaeger, OpenTelemetry)은 없다

## 근본 원인

F-cache-concurrency-lab의 "캐시"와 같은 패턴이다. 이름과 실제 구현 depth 사이에 간극이 있고, 이 간극을 명시하지 않으면 면접에서 "observability 경험이 있습니다"라고 말한 뒤 구체적인 질문에 답하지 못하는 상황이 생긴다.

## 해결 과정

코드 변경이 아닌 문서 변경으로 대응했다. docs/README.md와 검증 문서에 세 가지를 구분했다:

1. **현재 증명된 것**: JSON structured logging, health endpoints, Prometheus scrape target 노출, CI 파이프라인
2. **구조는 있지만 활용은 미완인 것**: Prometheus 컨테이너는 있지만 alert rules/dashboard가 없다
3. **아직 없는 것**: 분산 트레이싱, 외부 로그 수집, IaC, AWS 배포 코드

```bash
make test    # OpsApiTest 통과
make lint    # Spotless + Checkstyle 통과
make smoke   # health check 통과
```

## 남은 부채

- `/actuator/prometheus`의 응답을 실제로 파싱하여 특정 메트릭(JVM 힙, HTTP 요청 카운트)이 존재하는지 검증하는 smoke test 추가
- Grafana 대시보드 JSON을 `config/` 디렉토리에 포함시켜 "이렇게 시각화할 수 있다"를 보여주기
- Alertmanager 설정 예시: CPU > 80%, 5xx rate > 1% 같은 기본 alert rules 작성
- distributed tracing: OpenTelemetry SDK 추가, Jaeger/Tempo 컨테이너 설정

