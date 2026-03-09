# Problem Framing

## Goal

`study2/labs/A-auth-lab`의 목표는 Spring Boot에서 로컬 계정 인증의 최소 핵심을 구조적으로 설명하는 것이다. 이 랩은 production-complete auth가 아니라, register/login/refresh/logout, cookie와 CSRF, verification/reset 개념을 Spring 관점에서 배치하는 scaffold 역할을 한다. 최소 성공 조건은 현재 구현 범위와 빠진 범위를 모두 숨기지 않고, `make lint`, `make test`, `make smoke`, Compose boot가 실제로 통과하는 것이다.

## Inputs and constraints

- Java and Spring:
  - Java 21
  - Spring Boot 3.4.x
- Datastores or services:
  - PostgreSQL
  - Redis
  - Mailpit
- Security requirements:
  - refresh rotation pattern
  - HttpOnly cookie and CSRF discussion
  - local account lifecycle
- Repository givens:
  - 현재 상태는 `verified scaffold`다
  - auth persistence는 intentionally lightweight하다
- Decisions still needed:
  - verification/reset을 실제 persisted flow로 얼마나 끌어올릴지

## Success criteria

- register, login, refresh, logout, `me` surface가 설명 가능해야 한다.
- cookie와 CSRF 경계가 README와 노트에서 같이 보여야 한다.
- documented commands가 재실행 가능해야 한다.
- 실 mail-delivery lifecycle이 아직 빠졌다는 점을 명확히 적어야 한다.

## Uncertainty log

- 이 랩만으로 Spring Security auth의 실전 난점을 충분히 보여주는지는 불확실하다.
- 그래도 학습 트랙의 첫 랩에서는 구조와 용어를 고정하는 편이 낫다고 가정했다.
- deeper persistence와 mail workflow는 capstone 또는 후속 개선으로 검증해야 한다.

