# J-edge-gateway-lab 근거 정리

## 1. 문제 정의와 범위

- `problem/README.md`
  - public API shape 유지, gateway edge cookie/CSRF, 내부 호출의 `X-Request-ID` 전달을 목표로 둔다.
  - 제외 범위를 circuit breaker, service discovery, 고급 edge cache로 명시한다.
- `README.md`
  - 이 랩을 public API 유지와 edge 책임 재배치 랩으로 소개한다.

## 2. 실제 compose 런타임

- `fastapi/compose.yaml`
  - `gateway`, `identity-service`, `workspace-service`, `notification-service`, `redis`를 함께 띄운다.
  - public entrypoint는 `8013`의 gateway다.
  - 내부 서비스는 `8121`, `8122`, `8123`, Redis는 `6393`을 사용한다.
- `fastapi/README.md`
  - gateway를 public API와 websocket edge의 진입점으로 설명한다.

## 3. cookie와 CSRF가 edge에만 남는 근거

- `fastapi/gateway/app/api/v1/routes/auth.py`
  - `/login`, `/google/login`에서 내부 identity 응답을 받아 gateway가 직접 access/refresh/csrf 쿠키를 설정한다.
  - `/token/refresh`, `/logout`는 gateway에서 CSRF를 검증하고 refresh cookie를 읽은 뒤 내부 identity API를 호출한다.
- `fastapi/gateway/app/api/deps.py`
  - gateway는 access cookie를 읽어 현재 claims를 해석한다.
  - CSRF 검증도 gateway dependency에서 수행한다.
- `fastapi/services/identity-service/app/api/v1/routes/auth.py`
  - 내부 identity login/google-login/refresh는 쿠키가 아니라 JSON session bundle을 반환한다.

## 4. gateway가 내부 서비스 계약으로 번역하는 경로

- `fastapi/gateway/app/api/v1/routes/platform.py`
  - `_auth_headers()`가 gateway cookie의 access token을 `Authorization: Bearer ...`로 변환한다.
  - public `/api/v1/platform/*` 호출을 내부 `/internal/*` 호출로 fan-out 한다.
  - `/notifications/drain`은 workspace relay와 notification consume를 묶어 외부에 하나의 엔드포인트로 보여 준다.
  - 다만 `/notifications/drain`은 현재 `get_current_claims()` dependency 없이 orchestration만 수행하는 예외 route다.
  - `/ws/notifications`는 websocket edge를 제공하고, access token query parameter를 직접 받는다.
- `fastapi/contracts/README.md`
  - public API는 gateway 기준 `/api/v1/auth/*`, `/api/v1/platform/*`로 고정한다고 적어 둔다.

## 5. request id 전파 근거

- `fastapi/gateway/app/main.py`
  - gateway middleware가 들어온 `X-Request-ID`를 쓰거나 새 UUID를 만들고, response header에도 같은 값을 넣는다.
- `fastapi/gateway/app/runtime.py`
  - `ServiceClient.request()`가 모든 upstream 호출 헤더에 `X-Request-ID: request.state.request_id`를 추가한다.
- `fastapi/services/identity-service/app/main.py`
- `fastapi/services/workspace-service/app/main.py`
- `fastapi/services/notification-service/app/main.py`
  - 세 내부 서비스 모두 요청 헤더의 `X-Request-ID`를 읽어 response header에 다시 넣는다.

이 부분은 이번 system test에서 직접 assert되지는 않았다. 문서에서는 "소스 경로로 확인한 전파"로 표현했다.

## 6. websocket과 복구 시나리오

- `fastapi/gateway/app/runtime.py`
  - `RedisNotificationRelay`가 pub/sub를 듣고 websocket 연결로 fan-out 한다.
  - `ConnectionManager`가 사용자별 websocket set을 관리한다.
- `fastapi/tests/test_system.py`
  - 클라이언트는 끝까지 gateway base URL `http://127.0.0.1:8013`만 사용한다.
  - collaborator가 gateway websocket `/api/v1/platform/ws/notifications`에 연결한다.
  - `notification-service`를 중지한 뒤 drain 요청이 `503`이 되는지, 재시작 후 recovery drain으로 두 번째 알림이 도착하는지 확인한다.

## 7. 이번 턴에서 다시 실행한 명령과 결과

- `cd fastapi && make lint`
  - 통과.
- `cd fastapi && make test`
  - `gateway` 테스트 import 단계에서 `ModuleNotFoundError: No module named 'argon2'`로 실패.
- `cd fastapi && make smoke`
  - 통과.
- `cd fastapi && python3 -m pytest tests/test_system.py -q`
  - 통과.

## 8. 문서에 반영한 핵심 판단

- 이 랩의 핵심은 gateway 제품 기능 나열이 아니라 edge 책임 재배치다.
- 쿠키/CSRF는 gateway에만 남고, 내부 서비스는 bearer 계약만 읽는다.
- 다만 drain과 websocket은 각각 무-auth orchestration, query-token auth라는 예외를 가진다.
- request id 전파는 명시적 테스트보다 코드 경로 근거가 더 강하다.
- gateway는 upstream 장애를 하나의 public surface로 번역하고, recovery 이후에도 같은 public API shape를 유지한다.
