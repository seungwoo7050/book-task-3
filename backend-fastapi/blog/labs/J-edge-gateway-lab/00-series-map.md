# J-edge-gateway-lab 시리즈 맵

이 랩의 질문은 기능 추가가 아니다. 이미 분리된 `identity-service`, `workspace-service`, `notification-service`를 앞에 다시 하나의 얼굴로 세우는 방법이 핵심이다. gateway가 public API shape를 유지하고, 브라우저 상태는 edge에만 남기며, 내부 서비스에는 bearer token과 `X-Request-ID`만 넘기는 구조가 실제로 어떻게 굴러가는지를 추적한다.

## 이 랩에서 끝까지 붙잡은 질문

- 외부 클라이언트가 내부 서비스 포트를 몰라도 되게 만드는 경계는 어디인가
- 쿠키와 CSRF는 왜 gateway에만 둬야 하는가
- request id는 실제로 어디서 만들어지고 어떤 경로로 전달되는가
- upstream 장애가 생겼을 때 gateway는 어떤 실패를 외부에 보여 주는가

## 이 문서 묶음이 내린 현재 결론

- 검증된 public entrypoint는 `gateway` 하나다. system test도 끝까지 `http://127.0.0.1:8013`만 호출한다.
- 로그인 후 쿠키는 gateway가 세팅하고, 내부 `identity-service`는 JSON bundle만 반환한다.
- gateway의 platform route 대부분은 쿠키의 access token을 bearer header로 바꿔 `workspace-service`에 넘긴다. 다만 `/notifications/drain`은 현재 route-level `get_current_claims` dependency 없이 내부 relay/consume orchestration만 수행하는 예외 경로다.
- HTTP auth는 edge cookie 중심이지만, websocket edge는 `access_token` query parameter를 직접 받는다. 즉 public edge도 모든 경로가 같은 인증 매체를 쓰는 것은 아니다.
- `X-Request-ID` 전파는 테스트에서 직접 assert하지는 않지만, gateway middleware와 `ServiceClient.request()` 코드 경로로 확인된다.
- notification-service가 내려가면 gateway의 drain 엔드포인트는 `503`을 반환하고, 서비스 복구 뒤 같은 public 경로로 recovery를 이어 간다.

## 추천 읽기 순서

1. `10-development-timeline.md`
2. `_evidence-ledger.md`
3. `_structure-plan.md`

## 각 문서의 역할

- `10-development-timeline.md`: public edge, cookie/CSRF, request id 전파, websocket recovery 시나리오를 시간순으로 정리한다.
- `_evidence-ledger.md`: gateway와 내부 서비스의 경계 증거, system test, 검증 명령 결과를 모은다.
- `_structure-plan.md`: 이 랩을 "edge 책임 재배치" 문서로 읽기 위한 설명 순서를 남긴다.

## 이번에 다시 확인한 검증 스냅샷

- `make lint`: 통과
- `make test`: 로컬 `python3` 환경에서 gateway 테스트 import 단계에서 `ModuleNotFoundError: No module named 'argon2'`
- `make smoke`: 통과
- `python3 -m pytest tests/test_system.py -q`: 통과

이 랩의 핵심은 gateway가 모든 걸 대신하는 만능 제품이라는 데 있지 않다. 오히려 브라우저 상태와 내부 서비스 계약을 분리해서, public API와 internal API를 서로 다른 언어로 유지하는 데 있다.
