# workspace-backend 개발 타임라인

이 capstone에는 랩처럼 "문제 하나, 기법 하나"의 깔끔한 단선형 서사가 없다. 대신 `problem/README.md`, `fastapi/app`, `tests/integration/test_capstone.py`, 실제 재실행 결과를 함께 보면, 단일 백엔드 기준선이 어떤 순서로 봉합되었는지는 꽤 분명하게 복원된다.

## 1. 출발점은 기능 추가가 아니라 기준선 만들기였다

문제 정의는 처음부터 기능 카탈로그가 아니다. `workspace-backend`는 인증, 인가, 데이터 API, 비동기 알림, 실시간 전달을 한 협업형 SaaS 백엔드로 "다시 조합"하는 프로젝트라고 선언한다. 그래서 첫 단계의 핵심은 랩 코드를 공용 패키지로 추출하는 것이 아니라, 어떤 조합을 보여 줄지 범위를 다시 고르는 일이었다.

이 선택은 앱 초기화 코드에서도 드러난다. `app/main.py`는 앱 시작 시 `initialize_schema()`를 호출하고, `app.state.mailbox`, `connection_manager`, `presence_tracker`를 직접 붙인다. 운영 배포보다 로컬 학습과 반복 실행을 우선한 셈이다. v1 기준선으로서의 단순함은 여기서부터 의도적으로 확보된다.

## 2. 인증은 로컬과 Google을 같은 사용자 모델에 우겨 넣는 대신, 토큰 경계를 분명히 남겼다

`app/domain/services/auth.py`를 보면 local register/login과 Google login이 결국 같은 `User`와 `ExternalIdentity` 모델로 수렴한다. local register는 mailbox에 verification token을 남기고, Google login은 이미 검증된 사용자처럼 처리해 바로 session을 발급한다. 둘 다 마지막엔 `issue_session()`으로 들어가 access token, refresh token, CSRF token을 같이 만든다.

여기서 중요한 건 "로그인 수단이 둘"이라는 사실보다, 둘이 같은 세션 규약으로 닫힌다는 점이다. `auth.py` route도 이 구조를 그대로 노출한다. 다만 보안 설계가 다 끝난 것은 아니다. refresh rotation과 CSRF 검사는 구현돼 있지만, 통합 테스트는 `register -> verify-email -> login -> me`와 `google/login`을 중심으로 흐르고 refresh/logout을 끝까지 검증하지는 않는다. 그리고 `RateLimiter` 클래스가 따로 있어도 실제 route에 연결돼 있지 않으니, 인증 hardening이 끝난 프로젝트처럼 읽으면 안 된다.

## 3. 플랫폼 경계는 CRUD 확장이 아니라 membership guard가 어디에 붙는지로 읽어야 한다

`app/api/v1/routes/platform.py`와 `app/domain/services/platform.py`는 이 capstone의 진짜 중심이다. surface만 보면 `workspaces`, `invites`, `projects`, `tasks`, `comments`, `notifications/drain`, `presence`, `ws/notifications`가 한 파일에 몰려 있다. 이게 거칠어 보일 수도 있지만, v1 기준선의 목적에는 맞다. auth 뒤에 오는 협업 흐름을 한 파일에서 끝까지 추적할 수 있기 때문이다.

실제 핵심은 모든 쓰기 연산이 membership guard를 어떻게 통과하는가에 있다.
- workspace 생성 시 owner membership을 즉시 만든다.
- invite 생성은 owner만 허용한다.
- invite 수락은 `invite.email == actor.email`일 때만 membership으로 변환된다.
- project, task, comment 생성은 모두 `_require_member()`를 거친다.

즉, 이 프로젝트는 "워크스페이스 권한 모델이 있다"는 문장보다, comment를 쓰는 순간까지 membership 규칙이 실제로 따라붙는다는 점에서 의미가 있다.

## 4. comment는 이 capstone에서 가장 중요한 전환점이다

`create_comment()`는 댓글 하나를 저장하는 함수처럼 보이지만, 실제로는 세 개의 경계를 한 번에 묶는다.
- 데이터 API: `Comment` row를 저장한다.
- 비동기 알림: 같은 workspace의 다른 멤버에게 `Notification(status="queued")`를 만든다.
- 실시간 전달 준비: drain 단계에서 WebSocket fan-out 할 payload의 원천을 만든다.

여기서 의도적으로 단순화한 지점도 분명하다. outbox, retry, broker, consumer receipt는 없다. queued notification은 DB row일 뿐이고, `POST /notifications/drain`을 호출해야만 `status="sent"`로 넘어간다. 다시 말해, 이 capstone은 "알림을 백그라운드에서 알아서 흘리는 시스템"이 아니라 "write path가 다음 단계 경계를 어디서 필요로 하는지 보여 주는 기준선"이다.

