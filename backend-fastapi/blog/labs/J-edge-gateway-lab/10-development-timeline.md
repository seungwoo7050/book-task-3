# J-edge-gateway-lab 개발 타임라인

## 1. 이번 랩의 질문은 "서비스를 더 나누자"가 아니라 "밖에서는 하나처럼 보이게 하자"였다

`problem/README.md`는 처음부터 초점을 분명하게 잡고 있었다. 서비스가 분리된 뒤에도 외부 클라이언트는 하나의 API만 보고 싶고, gateway가 `/api/v1/auth/*`, `/api/v1/platform/*` shape를 유지해야 한다. 쿠키와 CSRF는 edge에만 두고, 내부 서비스에는 request id와 bearer token만 전달한다.

즉, 이 랩은 새로운 도메인 기능을 넣는 단계가 아니다. 오히려 이전 랩들에서 흩어진 기능을 브라우저 관점에서 다시 한 장의 표면으로 정리하는 단계다.

## 2. 실제 compose 런타임도 그 의도를 그대로 보여 줬다

`fastapi/compose.yaml`을 열어 보면 제일 앞에 `gateway`가 있고, 뒤에 `identity-service`, `workspace-service`, `notification-service`, `redis`가 따라온다. 호스트에서 public 포트로 열리는 건 `8013`의 gateway다. 나머지 서비스들도 각각 `8121`, `8122`, `8123`으로 열려 있지만, 이건 주로 내부 검증과 학습용이고 외부 클라이언트의 기준점은 gateway 하나다.

이 배치는 문서 논지를 정하는 데 중요했다. 이전 랩들에서는 내부 서비스가 직접 주인공이었다면, J 랩에서는 내부 서비스들이 그대로 있어도 브라우저는 그것들을 직접 상대하지 않는다는 점이 핵심이다.

## 3. 인증 세션 상태는 edge에만 남고, 내부 auth는 토큰 묶음만 반환했다

이 랩을 읽으면서 가장 먼저 분리해야 했던 것은 "누가 로그인 자체를 처리하는가"와 "누가 세션 상태를 브라우저에 남기는가"였다.

`services/identity-service/app/api/v1/routes/auth.py`를 보면 내부 로그인 API는 `access_token`, `refresh_token`, `csrf_token`, `user`를 JSON bundle로 반환한다. 여기서는 `Set-Cookie`를 만들지 않는다.

반면 `gateway/app/api/v1/routes/auth.py`의 `/login`, `/google/login`, `/token/refresh`, `/logout`는 내부 identity API를 호출한 뒤 응답 쿠키를 직접 다룬다.

- login/google login: gateway가 `access_token`, `refresh_token`, `csrf_token` 쿠키를 설정한다.
- refresh/logout: gateway가 쿠키를 읽고 CSRF를 검증한 뒤 내부 identity API를 호출한다.

이 구조 덕분에 브라우저 상태는 gateway에만 머물고, 내부 인증 서비스는 "토큰 발급기" 역할에 더 가깝게 정리된다. 이 차이를 분명히 적어 두지 않으면, 왜 edge가 필요한지 설명이 흐려진다.

## 4. platform 쪽에서는 쿠키를 다시 bearer 계약으로 번역했다

다음으로 본 곳은 `gateway/app/api/deps.py`와 `gateway/app/api/v1/routes/platform.py`였다. 여기서 흥미로운 점은 gateway가 브라우저 친화적인 상태를 그대로 내부 서비스에 넘기지 않는다는 것이다.

`get_current_claims()`는 gateway 쿠키에 있는 access token을 읽어 현재 사용자를 확인한다. 그리고 platform route의 `_auth_headers()`는 같은 access token을 다시 `Authorization: Bearer ...` 형태로 바꿔 `workspace-service`에 전달한다.

즉, public edge에서는 쿠키, internal contract에서는 bearer라는 두 언어가 분리돼 있다. 이 랩의 좋은 지점은 이 번역이 명시적으로 드러난다는 데 있다. 브라우저가 다루기 쉬운 상태와 서비스가 다루기 쉬운 계약을 일부러 다르게 유지한다.

다만 이 설명도 경로별로 조금 더 세밀하게 적어야 한다. `create_workspace`, `invite_member`, `create_project`, `create_task`, `create_comment`, `accept_invite` 같은 route는 실제로 `get_current_claims()`와 `_auth_headers()`를 함께 타지만, `/notifications/drain`은 현재 그 dependency를 직접 걸지 않고 내부 `/internal/events/relay`, `/internal/notifications/consume` 두 호출을 orchestration하는 예외 route다. 이번 system test는 authenticated client로 이 경로를 밟지만, route 보호 자체를 별도 assert하지는 않는다.

## 5. request id 전파는 테스트보다 코드 경로가 더 직접적인 근거였다

문제 정의의 성공 기준 중 하나는 내부 호출에 `X-Request-ID`가 전달되는 것이다. 이번에는 이 부분을 테스트 결과보다 소스 경로로 확인하는 편이 더 정확했다.

`gateway/app/main.py` middleware는 들어온 요청에서 `X-Request-ID`를 읽거나 새 UUID를 만들고, `request.state.request_id`에 넣은 뒤 응답 헤더에도 같은 값을 넣는다. 그리고 `gateway/app/runtime.py`의 `ServiceClient.request()`는 모든 upstream 요청 헤더에 `X-Request-ID: request.state.request_id`를 자동으로 추가한다.

