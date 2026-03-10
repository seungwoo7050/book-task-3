# 접근 기록: 운영 표면을 설계하기까지

## 처음 본 선택지들

운영성을 어떻게 끼워 넣을지 세 가지 방향이 있었다.

**1) Capstone 부속으로 운영 코드를 넣는다**
자연스러운 위치지만, 운영을 독립 학습 주제로 보기 어렵다.
"capstone에 health check 있어요"라는 수준이 된다.

**2) Prometheus + Grafana + alerting 풀 스택을 구축한다**
화려하지만, 랩 하나에 넣기에는 인프라 복잡도가 과하다.
학습 초점이 흐려진다.

**3) 최소 운영 표면을 독립 랩으로 분리한다**
health/live, health/ready, metrics, structured logging 네 가지만 집중한다.
각각이 답하는 질문이 명확하고, 면접에서 설명하기 좋다.

세 번째를 선택했다.

## 핵심 설계 결정

### Liveness vs Readiness 분리

`/health/live`는 프로세스 건강만 확인한다. DB 연결 실패여도 200이다.
Kubernetes의 livenessProbe에 대응한다.

`/health/ready`는 DB와 Redis를 실제로 ping한다.
의존성이 준비되지 않았으면 503 `DEPENDENCY_NOT_READY`를 반환한다.
Kubernetes의 readinessProbe에 대응한다.

이 분리가 왜 중요한지: liveness 실패 → 컨테이너를 재시작한다.
readiness 실패 → 트래픽을 빼되 컨테이너는 살려둔다.
둘을 한 엔드포인트로 합치면 의도하지 않은 재시작이 발생한다.

### MetricsRegistry와 미들웨어 카운터

Prometheus client library 없이 자체 카운터를 만들었다.
`MetricsRegistry`에 `request_count`를 두고,
미들웨어에서 모든 요청마다 `increment()`를 호출한다.

`/ops/metrics`는 Prometheus text exposition format으로 응답한다:
```
# HELP app_requests_total Total HTTP requests handled
# TYPE app_requests_total counter
app_requests_total 42
```

왜 직접 만들었는가: Prometheus client 라이브러리의 동작을 이해하기 위해
카운터 구조를 먼저 손으로 구현했다.
프로덕션에서는 `prometheus_client` 패키지를 쓰는 것이 맞다.

### JsonFormatter

Python의 `logging.Formatter`를 상속해서
`{timestamp, level, logger, message}` JSON을 출력한다.
`configure_logging()`에서 root logger의 핸들러를 교체한다.

왜 JSON인가: 로그 수집기(Fluentd, CloudWatch Logs, Datadog)가
줄 단위로 파싱할 수 있어야 하기 때문이다.
사람이 읽기엔 불편하지만, 기계가 읽기엔 필수다.

### AppError와 통일된 에러 응답

`AppError` exception class와 `register_exception_handlers`로
모든 에러를 `{error: {code, message, details}}` 형식으로 통일했다.
validation error, 예상치 못한 exception도 같은 포맷으로 잡는다.

이것은 ops 랩의 부산물이지만, 로그와 모니터링 관점에서
"에러 응답 포맷이 일관적이다"는 것이 운영 편의에 직결된다.

## 버린 아이디어

- Prometheus + Grafana 풀 스택은 범위 초과로 제외했다.
- AWS live deployment 요구는 학습 저장소가 계정/비용에 묶이므로 제외했다.
- alerting rule은 후속 확장 주제로 남겨 두었다.
