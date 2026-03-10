# Approach Log — 커머스 도메인을 baseline으로 선택한 과정

## 세 가지 선택지

랩에서 배운 것들을 어떻게 통합할 것인가. 세 가지 방향이 있었다.

**첫 번째 길: 처음부터 포트폴리오 수준 캡스톤으로 바로 가기.** JWT 인증, 결제 연동, 이벤트 발행/소비, 분산 락, 운영 모니터링까지 한 번에 구현한다. 결과물은 강력하지만 "baseline → 개선"이라는 학습 서사가 사라진다. 무엇이 왜 개선되었는지를 설명할 비교 지점이 없다.

**두 번째 길: scaffold 캡스톤을 별도로 보존하기.** baseline과 개선 버전을 모두 유지하면 중복이 생기지만, 학습 이력이 선명해진다. "v1에서 인증이 stub이었는데 v2에서 JWT로 교체했다"는 서사가 가능하다.

**세 번째 길: 랩 코드를 그대로 import하여 합치기.** 가장 빠르지만 의미가 없다. 랩은 각각 독립적인 시나리오를 위해 설계되었으므로, 그대로 합치면 domain model이 충돌한다.

두 번째 길을 택했다.

## 선택한 설계 방향

### 커머스 도메인의 선택

왜 커머스인가? 인증(누가 산다), 카탈로그(뭘 산다), 장바구니(담아둔다), 주문(결제한다), 알림(알려준다) — 백엔드의 주요 개념들이 하나의 구매 흐름 안에 자연스럽게 연결된다. 다른 도메인(예: 채팅, SNS, 예약)도 가능하지만, 커머스는 도메인 자체가 명확하고 면접에서도 이해하기 쉽다.

### 모듈형 모놀리스

```
com.webpong.study2.app
├── commerce/
│   ├── api/           ← CommerceController, CommerceAuthController
│   ├── application/   ← CommerceService
│   └── domain/        ← Entity, Repository
└── global/            ← SecurityConfig, HealthController, TraceIdFilter, ...
```

하나의 Spring Boot 애플리케이션 안에서 `commerce` 패키지가 비즈니스 도메인을, `global` 패키지가 인프라/운영을 담당한다. 마이크로서비스가 아닌 모듈형 모놀리스를 택한 이유: 이 저장소의 목적이 "백엔드 구조를 이해하기"이지 "서비스 오케스트레이션을 학습하기"가 아니기 때문이다.

### 세 개의 엔티티

| 엔티티 | 테이블 | 핵심 필드 |
|--------|--------|----------|
| `CommerceProductEntity` | `commerce_products` | name, price(BigDecimal), stock, version(@Version) |
| `CartItemEntity` | `commerce_cart_items` | customerEmail, productId, quantity |
| `OrderEntity` | `commerce_orders` | customerEmail, totalQuantity, status |

`CommerceProductEntity`에 `@Version`이 있으므로 낙관적 락이 적용된다. 두 관리자가 동시에 같은 상품의 재고를 수정하면 하나는 `OptimisticLockException`을 받는다.

### checkout: 하나의 트랜잭션

`CommerceService.checkout()`은 `@Transactional` 안에서:
1. 고객 이메일로 장바구니 항목 조회
2. 각 상품의 재고 확인 → 부족하면 예외
3. 재고 차감 (`decrementStock`)
4. 주문 생성 (status: PLACED)
5. 장바구니 비우기 (`deleteByCustomerEmail`)

모든 단계가 하나의 트랜잭션이므로, 4단계에서 실패하면 3단계의 재고 차감도 롤백된다.

### 인증: stub으로 남긴 이유

`CommerceAuthController`는 하드코딩된 토큰을 반환한다. 이것은 의도적인 선택이다:
- A-auth-lab에서 인증의 원리를 이미 다뤘다
- baseline에서 인증까지 완성하면 v2에서 개선할 축이 줄어든다
- "인증이 필요하다"는 구조(endpoint 존재)는 보여주되, 구현은 v2로 미룬다

## 폐기한 아이디어들

- **랩 코드 직접 import**: 각 랩의 도메인 모델이 다르므로 합치면 충돌한다. 커머스 도메인에 맞게 새로 설계해야 한다.
- **최종본으로 바로 주장**: baseline 없이 v2만 보여주면 "왜 이렇게 만들었는지"를 설명할 수 없다. 이전 버전과의 비교가 학습 깊이를 증명한다.

## 근거 자료

docs/README.md에서 현재 구현 범위("login surface, admin product creation, cart item creation, order placement, stock decrement through checkout")와 simplification("auth is contract-level only, payment is omitted entirely")을 확인했다. problem/README.md는 "a backend-only commerce system that recomposes the learning from the Spring labs into one coherent service"로 방향을 정의하고 있다.

