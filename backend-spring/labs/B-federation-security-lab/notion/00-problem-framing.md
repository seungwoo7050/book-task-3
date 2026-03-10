# Problem Framing — "로그인 성공" 이후에도 신뢰를 높여야 하는 이유

## 이 랩이 풀려는 문제

A-auth-lab에서 로컬 계정의 register → login → refresh → logout 흐름을 잡았다면, 자연스럽게 다음 질문이 따라온다. **"비밀번호 하나로 정말 충분한가?"**

현실에서 대부분의 서비스는 소셜 로그인(Google, GitHub 등)을 지원하고, 민감한 작업 전에는 2FA(이중 인증)를 요구하며, 비정상적인 로그인 시도를 감지해 차단한다. 이 모든 것이 "인증 성공 이후에도 신뢰를 어떻게 높일 것인가"라는 하나의 질문 아래 묶인다.

이 랩은 그 질문을 네 가지 축으로 분해한다:
1. **Federation** — Google OAuth2 콜백을 모델링해서, 외부 provider의 identity를 내부 user에 연결하는 구조를 이해한다.
2. **Second Factor (2FA)** — TOTP 설정과 검증 흐름을 구현해서, 비밀번호 이후의 추가 인증 레이어를 경험한다.
3. **Audit Logging** — 모든 인증 관련 이벤트를 기록해서, "누가 언제 무엇을 했는지" 사후 추적이 가능한 기반을 만든다.
4. **Throttling** — 무차별 대입 공격 방어를 위한 속도 제한을 문서화한다 (현재는 개념 수준).

처음엔 이 주제들을 별도 랩으로 쪼개는 것도 고려했다. 하지만 직접 작업해보니, 이 네 가지는 서로 물려 있다. OAuth 콜백이 성공한 뒤에도 2FA가 남아야 하고, 2FA 실패는 audit에 기록되어야 하며, 반복적인 2FA 실패는 throttling으로 이어져야 한다. 하나의 랩에서 이 흐름을 연결하는 것이 조각난 이해보다 낫다.

## 기술 환경과 제약

**언어와 프레임워크**: Java 21, Spring Boot 3.4.x — A랩과 동일한 기반에서 확장한다.

**데이터 스토어**: PostgreSQL 16 (Docker 프로필), Redis 7, H2 인메모리 (로컬). 이 랩에서 Redis는 향후 rate limiting 백엔드로 사용될 잠재적 역할을 갖고 있지만, 현재 scaffold에서는 아직 활용하지 않는다.

**보안 요구사항**:
- Google OAuth2 콜백 흐름 (시뮬레이션)
- TOTP(Time-based One-Time Password) 설정과 검증
- recovery code 발급
- audit event 기록

**핵심 제약**: Google integration은 **simulated contract**다. 실제 Google Cloud Console 앱을 등록하고 client ID를 받아 연동하는 것이 아니라, authorize URL 생성과 callback 수신의 **형태(shape)**를 보여주는 데 그친다.

## 성공 기준

1. federation(외부 provider 연동), second factor(2FA), throttling, audit를 **하나의 auth 확장 문제**로 설명할 수 있어야 한다.
2. 문서에 적힌 명령어(`make lint`, `make test`, `make smoke`, `docker compose up --build`)가 통과해야 한다.
3. **simulation과 real integration의 경계**를 숨기지 않아야 한다.

## 아직 확실하지 않은 것들

mocked provider와 real provider 사이의 실제 운영 차이는 이 랩만으로 메울 수 없다. 실제 OAuth2 연동에서는 token exchange, id_token 검증, provider-side session 관리 같은 추가 복잡성이 있다. 그래도 scaffold 단계에서는 internal identity model을 먼저 이해하는 것이 우선이라고 판단했다.

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

