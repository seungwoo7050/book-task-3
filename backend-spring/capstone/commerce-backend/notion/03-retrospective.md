# Retrospective — baseline capstone의 가치와 한계

## 잘한 것: 통합 기준점의 생성

### 커머스 도메인이 연결 고리가 되었다

7개의 랩이 각각 독립된 개념을 가르친다. 하지만 "이것들이 실제 서비스에서 어떻게 합쳐지는가?"라는 질문에 답하려면 하나의 도메인이 필요하다. 커머스 도메인은 인증(누가 산다), 카탈로그(뭘 산다), 장바구니(담아둔다), 주문(결제한다)이라는 자연스러운 흐름을 제공했다.

`CommerceApiTest.catalogCartAndOrderFlowWork()`가 이 통합을 하나의 테스트로 보여준다. 로그인 → 상품 등록 → 목록 조회 → 장바구니 추가 → checkout → 주문 확인. 각 단계가 다른 랩의 개념에 대응된다.

### baseline이 v2의 설명을 가능하게 했다

"왜 v2를 만들었는가?"에 답하려면 v1의 한계를 구체적으로 보여줘야 한다. 이 baseline이 있으므로:
- "인증이 stub이었습니다" → v2에서 JWT로 교체
- "결제가 없었습니다" → v2에서 결제 flow 추가
- "이벤트 연동이 없었습니다" → v2에서 outbox + Kafka consumer 추가
- "주문 상태가 PLACED 하나였습니다" → v2에서 상태 전이 구현

이 서사가 면접에서 "학습과 개선의 과정"을 설명하는 핵심 자료가 된다.

## 여전히 약한 것

### 인증의 얕음

`CommerceAuthController.login()`은 어떤 이메일이든 `"commerce-access-token"`을 반환한다. SecurityConfig는 모든 요청을 permit한다. 실제 인증이 없으므로 `/api/v1/admin/products`에 아무나 접근할 수 있다. admin/customer 역할 구분이 코드에는 없고 URL naming convention에만 있다.

### 결제의 부재

커머스 백엔드에서 결제가 없다는 것은 핵심 기능이 빠진 것이다. checkout은 재고만 차감하고 주문을 PLACED로 만든다. 실제 결제(PG사 연동 또는 포인트 차감)가 있어야 "커머스"라는 이름이 정당화된다.

### 비동기 통합의 부재

compose.yaml에 Redpanda와 Mailpit이 있지만, 코드에서 이들에 연결하는 부분이 없다. checkout 후 주문 이벤트를 Kafka로 발행하고, consumer가 이를 받아 알림 이메일을 보내는 flow가 없다. E-event-messaging-lab에서 다룬 outbox pattern이 여기에 적용되지 않았다.

## 다시 볼 것

1. **v2와의 비교 문서**: 파일 단위로 "v1에서 → v2에서" 변경 내역을 정리한다. 어떤 파일이 추가되었고, 어떤 클래스가 교체되었고, 각 변경이 어떤 한계를 해결하는지.

2. **checkout 트랜잭션 강화**: `@Version` 낙관적 락이 있지만, 동시 checkout 시나리오 테스트가 없다. 두 고객이 같은 상품의 마지막 1개를 동시에 checkout하면 어떻게 되는지 테스트한다.

3. **포트폴리오 전략**: 면접에서 이 프로젝트를 보여줄 때는 v2를 전면에 두되, "왜 이렇게 만들었는지"를 설명할 때 v1을 참조하는 것이 가장 효과적이다.

