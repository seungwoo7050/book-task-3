# Knowledge Index — 통합 캡스톤의 핵심 개념 사전

## 핵심 개념

### Baseline Capstone

학습 트랙의 **통합 방향**을 보여주는 기준 프로젝트이다. 최종 포트폴리오가 아니라, 개선의 출발점이다.

이 baseline의 역할:
1. 7개 랩에서 다룬 개념들이 하나의 도메인에서 어떻게 합쳐지는지 보여준다
2. v2와의 비교를 통해 "무엇이 왜 개선되었는지"를 설명할 수 있게 한다
3. 각 축(인증, 데이터, 이벤트 등)의 현재 깊이와 목표 깊이의 간극을 명시한다

면접에서의 활용: "처음에는 인증을 stub으로 두고 도메인 흐름에 집중했습니다. 이후 v2에서 JWT 인증과 역할 기반 접근 제어를 추가했습니다."

### 모듈형 모놀리스 (Modular Monolith)

하나의 애플리케이션(하나의 JAR, 하나의 프로세스) 안에서 **모듈 경계를 명확히 두는** 아키텍처이다. 마이크로서비스의 분리 비용(네트워크 통신, 분산 트랜잭션, 배포 복잡도) 없이, 코드 수준에서 관심사를 분리한다.

이 프로젝트의 모듈 구조:
- `commerce/` — 비즈니스 도메인 (api, application, domain)
- `global/` — 인프라 모듈 (security, logging, health, config)

모듈 간 규칙: `global/`은 `commerce/`를 모른다. `commerce/`는 필요한 경우 `global/`의 설정을 사용한다. 이 단방향 의존이 모듈 경계를 유지한다.

### Checkout 트랜잭션

장바구니의 내용을 주문으로 변환하는 핵심 비즈니스 로직이다.

```java
@Transactional
public OrderResponse checkout(String customerEmail) {
    List<CartItemEntity> items = cartItemRepository.findByCustomerEmail(customerEmail);
    if (items.isEmpty()) throw new IllegalArgumentException("Cart is empty");
    
    int totalQuantity = 0;
    for (CartItemEntity item : items) {
        CommerceProductEntity product = productRepository.findById(item.getProductId())
            .orElseThrow(() -> new IllegalArgumentException("Product not found"));
        if (product.getStock() < item.getQuantity())
            throw new IllegalArgumentException("Not enough stock");
        product.decrementStock(item.getQuantity());
        totalQuantity += item.getQuantity();
    }
    
    OrderEntity order = orderRepository.save(
        new OrderEntity(customerEmail, totalQuantity, "PLACED"));
    cartItemRepository.deleteByCustomerEmail(customerEmail);
    return new OrderResponse(...);
}
```

`@Transactional`이 보장하는 것: 재고 차감 후 주문 생성이 실패하면 재고도 롤백된다. 단, 이 방식은 "긴 트랜잭션" 문제가 있다 — 장바구니 항목이 많으면 트랜잭션 시간이 길어지고 DB 락을 오래 잡는다.

### @Version 낙관적 락

```java
@Version private long version;
```

JPA의 `@Version`은 UPDATE 시 WHERE 절에 version을 포함한다. 두 트랜잭션이 같은 row를 동시에 수정하면, 먼저 커밋한 쪽이 version을 올리고, 늦은 쪽은 `OptimisticLockException`을 받는다.

비관적 락(`SELECT ... FOR UPDATE`)과의 차이:
- 낙관적 락: 충돌이 드문 경우 효율적. 충돌 시 재시도 로직 필요
- 비관적 락: 충돌이 잦은 경우 안전. 대기 시간 증가

### Upgrade Path (Scaffold → Portfolio-grade)

scaffold에서 portfolio-grade 프로젝트로 승격시키는 과정이다. 이 프로젝트에서 v2로의 upgrade path:

| 축 | v1 (baseline) | v2 (portfolio-grade) |
|----|--------------|---------------------|
| 인증 | stub (하드코딩 토큰) | JWT + Spring Security |
| 결제 | 없음 | 결제 flow + idempotency |
| 주문 상태 | PLACED만 | PLACED → PAID → SHIPPED → DELIVERED |
| 이벤트 | 없음 | outbox pattern + Kafka |
| 알림 | 없음 | 이메일/webhook |

## 참고 자료

| 출처 | 확인 내용 | 날짜 |
|------|----------|------|
| docs/README.md | 현재 구현 범위와 simplification | 작성 시점 |
| problem/README.md | "backend-only commerce system that recomposes learning" | 작성 시점 |
| commerce-backend-v2/README.md | v2의 역할과 baseline과의 차이 | 작성 시점 |
