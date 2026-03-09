# 회고: 조각과 전체는 다른 무게

## 잘된 것

**일곱 개 랩의 개념이 자연스럽게 합쳐졌다.**
SaaS 협업 도구라는 도메인이 auth, workspace, CRUD, notification, WebSocket을
억지 없이 하나의 흐름으로 엮어줬다.
"왜 이 도메인인가?"에 대해 "모든 랩 개념이 필요하니까"라고 답할 수 있다.

**통합 테스트 하나로 전체 흐름을 검증한다.**
`test_capstone.py`는 회원가입부터 WebSocket 알림 수신까지를 하나의 테스트로 검증한다.
이 테스트가 통과하면 "각 역량이 연결되어 동작한다"는 것이 증명된다.

**Cookie 기반 인증 + CSRF를 실제로 구현했다.**
access token을 httpOnly cookie에 넣고, CSRF token을 별도 cookie로 발행하고,
상태 변경 요청에서 CSRF를 검증하는 흐름을 처음부터 끝까지 만들었다.
랩에서는 헤더 기반이었던 인증이 cookie 기반으로 바뀌면서 새로운 문제들을 만났다.

**Notification → Drain → WebSocket 파이프라인이 동작한다.**
코멘트 작성 → 알림 큐잉 → drain → WebSocket 전달이라는 전체 경로가
코드 수준에서 추적 가능하고, 테스트에서 검증된다.

## 아쉬운 것

**Worker 프로세스가 분리되지 않았다.**
drain은 API 프로세스 안에서 실행된다.
E-async-jobs-lab에서 배운 Celery worker 분리가 capstone에는 적용되지 않았다.
학습 목적으로는 충분하지만, 프로덕션 구조와는 다르다.

**Rate limiter가 테스트에서 충분히 검증되지 않았다.**
RateLimiter 클래스는 존재하지만, 통합 테스트에서 rate limiting 시나리오를
직접 검증하지 않는다.

**프론트엔드 없이는 "제품"이 아니다.**
백엔드만으로는 완결된 사용자 경험을 보여줄 수 없다.
하지만 이 저장소의 목적은 백엔드 학습이므로 이것은 의도된 한계다.

## 면접에서 쓸 수 있는 것

- 여러 백엔드 역량을 하나의 서비스로 통합한 설계 과정
- Cookie + CSRF 인증 흐름: httpOnly cookie, SameSite, CSRF double-submit
- SQLAlchemy metadata와 import side effect의 관계
- Notification queue → WebSocket drain 파이프라인
- 통합 테스트에서 HTTP + WebSocket 혼합 검증 전략
- lru_cache + Settings 테스트 격리 패턴
- lifespan을 이용한 schema bootstrapping
