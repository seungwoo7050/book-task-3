# commerce-backend structure outline

## 글 목표

- 이 capstone을 "통합 완료본"이 아니라 deliberately thin baseline으로 다시 쓴다.
- fake auth, public admin, validation 공백을 본문 핵심으로 올린다.
- 통합 user journey가 있는 것과 production-grade commerce가 아닌 것을 동시에 보여 준다.

## 글 순서

1. test와 auth controller를 보고 baseline user journey와 auth depth를 먼저 정리한다.
2. controller/service/domain을 따라 catalog/cart/order 연결과 validation 공백을 설명한다.
3. manual HTTP로 invalid inputs, stock decrement, second checkout failure를 확인한다.
4. 왜 이 얕음이 v2 필요성을 만드는지 닫는다.

## 반드시 넣을 코드 앵커

- `CommerceApiTest.catalogCartAndOrderFlowWork()`
- `CommerceAuthController.login()`
- `CommerceAuthController.me()`
- `CommerceController.createProduct()`
- `CommerceService.checkout()`
- `SecurityConfig.securityFilterChain()`
- `V2__commerce.sql`

## 반드시 넣을 검증 신호

```bash
docker run --rm -u $(id -u):$(id -g) \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew test'

docker run --rm -u $(id -u):$(id -g) -p 18087:8080 \
  -e GRADLE_USER_HOME=/tmp/gradle \
  -v /Users/woopinbell/work/book-task-3/backend-spring/capstone/commerce-backend/spring:/workspace \
  -w /workspace eclipse-temurin:21-jdk \
  bash -lc './gradlew bootRun'
```

## 반드시 남길 한계

- fixed token, unauthenticated `/me`
- public admin endpoints
- invalid product/cart inputs accepted
- payment, async integration, strong authz 부재
