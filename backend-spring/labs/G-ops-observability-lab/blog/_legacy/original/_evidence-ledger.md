# G-ops-observability-lab Evidence Ledger

- 복원 기준:
  - `problem/README.md`, `docs/README.md`, `HealthController`, `TraceIdFilter`, `OpsController`, `application.yml`, `logback-spring.xml`, 테스트, `2026-03-13` 재실행 CLI를 묶어 chronology를 복원했다.
- 기존 blog 처리:
  - 기존 `blog/`가 없어 격리 대상은 없었다.

## Phase 1

- 시간 표지: Phase 1
- 당시 목표:
  - 운영성을 capstone 부록이 아니라 독립 학습 주제로 먼저 고정한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - health, metrics, logging, CI를 코드와 분리해서 이야기하면 운영성이 "나중에 붙이는 것"처럼 보인다.
- 실제 조치:
  - health/readiness, JSON logging, trace ID, Prometheus scrape target, Compose-based 운영 표면을 current scope로 선언했다.
  - alert, dashboard, live AWS 배포는 다음 단계로 남겼다.
- CLI:

```bash
cp .env.example .env
make run
```

- 검증 신호:
  - `spring/README.md`가 VSCode 터미널 진입점을 고정하고, docs는 지금 증명한 운영 기본기와 남긴 영역을 분리해서 남겼다.
- 핵심 코드 앵커:
  - `HealthController`, `TraceIdFilter`, `application.yml`, `logback-spring.xml`, `OpsApiTest`.
- 새로 배운 것:
  - 운영 랩의 첫 단계는 외부 SaaS 연결이 아니라, 애플리케이션이 자기 상태를 어떤 HTTP와 로그 표면으로 드러내는지 정하는 일이다.
- 다음:
  - health, trace ID, metrics, JSON logging을 실제 코드로 만든다.

## Phase 2

- 시간 표지: Phase 2
- 당시 목표:
  - 앱이 스스로를 설명하는 최소 운영 표면을 구현한다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/global/api/HealthController.java`
  - `spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java`
  - `spring/src/main/java/com/webpong/study2/app/ops/api/OpsController.java`
  - `spring/src/main/resources/application.yml`
  - `spring/src/main/resources/logback-spring.xml`
- 처음 가설:
  - actuator와 JSON logging, trace ID만 있어도 "운영 기본기"의 대부분은 충분히 설명된다.
- 실제 조치:
  - `/api/v1/health/live`, `/api/v1/health/ready`를 만들었다.
  - 모든 요청에 `X-Trace-Id`를 내려주는 `TraceIdFilter`를 추가했다.
  - actuator exposure에 `health`, `info`, `prometheus`를 열고, logback을 JSON encoder로 고정했다.
  - `/api/v1/ops/summary`에서 metrics, docs, health 링크를 한 번에 보여 주게 했다.
- CLI:

```bash
make test
```

- 검증 신호:
  - `2026-03-13` 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.
- 핵심 코드 앵커:

```java
response.setHeader("X-Trace-Id", traceId);
```

- 새로 배운 것:
  - observability의 최소 단위는 "로그가 남는다"가 아니라, 요청 하나를 끝까지 식별할 trace ID를 응답과 로그에 함께 남기는 것이다.
- 다음:
  - 이 표면이 테스트와 검증 문서에서 실제로 보이는지 확인한다.

## Phase 3

- 시간 표지: Phase 3
- 당시 목표:
  - health, metrics, logs, ops summary가 실제 검증 표면으로 남는지 증명한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/OpsApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - ops summary와 health smoke만 고정해도 이 랩의 baseline은 충분히 설명된다.
- 실제 조치:
  - `/api/v1/ops/summary`가 `/actuator/prometheus`, `/api/v1/health/ready`를 노출하는지 검증했다.
  - 루트와 workspace를 검색했지만 `backend-spring` 아래에는 `.github/workflows` 파일이 없어서, 현재 CI 증거는 docs의 "CI hooks" 설명과 검증 명령 기록에 한정된다는 점도 같이 확인했다.
- CLI:

```bash
make test
make smoke
docker compose up --build
```

- 검증 신호:
  - `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
  - `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.
  - `.github/workflows` 검색 결과는 `0`개였다.
- 핵심 코드 앵커:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
```

- 새로 배운 것:
  - 운영성은 존재를 주장하는 문서보다, 어떤 endpoint와 로그 포맷을 실제로 열어 두었는지가 더 강한 근거가 된다.
- 다음:
  - alert rule, dashboard, 실제 CI workflow 파일, live infra는 다음 단계에서 채운다.
