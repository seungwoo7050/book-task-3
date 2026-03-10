# Debug Log — "완성된 커머스 백엔드"처럼 보이는 문제

## 장애 상황: feature surface가 넓으면 완성도가 높아 보인다

이 baseline 캡스톤에는 런타임 버그가 없었다. `make test`를 실행하면 `CommerceApiTest`가 통과하고, 로그인 → 상품 등록 → 카탈로그 조회 → 장바구니 추가 → checkout → 주문 확인이라는 전체 흐름이 동작한다.

문제는 이 테스트가 통과한다는 사실이 암시하는 것이다. 실제로는 인증이 stub이고, 결제가 없고, 이벤트 발행/소비가 없고, 주문 상태 전이가 없다.
## 잘못된 첫 번째 가정

"feature surface가 넓으면 포트폴리오로 충분하다"는 생각이 위험하다. 면접관은 엔드포인트 수가 아니라 각 엔드포인트의 **구현 깊이**를 본다. 인증이 stub이고 결제가 없다면, 엔드포인트가 7개여도 깊이는 얕다.

## 근본 원인

통합 캡스톤은 범위가 넓어질수록 각 축의 구현 깊이가 얕아지는 경향이 있다. baseline의 역할은 방향을 보여주는 것이지 완성도를 증명하는 것이 아니다. 완성도 증명은 v2의 역할이다.

## 해결 과정

코드 변경이 아닌 구조적 분리로 대응했다. `commerce-backend`를 "verified scaffold"로, `commerce-backend-v2`를 "portfolio-grade capstone"으로 분리하고 역할 차이를 문서화했다.

```bash
make test    # 전체 테스트 통과
make lint    # Spotless + Checkstyle 통과
make smoke   # health check 통과
```

## 남은 부채

- baseline과 v2의 구체적인 diff 문서 작성
- authentication stub → JWT 교체 과정 기록
- checkout에 outbox pattern 이벤트 발행 추가 과정 기록