내부 `identity-service`, `workspace-service`, `notification-service`의 `app/main.py`들도 모두 같은 패턴으로 요청 헤더의 `X-Request-ID`를 읽어 response header에 다시 넣는다.

이 전파는 이번 system test에서 직접 assert되지는 않았다. 그래서 문서에서는 "테스트로 검증됨"이 아니라 "코드 경로로 확인한 source-based inference"로 다루는 편이 맞았다. 그래도 문제 정의의 요구 자체는 코드 상에서 분명히 충족되고 있다.

## 6. gateway는 단순 프록시가 아니라 복구 시나리오의 외부 표면도 맡았다

`tests/test_system.py`가 보여 준 건 단순 로그인 프록시보다 훨씬 흥미로운 흐름이었다. 이 테스트는 owner와 collaborator 두 클라이언트를 모두 gateway base URL `http://127.0.0.1:8013`로만 다룬다.

흐름은 다음과 같다.

1. owner가 `/api/v1/auth/register`, `/verify-email`, `/login`
2. collaborator가 `/api/v1/auth/google/login`
3. owner가 `/api/v1/platform/workspaces`, `/invites`, `/projects`, `/tasks`, `/comments`
4. collaborator는 gateway websocket `/api/v1/platform/ws/notifications`에 붙어 알림을 기다림
5. owner가 `/api/v1/platform/notifications/drain`을 호출하면 첫 알림이 websocket으로 도착
6. 테스트가 `notification-service`를 직접 중지
7. owner가 두 번째 comment를 만든 뒤 다시 drain을 호출하면 gateway는 `503`을 반환
8. `notification-service`를 다시 올리고 recovery drain을 호출하면 두 번째 알림이 websocket으로 도착

이 시나리오 덕분에 gateway의 역할이 아주 선명해졌다. gateway는 단순히 path만 바꾸는 곳이 아니라, upstream 장애를 외부에 하나의 HTTP surface로 드러내고, 복구 뒤에도 같은 public route를 계속 유지하는 곳이다.

## 7. websocket edge는 Redis pub/sub와 내부 fan-out 위에 얹혀 있었다

이 랩에서 gateway는 HTTP만 하지 않는다. `gateway/app/runtime.py`의 `RedisNotificationRelay`는 Redis pub/sub를 구독하고, 들어온 메시지를 `ConnectionManager`가 가진 websocket 연결로 fan-out 한다. `platform.py`의 `/ws/notifications`는 access token query parameter를 decode해 사용자별 websocket 연결을 연다.

즉, gateway는 단순 API 집합이 아니라 브라우저와 가장 가까운 실시간 edge 역할까지 맡는다. 다만 중요한 건, 이 websocket edge의 인증도 HTTP와 완전히 같지는 않다는 점이다. HTTP 쪽은 cookie+CSRF를 edge에 두지만, `/ws/notifications`는 access token query parameter를 직접 decode한다. gateway는 "브라우저에게 어떻게 보일 것인가"를 책임지지만, public edge 안에서도 transport별로 인증 매체가 다를 수 있다는 사실을 숨기지 않는 편이 정확하다.

## 8. 검증 결과는 다시 두 층으로 나뉘었다

이번에도 명령을 재실행해 현재 상태를 확인했다.

`make lint`는 통과했다. gateway와 세 내부 서비스, tests 전반에서 정적 검사는 깨지지 않았다.

반면 `make test`는 통과하지 못했다. `gateway`의 아주 단순한 health test조차 import 단계에서 공용 security 모듈을 타고 `argon2`를 요구하면서 `ModuleNotFoundError: No module named 'argon2'`가 발생했다. 테스트 내용 자체는 health/metrics 수준인데도, gateway가 auth 관련 security 모듈을 공용으로 가져가고 있어서 로컬 환경 dependency에 막힌다는 점이 드러났다.

compose 기반 검증은 살아 있었다. `make smoke`는 통과했고, `python3 -m pytest tests/test_system.py -q`도 통과했다. 특히 이 system test는 public route 유지, cookie 기반 세션, websocket 알림, notification-service 장애와 복구까지 한 번에 묶어 보여 주기 때문에 J 랩의 핵심 설계를 설명하는 가장 강한 근거였다.

## 9. 이 랩을 지금 시점에서 어떻게 읽어야 하는가

이 랩을 "API gateway 제품 흉내 내기"로 읽으면 초점이 어긋난다. 실제로 이 lab이 보여 주는 더 중요한 변화는 책임의 재배치다.

- 브라우저 상태는 gateway에 둔다.
- 내부 서비스는 bearer와 request id 같은 서비스 친화적 계약만 받는다.
- public API shape는 gateway가 유지한다.
- upstream 실패는 gateway가 하나의 외부 표면으로 번역한다.

그래서 J 랩은 기능을 더 붙이는 단계가 아니라, 외부 경험과 내부 구조를 다른 언어로 분리하는 단계라고 보는 편이 정확하다. 이 관점을 잡아 두면 뒤이은 distributed ops나 운영 실험도 훨씬 덜 헷갈린다.
