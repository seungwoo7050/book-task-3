# 10-shippable-backend-service structure plan

이 문서는 capstone 확장판처럼 보이기보다, 제출용 서비스 표면이 어디서 만들어지는지 보여 줘야 한다. 서사의 축은 `bootstrap/docs/schema -> cache/throttle policy -> infra-backed verification`이다.

## 읽기 구조

1. `configureApp`와 migration으로 제출용 표면을 먼저 세운다.
2. Redis cache와 login throttling이 service flow를 어떻게 바꾸는지 보여 준다.
3. infra 부재 실패와 compose 이후 성공을 하나의 검증 서사로 묶는다.

## 반드시 남길 근거

- `configureApp`
- migration file
- `AuthRateLimitService`
- `AuthService.login`
- `BooksService`
- unit 12개
- e2e 초기 실패와 compose 이후 16개 통과

## 리라이트 톤

- 기능 홍보문처럼 쓰지 않는다.
- "왜 이 검증은 인프라까지 포함해야 하는가"가 먼저 보이게 쓴다.
