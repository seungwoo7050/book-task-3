# Problem Framing — 랩에서 배운 것을 하나의 서비스로 엮기

## 이 캡스톤이 존재하는 이유

7개의 랩(A-auth부터 G-ops까지)에서 인증, OAuth, 권한, JPA, 이벤트, 캐시, 운영을 각각 다뤘다. 하지만 면접에서 "백엔드 서비스를 처음부터 끝까지 만들어 보셨나요?"라는 질문에 "랩 7개를 했습니다"라고 답하면 설득력이 약하다. 이 질문에 답하려면 하나의 도메인 안에서 인증, 데이터, 주문 흐름, 운영이 어떻게 맞물리는지를 보여주는 통합 프로젝트가 필요하다.

`commerce-backend`는 그 통합의 **baseline**이다. 최종 포트폴리오가 아니라, "이런 방향으로 갈 것이다"라는 출발점이다. `commerce-backend-v2`가 이 baseline을 실제 포트폴리오 수준으로 끌어올린 버전이다.

baseline이 별도로 존재하는 이유: v2와의 차이를 설명할 수 있기 때문이다. "처음에는 이렇게 만들었는데, 이런 한계가 있어서 v2에서 이렇게 개선했다" — 이 서사가 학습 이력의 핵심이다.

## 이 캡스톤이 다루는 것

### 커머스 도메인: 상품 → 장바구니 → 주문

세 개의 엔티티가 하나의 구매 흐름을 형성한다:

- **CommerceProductEntity**: 상품명, 가격(`BigDecimal`), 재고(`int`), 낙관적 락(`@Version`). `decrementStock()` 도메인 메서드로 재고를 차감한다.
- **CartItemEntity**: 고객 이메일, 상품 ID, 수량. 고객별 장바구니를 형성한다.
- **OrderEntity**: 고객 이메일, 총 수량, 상태(`PLACED`). checkout 시점에 장바구니 항목을 주문으로 변환한다.

### CommerceService: checkout 트랜잭션

```java
@Transactional
public OrderResponse checkout(String customerEmail) {
    List<CartItemEntity> items = cartItemRepository.findByCustomerEmail(customerEmail);
    // 장바구니가 비어있으면 예외
    // 각 상품의 재고 확인 → 차감
    // 주문 생성 (status: PLACED)
    // 장바구니 비우기
}
```

하나의 트랜잭션 안에서 재고 확인, 차감, 주문 생성, 장바구니 삭제가 모두 이루어진다. `@Transactional`이 보장하는 것: 재고 차감 후 주문 생성이 실패하면 재고도 롤백된다.

### 인증 surface

`CommerceAuthController`는 login과 me 엔드포인트를 제공하지만, 실제 인증 로직은 없다. 하드코딩된 `"commerce-access-token"`을 반환한다. 이것은 "인증이 필요하다"는 것을 구조적으로 보여주되, 구현은 A-auth-lab 수준으로 남겨둔 상태이다.

### API 엔드포인트

```
POST /api/v1/auth/login          — 로그인 (stub)
GET  /api/v1/me                  — 사용자 정보 (stub)
POST /api/v1/admin/products      — 상품 등록
GET  /api/v1/products            — 상품 목록
POST /api/v1/cart/items          — 장바구니 추가
POST /api/v1/orders              — 주문 (checkout)
GET  /api/v1/admin/orders        — 주문 목록
```

`@Validated`와 Bean Validation(`@Email`, `@NotBlank`, `@Min`)으로 입력을 검증한다.

## 이 캡스톤이 다루지 않는 것

| 미포함 항목 | 이유 |
|------------|------|
| 결제 (Payment) | 결제 연동은 외부 서비스(PG사) 통합이 필요하다. baseline 범위를 넘는다 |
| 실제 인증/인가 | JWT 발급, 토큰 검증, 역할 기반 접근 제어는 v2에서 다룬다 |
| 이벤트/알림 통합 | Redpanda/Kafka consumer가 checkout 이벤트를 받아 알림을 보내는 flow는 미구현 |
| 주문 상태 전이 | PLACED 이후의 상태(PAID, SHIPPED, DELIVERED, CANCELLED)는 v2에서 다룬다 |
| 검색/필터링 | 상품 검색, 카테고리 필터, 페이지네이션은 미구현 |

## 기술 스택

| 구성 요소 | 선택 |
|----------|------|
| 런타임 | Java 21, Spring Boot 3.4.x |
| DB | PostgreSQL 16 (docker), H2 (기본/테스트) |
| ORM | Spring Data JPA, Flyway |
| 검증 | Bean Validation (`@Email`, `@NotBlank`, `@Min`) |
| 인프라 | Redis 7, Mailpit v1.24, Redpanda (compose.yaml) |
| 빌드 | Gradle Kotlin DSL, Spotless, Checkstyle |
| 컨테이너 | Docker multi-stage (temurin:21) |

## 성공 기준

- `make test` — `CommerceApiTest`의 `catalogCartAndOrderFlowWork()` 통과: 로그인 → 상품 등록 → 목록 조회 → 장바구니 추가 → checkout → 주문 확인
- `make lint` — Spotless + Checkstyle 통과
- 현재 상태가 "verified scaffold"임을 문서에서 숨기지 않는다
- payment omission, partial auth depth를 명시한다

## 불확실한 것들

scaffold 수준의 통합 캡스톤만으로는 강력한 포트폴리오가 되기 어렵다. 하지만 baseline이 있어야 v2의 개선 방향과 그 이유를 설명할 수 있다. "왜 v2를 만들었는가?"라는 질문에 "v1에 이런 한계가 있었습니다"라고 답하려면, v1이 존재해야 한다.

