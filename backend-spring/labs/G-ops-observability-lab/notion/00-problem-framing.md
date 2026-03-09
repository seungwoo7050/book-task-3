# Problem Framing

## Goal

`study2/labs/G-ops-observability-lab`의 목표는 Spring 백엔드에서도 운영성이 독립 주제임을 분명히 하는 것이다. Docker, health, logs, metrics, CI, AWS delivery note는 제품 기능이 아니라 서비스 신뢰성의 언어다. 최소 성공 조건은 JSON logging, trace ID, Prometheus scrape target, Compose, GitHub Actions, deployment note가 현재 scaffold 범위 안에서 검증 가능하고, alerting/IaC가 아직 후속 단계임을 명시하는 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
  - Actuator, Micrometer, Prometheus
- Operational surfaces:
  - health endpoints
  - structured logs
  - metrics
  - CI
  - AWS docs
- Repository givens:
  - 현재는 `verified scaffold`
- Decisions still needed:
  - observability depth를 어디까지 core lab 범위로 둘지

## Success criteria

- health, logs, metrics, CI, deployment note가 한 묶음으로 설명돼야 한다.
- documented commands가 통과해야 한다.
- metrics/alerts와 AWS live deployment가 아직 미완임을 숨기지 않아야 한다.

## Uncertainty log

- 이 랩만으로 운영 역량을 충분히 증명할 수는 없다.
- 그래도 backend hiring에서는 이런 기본 언어를 말할 수 있는지가 중요하다고 가정했다.
- IaC와 alert rules는 후속 개선으로 남겨 둔다.