## 5. 실시간과 presence는 가능한 한 작은 메모리 모델로 남겨 두었다

`app/runtime.py`는 `ConnectionManager`와 `PresenceTracker` 두 클래스로 끝난다. user_id별 WebSocket 집합을 메모리에 들고 있고, heartbeat의 마지막 시각을 `time.monotonic()`으로 저장한다. `platform.py`의 WebSocket route는 access token을 query parameter로 받아 decode하고, connect 시 heartbeat를 찍고, receive loop 동안 heartbeat를 갱신한다.

이 설계는 작지만 중요한 사실을 드러낸다. v1 기준선에서 실시간은 "동작은 한다" 수준까지는 구현됐지만, 멀티 인스턴스 fan-out, broker 기반 전달, reconnect 정책, durable delivery는 아직 없다. presence도 TTL 기반 온라인 표시일 뿐이다. 바로 이 단순함 때문에 이후 MSA 버전에서 무엇이 비싸지는지 비교할 수 있다.

## 6. 운영 신호도 최소 기준선만 남겼다

`/api/v1/health/live`는 항상 `ok`를 반환하고, `/api/v1/health/ready`는 DB `SELECT 1`과 선택적 Redis `ping()`만 확인한다. Compose 역시 API, Postgres, Redis 세 컨테이너로 닫힌다. JSON logging formatter는 있지만 payload는 `timestamp`, `level`, `logger`, `message` 정도만 담고, K-lab에서 봤던 request correlation 수준까지는 가지 않는다.

이 역시 부족함이 아니라 의도된 위치다. 이 capstone은 단일 앱 기준선이므로, 분산 운영성보다는 통합 도메인 경계를 먼저 설명하는 데 초점을 둔다.

## 7. 통합 테스트는 이 기준선을 한 사용자 이야기로 고정한다

`tests/integration/test_capstone.py`는 owner와 collaborator를 두 클라이언트로 분리해 놓고, 아래 순서를 끝까지 밀어 붙인다.
1. owner 로컬 가입
2. mailbox에서 verification token 꺼내 메일 인증
3. owner 로컬 로그인
4. collaborator Google 로그인
5. owner workspace 생성
6. owner가 collaborator 이메일로 invite 발송
7. collaborator가 invite 수락
8. owner가 project, task, comment 생성
9. owner가 `notifications/drain` 호출
10. collaborator WebSocket이 "New comment on task..." 메시지를 수신

이 테스트가 보여 주는 건 "기능이 많다"가 아니다. 서로 다른 인증 수단으로 들어온 두 사용자가 하나의 workspace 규칙 아래에서 협업하고, comment write path가 알림과 실시간 전달까지 밀고 간다는 사실이다. 이게 v1 기준선의 핵심 가치다.

## 8. 이번 재실행은 코드보다 환경이 먼저 어긋난다는 사실을 드러냈다

이번 턴에서 canonical verification을 다시 돌린 결과는 아래와 같았다.

```bash
make lint
# All checks passed!

make test
# ModuleNotFoundError: No module named 'app'

make smoke
# ModuleNotFoundError: No module named 'fastapi'

python3 -m pytest tests/integration/test_capstone.py -q
# ModuleNotFoundError: No module named 'fastapi'
```

즉, 현재 호스트 환경에서는 lint만 곧바로 닫히고, test는 import path가, smoke와 추가 pytest 실행은 interpreter dependency가 막고 있다. 더 정확히 말하면 `fastapi/README.md`가 적어 둔 `.venv -> make install -> make test/smoke` bootstrap을 생략한 bare rerun이기 때문에 `app` import와 FastAPI dependency가 동시에 어긋난다. 이건 문서가 감춰야 할 흠이 아니라 지금 이 프로젝트를 다시 실행하는 사람이 가장 먼저 마주칠 사실이다.

## 정리

`workspace-backend`는 단일 FastAPI 앱 안에서 모든 문제를 해결한 프로젝트가 아니다. 대신 어떤 경계는 한 앱 안에 합쳐도 되고, 어떤 경계는 여전히 수동 drain, 메모리 WebSocket, 최소 readiness로 남겨 둬야 비교가 쉬운지를 정리한 기준선이다. 다음 `workspace-backend-v2-msa`를 읽을 때 중요한 건 기능 추가 목록이 아니라, 바로 이 기준선에서 어떤 단순함을 포기하게 되는지다.
