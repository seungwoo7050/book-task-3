# J-edge-gateway-lab 구조 계획

## 문서 목표

이 랩을 "edge gateway가 왜 필요한가"보다 한 단계 더 구체적으로, "브라우저 상태와 내부 서비스 계약을 어디서 분리할 것인가"를 설명하는 문서로 만든다. public API shape 유지, cookie/CSRF edge 집중, request id 전파, upstream failure 표면화를 같은 축으로 묶는다.

## 중심 논지

현재 검증된 핵심은 네 줄이다.

- 외부 클라이언트는 gateway 하나만 본다.
- 세션 상태는 gateway 쿠키와 CSRF에만 남는다.
- 내부 서비스는 bearer token과 `X-Request-ID`만 받는다.
- upstream 장애와 복구는 gateway가 하나의 public surface로 보여 준다.

## 본문 순서

1. 문제 정의에서 public API 유지 요구를 먼저 고정한다.
2. compose 런타임에서 gateway가 public entrypoint라는 점을 보여 준다.
3. gateway auth route와 internal identity route의 차이를 비교한다.
4. platform route가 cookie를 bearer로 번역하는 경로를 설명한다.
5. request id 전파는 테스트가 아니라 코드 경로 근거임을 분리해 적는다.
6. websocket + notification recovery system test를 통해 gateway의 외부 표면 역할을 보여 준다.
7. 실제 재실행 결과를 성공/실패로 기록한다.

## 반드시 포함할 근거

- `compose.yaml`의 gateway-first 구성
- gateway auth route의 cookie/CSRF 처리
- internal identity auth route의 JSON bundle 반환
- platform route의 `_auth_headers()` 번역
- gateway middleware와 `ServiceClient.request()`의 `X-Request-ID` 전파
- `tests/test_system.py`의 gateway-only client flow와 notification-service stop/start recovery
- `make lint`, `make test`, `make smoke`, `python3 -m pytest tests/test_system.py -q` 재실행 결과

## 반드시 피할 서술

- gateway가 circuit breaker나 service discovery까지 이미 해결한 것처럼 쓰지 않는다.
- request id 전파를 테스트가 보장한 사실처럼 과장하지 않는다.
- 내부 서비스가 여전히 브라우저 쿠키를 직접 읽는 것처럼 설명하지 않는다.
- 단순 프록시 수준의 얕은 설명으로 websocket/recovery 시나리오를 놓치지 않는다.

## 품질 체크

- chronology가 살아 있는가
- edge와 internal contract의 언어 차이가 드러나는가
- 검증된 사실과 source-based inference가 구분되는가
- 현재 한계와 제외 범위를 숨기지 않았는가
