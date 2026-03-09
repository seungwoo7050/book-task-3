# Problem Framing

## Goal

`study2/capstone/commerce-backend`의 목표는 Spring 랩의 개념을 하나의 모듈형 모놀리스 커머스 백엔드로 엮는 baseline capstone을 제공하는 것이다. 이 프로젝트는 최종 포트폴리오 수준이라기보다, auth, catalog, cart, order, async hook, ops surface를 한 도메인 안에서 어떻게 재조합할지를 보여주는 출발점이다. 최소 성공 조건은 현재 상태가 `verified scaffold`라는 점을 분명히 하면서, 어떤 축이 나중에 `commerce-backend-v2`로 승격되었는지 설명 가능한 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
- Services:
  - PostgreSQL
  - Redis
  - Mailpit
  - Redpanda
- Product requirements:
  - auth surface
  - catalog
  - cart and order lifecycle
  - notification hook
- Repository givens:
  - current status는 baseline scaffold다
- Decisions still needed:
  - 어떤 축을 실제 persisted flow로 먼저 끌어올릴지

## Success criteria

- 커머스 도메인이 Spring capstone의 baseline shape로 읽혀야 한다.
- auth, catalog, cart/order, async hook이 모두 보이되, 구현 깊이는 과장하지 않아야 한다.
- documented commands가 통과해야 한다.
- payment omission과 partial auth depth를 숨기지 않아야 한다.

## Uncertainty log

- scaffold 단계의 통합 캡스톤이 얼마나 강한 포트폴리오가 될지는 제한적이다.
- 그래도 baseline이 있어야 N+1 개선판의 차이를 설명할 수 있다고 가정했다.
- `commerce-backend-v2`가 이 가정을 실제로 검증하는 비교 대상이 된다.

