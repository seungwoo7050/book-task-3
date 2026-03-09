# 운영성은 기능이다: Health, Logging, Metrics를 독립 랩으로 만든 이유

## 왜 이 문제를 만들었는가

기능을 다 만들어 놓고 "배포는 나중에"라고 미루면,
서비스가 살아있는지, 요청을 처리하고 있는지, 어디서 에러가 나는지
확인할 수단이 없는 상태로 운영에 들어가게 된다.

G-ops-lab은 운영성(operability)을 product feature와 같은 무게로 다루는 연습이다.
health check, structured logging, request metrics, CI Compose probe라는
네 가지 축을 최소 구현하면서,
"이 서비스를 어떻게 신뢰하고 관찰할 것인가"에 코드로 답한다.

## 어떤 상황을 기대하는가

- `/health/live`는 프로세스가 살아있으면 무조건 200을 돌려준다.
- `/health/ready`는 DB와 Redis까지 확인하고, 문제가 있으면 503을 반환한다.
- `/ops/ready`는 설정 수준의 readiness — URL이 존재하는지만 확인한다.
- `/ops/metrics`는 Prometheus text format으로 요청 카운트를 노출한다.
- 모든 로그는 JSON 형식으로 출력된다.
- Compose의 healthcheck가 `live` 엔드포인트를 주기적으로 probe한다.

## 제약과 경계

| 항목 | 선택 |
|------|------|
| 프레임워크 | FastAPI |
| DB | SQLite (기본), PostgreSQL (compose) |
| Redis | 선택적 — config에 URL이 있을 때만 검사 |
| Metrics | 자체 카운터 (MetricsRegistry), Prometheus client 미사용 |
| Logging | Python logging + 커스텀 JsonFormatter |
| IaC | 없음 — documentation-first AWS 노트 |
| CI | lint + test + smoke + Compose health probe |

## 불확실한 것

- 이 랩만으로 실제 운영 경험을 주장하기는 어렵다.
  하지만 junior backend 면접에서 "기본 운영 감각"을 설명하기에는 충분하다.
- Prometheus/Grafana 전체 stack은 이 랩의 범위를 넘긴다.
- AWS 배포는 문서 수준이며 live verification이 없다.
