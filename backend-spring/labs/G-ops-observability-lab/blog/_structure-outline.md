# G-ops-observability-lab structure outline

## 글 목표

- 운영성을 부록이 아니라 health, logs, metrics의 기본기로 복원한다.
- macOS + VSCode 통합 터미널 기준의 검증 흐름을 유지한다.

## 글 순서

1. health와 ops summary를 먼저 고정한 단계
2. trace id, JSON logging, Prometheus scrape를 연결한 단계
3. alert와 live infra를 아직 남긴 이유를 닫는 단계

## 반드시 넣을 코드 앵커

- `OpsController.summary()`
- `TraceIdFilter.doFilterInternal()`
- `application.yml`의 actuator/prometheus 노출

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- observability의 시작은 앱이 관찰 surface를 드러내는 일이다.
- trace id와 JSON logging은 같은 요청을 잇는 최소 계약이다.
