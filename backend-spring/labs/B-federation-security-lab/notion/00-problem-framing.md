# Problem Framing

## Goal

`study2/labs/B-federation-security-lab`의 목표는 Spring에서 local auth 이후의 보안 hardening 주제를 분리해 보는 것이다. Google OAuth2 callback modeling, 2FA, recovery code, throttling, audit logging은 각각 따로 배우기보다 “인증 성공 이후에도 신뢰를 어떻게 높일 것인가”라는 질문 아래 묶는 편이 낫다. 최소 성공 조건은 현재 scaffold 범위를 분명히 밝히면서도, 왜 이 주제들이 같은 랩에 묶였는지 설명 가능한 것이다.

## Inputs and constraints

- Java/Spring:
  - Java 21
  - Spring Boot 3.4.x
- Services:
  - PostgreSQL
  - Redis
- Security requirements:
  - Google OAuth2-like callback flow
  - TOTP and recovery code
  - throttling and audit logging
- Repository givens:
  - 구현 상태는 `verified scaffold`
  - Google integration은 simulated contract다
- Decisions still needed:
  - real OAuth client integration을 언제 넣을지

## Success criteria

- federation, second factor, throttling, audit를 같은 auth 확장 문제로 설명해야 한다.
- documented commands가 통과해야 한다.
- simulation과 real integration의 경계를 숨기지 않아야 한다.

## Uncertainty log

- mocked provider와 real provider 사이의 operational gap은 남아 있다.
- 그래도 scaffold 단계에서는 internal identity model을 먼저 이해하는 것이 우선이라고 가정했다.
- live provider 실험은 별도 sandbox profile로 확인해야 한다.

