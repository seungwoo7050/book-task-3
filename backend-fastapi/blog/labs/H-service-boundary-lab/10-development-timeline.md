# H-service-boundary-lab 개발 타임라인

## 1. 문제 정의만 보면 두 서비스 분리 입문 랩이다

`problem/README.md`는 범위를 아주 분명하게 잡고 있었다. 인증과 워크스페이스 도메인을 처음 분리하고, `identity-service`가 발급한 토큰 claims만으로 `workspace-service`가 동작하는지 보는 랩이다. 제외 범위도 분명했다. 이벤트 브로커, edge gateway, websocket은 아직 넣지 않는다.

처음에는 이 문장을 그대로 따라가면 될 것 같았다. 그런데 실제 `fastapi/` 아래를 열어 보자마자 그렇게 읽기에는 소스가 더 넓었다. `gateway/`, `services/notification-service/`, `contracts/README.md`까지 함께 들어 있었다. 이 랩을 좋은 문서로 바꾸려면 먼저 "문제 정의의 최소 범위"와 "repo 안에 미리 심어진 확장 seam"을 분리해서 읽어야 했다.

## 2. 실제로 올라오는 런타임은 두 서비스뿐이었다

그 분리를 가장 먼저 확인한 파일은 `fastapi/compose.yaml`이었다. 여기서 올라오는 컨테이너는 `identity-service`와 `workspace-service` 두 개뿐이다. 포트도 각각 `8111`, `8011`로 분리돼 있고, DB URL도 `IDENTITY_DATABASE_URL`, `WORKSPACE_DATABASE_URL`로 갈라져 있다. 문제 정의의 핵심 문장인 "서로의 DB를 읽지 않는다"는 선언이 단지 설명 문장이 아니라 런타임 토폴로지에 바로 반영돼 있었다.

반대로 같은 폴더에 있는 `gateway`와 `notification-service`는 이 compose 경로에 포함되지 않았다. 그래서 이 랩의 현재 답을 설명할 때는, repo에 더 많은 코드가 있다는 이유만으로 그것까지 "현재 구현"으로 묶으면 안 됐다. 지금 검증 가능한 런타임 경계는 두 서비스 분리까지다.

## 3. 사용자 정보 전달은 claims 하나로 고정돼 있었다

다음으로 확인한 것은 `identity-service`가 어떤 계약을 발급하는가였다. `services/identity-service/app/api/v1/routes/auth.py`와 `app/domain/services/auth.py`를 보면 회원가입, 이메일 검증, 로그인, 리프레시를 거쳐 access token을 발급한다. 이 토큰에는 `sub`, `handle`, `email`, `display_name`, `type`, `iss`, `iat`, `exp`가 들어간다.

중요한 건 그 다음 단계였다. `services/workspace-service/app/api/deps.py`의 `get_current_claims()`는 Bearer 토큰을 받아 자기 서비스 안에서 바로 `decode_access_token()`을 호출한다. 즉, `workspace-service`가 어떤 workspace를 만들 때마다 identity DB를 조회하는 방식이 아니다. 인증 서비스가 토큰을 만들고, 워크스페이스 서비스는 토큰 claims만 계약으로 받아서 자신의 정책을 실행한다.

이 지점이 이 랩의 첫 번째 경계선이다. "인증은 identity-service의 책임, 도메인 정책은 workspace-service의 책임"이라는 구분이 말뿐이 아니라 코드 경로로도 유지된다.

## 4. workspace 도메인은 자기 DB만으로 흐름을 이어 갔다

그 다음엔 `services/workspace-service/app/domain/services/platform.py`와 `tests/integration/test_workspace_service.py`를 기준으로, 워크스페이스 쪽 흐름이 정말 자기 저장소만으로 닫히는지 확인했다.

여기서 보인 흐름은 꽤 선명했다.

- `create_workspace()`는 claims의 `sub`, `email`을 받아 workspace와 owner membership을 만든다.
- `invite_member()`는 owner role을 확인한 뒤 invite를 발급한다.
- `accept_invite()`는 invite email과 claims email이 같은지 검사하고 membership을 만든다.
- `create_project()`, `create_task()`, `create_comment()`는 모두 membership을 먼저 확인한 뒤 도메인 객체를 저장한다.

이 흐름에서 인증 서비스 쪽 DB를 직접 읽는 코드는 나오지 않는다. 사용자 식별은 토큰 claims, 권한 판정은 workspace DB의 membership 레코드라는 식으로 역할이 분리돼 있다. 이게 바로 "cross-DB를 하지 않으면서도 업무 흐름을 유지할 수 있는가"라는 문제 정의에 대한 현재 구현의 답이었다.

다만 여기서 문서가 한 번 더 선을 그어야 했다. 위에 적은 invite, project, task, comment, outbox 흐름은 `workspace-service` 자체를 붙잡는 integration test와 domain service source에서 아주 선명하게 보인다. 반면 top-level `tests/test_system.py`가 실제로 잠그는 것은 register -> verify -> login -> workspace create까지다. 즉 "경계 설계가 어디까지 구현돼 있는가"와 "이번 랩의 시스템 검증이 어디까지 직접 보장하는가"는 같은 문장이 아니다.

