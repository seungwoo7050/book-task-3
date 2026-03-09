# 지식 인덱스: 운영성(Operability) 패턴 정리

## Liveness vs Readiness

| 항목 | Liveness | Readiness |
|------|----------|-----------|
| 질문 | 프로세스가 살아있는가? | 요청을 받을 준비가 되었는가? |
| 실패 시 | 컨테이너 재시작 | 트래픽 제거 (재시작 안 함) |
| 비용 | 낮아야 함 (외부 호출 X) | 의존성 점검 포함 가능 |
| K8s probe | livenessProbe | readinessProbe |
| 이 랩에서 | `/health/live` → 무조건 200 | `/health/ready` → DB ping + Redis ping |

**핵심**: 둘을 합치면 DB 장애 시 컨테이너가 재시작된다.
재시작해도 DB는 여전히 죽어있으므로 무한 재시작 루프에 빠진다.

## Structured Logging

```python
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        })
```

왜 JSON인가:
- CloudWatch Logs, Datadog, Fluentd가 자동 파싱 가능
- grep이 아니라 structured query로 로그를 검색 가능
- 필드 추가가 포맷 변경 없이 가능

사람이 개발 중에 읽기엔 불편하므로,
`environment == "development"`일 때만 plain text formatter를 쓰는 분기도 가능하다.

## Prometheus Text Exposition Format

```
# HELP app_requests_total Total HTTP requests handled
# TYPE app_requests_total counter
app_requests_total 42
```

규약:
- `# HELP`: 메트릭 설명
- `# TYPE`: counter, gauge, histogram, summary
- `metric_name value`: 공백 구분

이 랩에서는 자체 MetricsRegistry로 counter만 구현했다.
프로덕션에서는 `prometheus_client` 패키지의 `Counter`, `Histogram` 등을 사용한다.

## AppError 통일 에러 포맷

```json
{
  "error": {
    "code": "DEPENDENCY_NOT_READY",
    "message": "Database or Redis is not ready.",
    "details": {}
  }
}
```

모든 에러 응답이 동일한 구조를 따르면:
- 프론트엔드가 에러 처리 로직을 일관되게 작성할 수 있다
- 로그 수집 시 에러 코드로 분류/집계가 가능하다
- validation error도 같은 형식에 들어가므로 API 소비자가 예측 가능하다

## Compose Healthcheck 설계

```yaml
healthcheck:
  test: ["CMD-SHELL", "python -c \"import urllib.request; ...\"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 15s
```

| 파라미터 | 의미 |
|----------|------|
| interval | probe 사이 간격 |
| timeout | 한 probe의 최대 대기 시간 |
| retries | 연속 실패 몇 번이면 unhealthy |
| start_period | 최초 probe 시작 전 유예 시간 |

Python slim 이미지에서 curl이 없을 수 있으므로
`urllib.request`로 probe하면 추가 설치 없이 동작한다.

## Smoke Test 패턴

```python
# tests/smoke.py — make smoke으로 실행
def main():
    os.environ["DATABASE_URL"] = "sqlite:///tmp/test.db"
    with TestClient(create_app()) as client:
        client.get("/api/v1/health/live").raise_for_status()
```

unit test와의 차이:
- smoke test는 "앱이 뜨고 기본 응답을 하는가"만 확인
- 의존성을 최소화(SQLite, Redis 없음)
- CI에서 compose 없이 빠르게 돌릴 수 있다

## 용어 정리

| 용어 | 의미 |
|------|------|
| liveness | 프로세스 생존 여부 |
| readiness | 요청 처리 가능 여부 (의존성 포함) |
| probe | 특정 상태를 자동으로 검사하는 요청 |
| structured logging | 기계가 파싱 가능한 형식의 로그 |
| text exposition | Prometheus가 정의한 메트릭 텍스트 포맷 |
| smoke test | 최소 기능 존재 검증 |

## 참고 자료

| 제목 | 출처 | 확인 | 비고 |
|------|------|------|------|
| Configure Liveness, Readiness Probes | kubernetes.io | 2025-01 | K8s 공식 문서 |
| Prometheus Exposition Formats | prometheus.io | 2025-01 | text format 규약 |
| 12-Factor App - Logs | 12factor.net | 2025-01 | 이벤트 스트림으로서의 로그 |
