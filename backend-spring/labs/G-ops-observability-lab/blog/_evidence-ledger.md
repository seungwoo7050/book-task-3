# G-ops-observability-lab evidence ledger

- 복원 방식: 세부 commit 로그 대신 `Phase 1 -> Phase 3`으로 다시 정리했다.
- 근거: `README.md`, `problem/README.md`, `docs/README.md`, `spring/Makefile`, `OpsController.java`, `TraceIdFilter.java`, `application.yml`, `logback-spring.xml`, `compose.yaml`, `prometheus.yml`, `OpsApiTest.java`, `HealthApiTest.java`, `spring/build/test-results/test/*.xml`, `../../docs/verification-report.md`
- 작업 환경 전제: macOS + VSCode 통합 터미널 기준.

## Phase 1

- 당시 목표: 운영 랩의 baseline을 health와 summary surface로 먼저 고정한다.
- 변경 단위: `README.md`, `problem/README.md`, `OpsApiTest.java`, `HealthApiTest.java`
- 처음 가설: 운영성은 capstone 부록으로만 정리해도 충분할 것 같았다.
- 실제 조치: `/api/v1/ops/summary`, `/api/v1/health/live`, `/api/v1/health/ready`를 별도 테스트로 고정했다.
- CLI:

```bash
cd spring
make test
```

- 검증 신호: `OpsApiTest` 1개 테스트 통과, `HealthApiTest` 2개 테스트 통과
- 핵심 코드 앵커: `OpsApiTest.summaryExposesOperationalLinks()`, `HealthApiTest.liveEndpointResponds()`
- 새로 배운 것: 운영성의 첫걸음은 대시보드가 아니라 앱이 관찰 surface를 스스로 드러내는 일이다.
- 다음: trace id, JSON logging, metrics 노출을 설정과 코드에 묶는다.

## Phase 2

- 당시 목표: health 외의 운영 기본기를 런타임 설정으로 연결한다.
- 변경 단위: `TraceIdFilter.java`, `logback-spring.xml`, `application.yml`, `compose.yaml`, `prometheus.yml`
- 처음 가설: 문서에 Prometheus 사용만 적어도 충분할 수 있다고 봤다.
- 실제 조치: `X-Trace-Id`, JSON logging, `/actuator/prometheus` 노출, Prometheus scrape 설정을 실제 파일에 넣었다.
- CLI:

```bash
cd spring
make smoke
docker compose up --build
```

- 검증 신호: `LabInfoApiSmokeTest` 1개 테스트 통과, `2026-03-09` 검증 보고서 기준 lint/test/smoke/Compose health 통과
- 핵심 코드 앵커: `TraceIdFilter.doFilterInternal()`, `logback-spring.xml`, `prometheus.yml`
- 새로 배운 것: observability는 도구 목록이 아니라 config, log format, endpoint exposure가 함께 맞물리는 계약이다.
- 다음: alert와 live infra를 아직 하지 않았다는 점을 문서에 닫는다.

## Phase 3

- 당시 목표: 운영 완성본이 아니라 baseline이라는 점을 분명히 남긴다.
- 변경 단위: `docs/README.md`, `spring/README.md`, `TEST-com.webpong.study2.app.OpsApiTest.xml`
- 처음 가설: health와 metrics path만 있으면 운영성 설명이 충분할 줄 알았다.
- 실제 조치: alert rule, dashboard, 외부 log platform, live AWS가 아직 없다는 점을 docs에 남겼다.
- CLI:

```bash
cd spring
make lint
make test
make smoke
```

- 검증 신호: `2026-03-13` 기준 4개 suite, 총 5개 테스트, 실패 0
- 핵심 코드 앵커: `docs/README.md`의 의도적 단순화, `verification-report.md`
- 새로 배운 것: 운영 글은 지금 관찰 가능한 것과 아직 비어 있는 것을 같이 써야 믿을 만해진다.
- 다음: 이 운영 baseline을 `commerce-backend`에 붙여 본다.
