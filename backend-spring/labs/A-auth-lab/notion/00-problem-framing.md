# Problem Framing — 왜 "인증"부터 시작했는가

## 이 랩이 풀려는 문제

백엔드를 처음 설계할 때 가장 먼저 부딪히는 관문은 "사용자가 누구인지 어떻게 확인하는가"이다. Spring Security는 이 질문에 대해 막강한 도구 세트를 제공하지만, 동시에 자동 설정이 겹겹이 쌓여 있어서 처음 보는 사람에겐 블랙박스처럼 느껴지기 쉽다.

이 랩은 그 블랙박스를 한 겹씩 벗기는 것을 목표로 한다. 완성된 프로덕션 인증 시스템을 만드는 게 아니라, **register → login → refresh → logout** 의 흐름이 Spring 안에서 어떤 구조로 배치되는지를 직접 손으로 잡아보는 scaffold다.

처음엔 "인증이야 라이브러리 갖다 쓰면 되지"라고 생각할 수 있다. 하지만 실제로 refresh token은 어디에 저장하는지, CSRF 토큰은 왜 따로 필요한지, cookie의 HttpOnly 플래그가 어떤 공격을 막는지를 구조적으로 이해하지 않으면, 프로덕션에서 반드시 보안 사고로 돌아온다. 이 랩은 그 "왜"를 먼저 고정하고, "어떻게"는 점진적으로 채워나가는 전략을 택했다.

## 기술 환경과 제약

이 랩을 시작하기 전, 몇 가지 기술적 출발점이 정해져 있었다.

**언어와 프레임워크** 측면에서는 Java 21과 Spring Boot 3.4.x를 사용한다. Spring Security의 최신 `SecurityFilterChain` 방식을 기준으로 하며, 더 이상 `WebSecurityConfigurerAdapter`는 쓰지 않는다.

**데이터 스토어**로는 PostgreSQL 16(Docker 프로필에서 사용), Redis 7(세션/캐시 용도), 그리고 Mailpit(로컬 메일 테스트)을 구성했다. 로컬 개발 시에는 H2 인메모리 데이터베이스가 PostgreSQL 호환 모드로 동작하므로, Docker 없이도 테스트가 돌아간다.

**보안 요구사항**으로는 refresh token rotation 패턴, HttpOnly cookie와 CSRF 토큰의 페어링, 그리고 로컬 계정 라이프사이클(가입 → 인증 → 갱신 → 로그아웃)을 다룬다.

다만 한 가지 의도적인 제약이 있다. **persistence는 의도적으로 가볍게** 두었다. `AuthDemoService`는 `ConcurrentHashMap`으로 유저와 세션을 관리한다. 이건 실수가 아니라, 첫 번째 랩에서 인증의 "흐름"에 집중하기 위한 선택이었다. 실제 DB 저장은 D-data-jpa-lab이나 capstone에서 본격적으로 다룬다.

## 성공 기준 — 이 랩이 제대로 됐다는 걸 어떻게 아는가

1. **register, login, refresh, logout, `/me`** 다섯 가지 엔드포인트가 동작하고, 각각의 역할을 설명할 수 있어야 한다.
2. **cookie와 CSRF의 경계**가 코드와 문서에서 일관되게 보여야 한다. 특히 `X-CSRF-TOKEN` 헤더 없이 refresh를 시도하면 명시적으로 실패하는 것을 테스트로 증명한다.
3. **문서에 적힌 명령어**(`make lint`, `make test`, `make smoke`, `docker compose up --build`)가 실제로 재실행 가능해야 한다.
4. 아직 **실제 메일 전송 라이프사이클이 빠져 있다**는 점을 숨기지 않고 명확히 기록해야 한다.

## 아직 확실하지 않은 것들

이 랩 하나로 Spring Security 인증의 실전 난이도를 충분히 보여줄 수 있는지는 솔직히 확신이 없다. OAuth2 연동, 2FA, rate limiting 같은 주제는 의도적으로 제외했고, 이건 B-federation-security-lab이나 C-authorization-lab에서 다룰 영역이다.

그래도 학습 트랙의 첫 랩에서는 **용어와 구조를 고정하는 것**이 가장 중요하다고 판단했다. "refresh rotation이 뭔지", "CSRF가 왜 필요한지" 같은 기본 개념이 흔들리면, 이후 랩에서 더 복잡한 시나리오를 다룰 때 혼란이 누적된다.

deeper persistence와 실제 메일 전송 워크플로우는 capstone 또는 후속 개선에서 검증해야 할 숙제로 남겨두었다.

