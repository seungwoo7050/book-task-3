# Problem Framing

## Goal

`study2/labs/C-authorization-lab`의 목표는 인증과 무관하게 role, membership, ownership을 Spring 서비스 경계에서 설명하는 것이다. organization/store membership, invite accept/decline, role changes, method-level authorization decisions는 실제 비즈니스 규칙의 핵심이지만, 처음부터 full auth와 섞으면 오히려 흐려진다. 최소 성공 조건은 current scaffold가 invite와 role 경계를 보여 주고, future improvement가 어디인지 분명히 적는 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
- Themes:
  - invitation lifecycle
  - RBAC
  - ownership checks
- Repository givens:
  - membership state is in memory
  - method security is 아직 다음 단계다
- Decisions still needed:
  - declarative security를 언제 도입할지

## Success criteria

- invite, membership, role change가 service logic 수준에서 드러나야 한다.
- forbidden path를 설명할 수 있어야 한다.
- commands가 검증 가능해야 한다.
- in-memory simplification을 숨기지 않아야 한다.

## Uncertainty log

- in-memory membership가 policy complexity를 충분히 보여주는지는 제한적이다.
- 그래도 scaffold 단계에서는 rule shape를 먼저 고정하는 것이 낫다고 가정했다.
- persistence와 method security는 후속 과제로 검증해야 한다.

