# Problem Framing

## Goal

`commerce-backend-v2`의 목표는 기존 `commerce-backend` 스캐폴드를 그대로 유지한 채, 같은 커머스 도메인을 더 설득력 있는 주니어 Spring 백엔드 포트폴리오 프로젝트로 다시 구현하는 것이다. 이 프로젝트는 단순히 엔드포인트 개수를 늘리는 것이 아니라, 한국 주니어 백엔드 공고에서 자주 요구되는 Spring Boot, JPA, PostgreSQL, Redis, Docker, 테스트, 인증/인가 감각을 한 코드베이스에서 설명 가능하게 만드는 데 초점을 둔다. 최소 성공 조건은 인증, 카탈로그, 장바구니, 주문, 결제, 비동기 알림 흐름이 저장소 기반으로 실제 연결되고, 문서에 적힌 검증 명령이 다시 실행되어 통과하는 것이다.

## Inputs and constraints

- Java and Spring Boot versions used:
  - Java 21
  - Spring Boot 3.4.13
- Datastores or external services involved:
  - H2 for fast local test profile
  - PostgreSQL via Docker profile
  - Redis for cart and auth throttling under Docker profile
  - Kafka-compatible broker via Redpanda
  - Mailpit in Compose, although 이번 캡스톤에서는 메일 기능을 중심 기능으로 사용하지 않았다
- Security or correctness requirements:
  - access token은 Bearer 토큰으로 전달한다
  - refresh token은 HttpOnly cookie에 저장한다
  - refresh/logout은 CSRF header 검증을 요구한다
  - 결제 확인은 `Idempotency-Key`를 강제한다
  - 재고 차감은 optimistic locking을 통해 oversell을 방지한다
- What the repository already gives you:
  - `study2/capstone/commerce-backend/`라는 기존 통합 스캐폴드
  - 공통 Spring workspace 구조
  - Compose, Gradle, checkstyle, OpenAPI, health endpoint 패턴
- What you still had to decide yourself:
  - 커머스 도메인을 어떤 수준까지 persisted flow로 끌어올릴지
  - Redis와 Kafka를 어디에 써야 “기술 과시”가 아니라 “정당한 사용”으로 보일지
  - 결제를 외부 PG 없이도 설득력 있게 모델링할 방법
  - 캡스톤 문서를 “학습 저장소” 톤을 유지하면서도 포트폴리오 설명으로 읽히게 만드는 방법

## Success criteria

- Endpoints or flows that must work:
  - 회원가입 → 로그인 → `me` 조회
  - refresh token rotation → logout
  - mocked Google authorize/callback → 기존 계정 link 또는 신규 계정 생성
  - admin category/product 생성
  - customer cart 추가 → checkout → mock payment confirm → order 조회
  - `order-paid` outbox event → Kafka consumer → notification 저장
- Commands that prove the current state:
  - `./gradlew testClasses --no-daemon`
  - `make lint`
  - `make test`
  - `make smoke`
  - `./tools/compose_probe.sh study2/capstone/commerce-backend-v2/spring 8111`
- Which failures must be prevented:
  - 잘못된 CSRF token으로 refresh/logout이 통과하는 문제
  - 중복 결제로 같은 주문이 여러 번 처리되는 문제
  - 재고 경쟁 상황에서 stock이 음수가 되는 문제
  - 비동기 알림이 DB 없이 메모리에서만 처리되어 재시작 시 사라지는 문제
- Which topics are intentionally out of scope:
  - 실 Google console 연동
  - 실 PG 결제사 연동
  - 쿠폰, 배송, 정산, 환불 등 전체 커머스 도메인
  - AWS 실제 배포 검증

## Uncertainty log

- What do you still not know?
  - 이 구조가 실제 트래픽 하에서 어느 정도까지 버틸지 알 수 없다.
  - Kafka consumer를 장시간 돌렸을 때 재처리나 운영 장애가 어떤 형태로 나타날지 아직 확인하지 않았다.
- What assumption are you making anyway?
  - 주니어 포트폴리오에서는 “모든 인프라를 실서비스 수준으로 운영했다”보다 “핵심 경계를 왜 이렇게 설계했는지 설명 가능하다”가 더 중요하다고 가정했다.
  - mocked Google callback도 계정 linking과 persisted auth 흐름을 설명하는 데는 충분하다고 가정했다.
- How would you verify or disprove it later?
  - k6 또는 Locust로 checkout/refresh 흐름 부하 테스트를 추가한다.
  - Kafka broker 재시작, Redis 장애, DB lock contention을 넣는 통합 테스트를 추가한다.
  - 실제 OAuth sandbox와 AWS 환경 변수를 물린 별도 profile을 만들어 재검증한다.