## 5. 그런데 코드 안에는 이미 다음 단계의 seam도 들어와 있었다

여기서 끝나면 정말 깔끔한 입문 랩인데, 실제 코드는 거기서 한 발 더 나가 있었다. `create_comment()`는 comment를 저장한 뒤 다른 멤버마다 `OutboxEvent`를 `queued` 상태로 남긴다. `relay_outbox()`는 pending outbox를 읽어 Redis Stream으로 넘기고 상태를 `relayed`로 바꾼다. `contracts/README.md`는 아예 `comment.created.v1`의 source/sink를 `workspace-service -> notification-service`로 적어 두고 있었다.

이 흔적은 중요했다. 왜냐하면 문제 정의는 이벤트 브로커를 제외 범위로 잡고 있기 때문이다. 그래서 문서에서는 이 부분을 "현재 H 랩의 검증된 핵심"이 아니라 "이미 심어진 다음 seam"으로 정리했다. 실제 top-level compose와 smoke/system 테스트는 여전히 identity와 workspace 두 서비스만 사용한다. 하지만 repo 수준에서는 다음 랩으로 이어질 outbox/event 통로가 이미 들어와 있다.

`gateway`도 비슷했다. `gateway/app/api/v1/routes/auth.py`, `platform.py`를 보면 public API 모양을 유지하려는 의도가 보인다. 다만 이 랩의 compose에서는 gateway를 띄우지 않고, system test도 `8111`, `8011` 포트로 직접 붙는다. 그래서 gateway는 이 랩의 "현재 진입점"이 아니라 "향후 public edge 정리용 코드"에 가깝다.

## 6. 검증은 두 층으로 나뉘었다

검증은 소스 읽기만으로 끝내지 않고 명령을 다시 돌려 확인했다.

먼저 `make lint`는 통과했다. 최소한 이 랩의 현재 Python 소스는 정적 검사 기준에서는 깨지지 않았다.

반면 `make test`는 통과하지 못했다. top-level Makefile이 `services/identity-service` 테스트부터 시작하는데, 로컬 `python3` 환경에서 `argon2`가 없어 `ModuleNotFoundError: No module named 'argon2'`로 멈췄다. 이 실패는 서비스 경계 설계가 틀렸다는 신호라기보다, host 환경이 이 랩의 Python dependency를 아직 다 갖추지 못했다는 신호에 가깝다.

그래도 런타임 경계가 실제로 연결되는지는 compose 기반 경로로 다시 확인할 수 있었다. `make smoke`는 통과했고, `python3 -m pytest tests/test_system.py -q`도 최종적으로 통과했다. 이 system test는 다음 순서로 움직인다.

1. `identity-service`에 register
2. debug mailbox에서 verify token 조회
3. verify-email
4. login으로 access token 획득
5. 그 access token을 `workspace-service`에 넘겨 workspace 생성

즉, 이 랩의 최소 성공 조건인 "토큰은 identity가 만들고, workspace는 claims만으로 생성된다"는 실제 명령 재실행으로 확인됐다.

여기서 더 나아가 invite/project/comment/outbox까지 한 번에 top-level system proof로 읽으면 과장에 가깝다. 그 deeper 흐름은 별도의 `services/workspace-service/tests/integration/test_workspace_service.py`가 더 직접적으로 고정한다. 이번 보강에서는 그래서 검증 층위를 두 개로 나눴다. compose 기반 system proof는 두 서비스 경계의 최소 성공 루프, service-local integration proof는 workspace 도메인 내부 정책과 outbox seam이다.

중간에 `tests/test_system.py`를 한 번 단독 재실행했을 때는 `0.0.0.0:8011` 포트 충돌로 실패했다. 그때는 이전 smoke 재실행에서 남아 있던 compose 스택이 포트를 점유하고 있었고, 정리 후 다시 돌렸을 때 통과했다. 이 실패는 코드 결함이라기보다 실행 환경 정리 문제로 보는 편이 정확했다.

## 7. 이 랩을 지금 시점에서 어떻게 읽어야 하는가

이 랩을 "MSA 전체 그림"으로 읽으면 오히려 흐려진다. 실제로 검증된 답은 더 작고 더 명확하다.

- 인증과 워크스페이스 도메인을 분리한다.
- 사용자 전달은 claims 계약으로 고정한다.
- 각 서비스는 자기 DB만 읽는다.
- 그 위에 gateway, notification, event relay seam이 자라날 자리를 미리 남긴다.

좋은 문서가 되려면 바로 이 크기를 지켜야 했다. 문제 정의보다 더 앞서 있는 코드 흔적을 숨길 필요는 없지만, 그렇다고 그 흔적을 현재 랩의 완료 범위처럼 과장해서도 안 된다. H 랩의 핵심은 화려한 분산 시스템이 아니라, 첫 경계선 하나를 무너지지 않게 고정하는 데 있다.
