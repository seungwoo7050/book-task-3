# 앱이 스스로를 설명하게 만드는 최소 표면들

`G-ops-observability-lab`은 health, metrics, logs를 나중에 덧붙이는 부록이 아니라, 애플리케이션이 자기 상태를 외부에 설명하는 방식으로 다룬다. macOS + VSCode 통합 터미널에서 `make test`를 다시 돌려 보면 이 랩의 핵심은 화려한 대시보드가 아니라 `/health`, `/actuator/prometheus`, `X-Trace-Id`, JSON 로그처럼 바로 확인 가능한 표면을 먼저 고정하는 데 있다는 점이 보인다.

## 구현 순서 요약

- `problem/README.md`와 `docs/README.md`가 운영 랩의 현재 scope와 의도적 한계를 고정한다.
- `HealthController`, `TraceIdFilter`, `OpsController`, `application.yml`, `logback-spring.xml`이 운영 표면을 만든다.
- `OpsApiTest`와 health/smoke 검증이 현재 증명 범위를 닫는다.

## Phase 1

### Session 1

- 당시 목표:
  - 운영성을 독립 랩의 문제로 먼저 선언한다.
- 변경 단위:
  - `problem/README.md`
  - `docs/README.md`
  - `spring/README.md`
- 처음 가설:
  - health, logging, metrics가 구현 뒤 장식처럼 붙으면 운영성을 "설명 가능한 기본기"로 남기기 어렵다.
- 실제 진행:
  - health/readiness, JSON logging, trace ID, Prometheus scrape target을 canonical scope로 정했다.
  - alert와 dashboard, live AWS 배포는 일부러 뒤로 뺐다.

CLI:

```bash
cp .env.example .env
make run
```

검증 신호:

- `spring/README.md`가 VSCode 터미널 기준 재현 명령을 고정했고, docs는 지금 증명한 운영 표면과 미완 영역을 분리해 적는다.

핵심 코드:

```java
@RequestMapping("/api/v1/health")
public class HealthController {
```

왜 이 코드가 중요했는가:

- 운영성의 시작점은 앱이 자기 상태를 어디서 보여 주는지다. health path가 고정되면 뒤의 smoke, Compose health 확인도 같은 언어로 연결된다.

새로 배운 것:

- observability는 툴 이름보다 먼저 "무슨 질문을 어디에 던질 수 있는가"를 정하는 일이다.

다음:

- trace ID, JSON logging, metrics exposure를 코드와 설정으로 넣는다.

## Phase 2

### Session 1

- 당시 목표:
  - 요청 추적, 구조화 로그, health, metrics를 실제 표면으로 만든다.
- 변경 단위:
  - `spring/src/main/java/com/webpong/study2/app/global/api/HealthController.java`
  - `spring/src/main/java/com/webpong/study2/app/global/logging/TraceIdFilter.java`
  - `spring/src/main/java/com/webpong/study2/app/ops/api/OpsController.java`
  - `spring/src/main/resources/application.yml`
  - `spring/src/main/resources/logback-spring.xml`
- 처음 가설:
  - `X-Trace-Id` 응답 헤더, JSON console appender, actuator prometheus exposure만 있어도 운영 baseline은 충분히 설명된다.
- 실제 진행:
  - live와 ready health endpoint를 분리했다.
  - `TraceIdFilter`가 요청마다 UUID를 만들고 응답 헤더와 MDC에 넣는다.
  - `application.yml`에서 `health,info,prometheus`를 열고 metrics tag를 설정했다.
  - `logback-spring.xml`은 console log를 `LogstashEncoder` 기반 JSON으로 고정했다.
  - `OpsController`는 metrics/docs/health 링크를 한 번에 보여 준다.

CLI:

```bash
make test
```

검증 신호:

- `2026-03-13` macOS + VSCode 통합 터미널 재실행에서 `make test`가 `BUILD SUCCESSFUL`로 끝났다.

핵심 코드:

```java
return Map.of(
    "profile", activeProfile,
    "metrics", "/actuator/prometheus",
    "docs", "/swagger-ui.html",
    "health", "/api/v1/health/ready");
```

왜 이 코드가 중요했는가:

- 운영성은 scattered config 모음이 아니라 "지금 당장 어디를 보면 되나"를 알려 주는 surface가 있어야 읽힌다. `OpsController`는 그 링크들을 한 점으로 모아 준다.

새로 배운 것:

- 운영 기본기는 복잡한 dashboard보다 먼저, 개발자 자신이 다음 진단 위치를 바로 찾을 수 있게 만드는 데서 출발한다.

다음:

- 현재 증명 범위를 테스트와 검증 기록으로 닫고, 아직 문서 단계인 운영 요소를 분리한다.

## Phase 3

### Session 1

- 당시 목표:
  - 운영 표면이 실제 검증 근거로 남는지 확인하고, 문서만 있는 부분도 구분한다.
- 변경 단위:
  - `spring/src/test/java/com/webpong/study2/app/OpsApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/HealthApiTest.java`
  - `spring/src/test/java/com/webpong/study2/app/LabInfoApiSmokeTest.java`
- 처음 가설:
  - ops summary와 health smoke만 있어도 현재 baseline을 충분히 증명할 수 있다.
- 실제 진행:
  - `OpsApiTest`는 summary 응답이 metrics와 health 링크를 노출하는지 검증한다.
  - `HealthApiTest`와 smoke 흐름으로 readiness/liveness surface를 고정했다.
  - `backend-spring` 아래 `.github/workflows` 파일을 직접 찾았지만 `0`개였기 때문에, docs가 말하는 CI hooks는 아직 workspace-local 코드 근거가 아니라 문서/검증 명령 수준이라고 정리했다.

CLI:

```bash
make test
make smoke
docker compose up --build
```

검증 신호:

- `2026-03-13` 재실행 뒤 XML 리포트 4개, `failures=0`이 확인됐다.
- `2026-03-09` 검증 기록에는 lint/test/smoke/Compose health 확인 통과가 남아 있다.
- `.github/workflows` 검색 결과는 `0`개였다.

핵심 코드:

```xml
<encoder class="net.logstash.logback.encoder.LogstashEncoder"/>
```

왜 이 코드가 중요했는가:

- health와 metrics가 외부에서 보는 표면이라면, JSON logging은 운영 중 사건을 다시 읽는 표면이다. 둘 다 있어야 "앱이 스스로를 설명한다"고 말할 수 있다.

새로 배운 것:

- 운영성은 언제나 "코드에 있는 것"과 "문서에서만 말하는 것"을 구분해서 써야 신뢰가 생긴다.

다음:

- alert, dashboard, actual workflow 파일, live infra는 다음 단계에서 추가한다.
