# 디버그 로그

## 1. copied Makefile이 실행 파일 경로에 직접 의존했다

- 증상: 서비스별 `make test`가 코드 문제가 아니라 깨진 `pytest` shebang 때문에 실패했다.
- 원인: copied Makefile이 `pytest`, `ruff` 실행 파일을 직접 호출하고 있었다.
- 수정: 새 MSA 트랙의 Makefile을 `python -m pytest`, `python -m ruff` 기준으로 다시 맞췄다.
- 효과: 루트 가상환경의 진입점 상태와 상관없이 동일한 명령으로 검증할 수 있게 됐다.

## 2. copied `workspace-service` 설정과 테스트가 경계 규칙과 맞지 않았다

- 증상: `Settings`에는 `access_token_ttl_seconds`가 빠져 있었고, service test는 `user-owner` 같은 비 UUID 값을 `sub` claim으로 써서 DB UUID column과 충돌했다.
- 수정: v2 기준 설정 필드를 복원하고, 테스트 토큰의 사용자 ID를 실제 UUID 문자열로 바꿨다.
- 효과: service test와 system test가 같은 claim 계약을 전제로 움직이게 됐다.

## 3. Compose 기반 system test 격리가 약했다

- 증상: 초기 harness는 초 단위 timestamp project name만 사용해서 병렬 검증 시 이름 충돌이 났다.
- 추가 문제: prefix에 대문자가 섞이면 Docker가 project name 자체를 거부했다.
- 수정: `ROOT.parent.name.lower() + UUID suffix` 조합으로 project name을 바꾸고, teardown의 `docker compose down`에는 timeout과 예외 무시를 넣었다.
- 효과: H~K와 v2가 같은 시점에 돌더라도 Compose 격리가 안정해졌다.

## 4. 컨테이너 의존성이 로컬 단위 테스트에 가려졌다

- 증상: `gateway`와 `workspace-service`가 `argon2.PasswordHasher`를 import하지만 Compose 빌드에서는 `ModuleNotFoundError`가 났다.
- 원인: 로컬 가상환경에는 패키지가 이미 설치돼 있어 문제가 숨겨졌다.
- 수정: `gateway`, `workspace-service`의 `pyproject.toml`에 `argon2-cffi`를 추가했다.
- 효과: Compose 환경과 로컬 테스트 환경의 차이를 줄였다.

## 5. 실제 장애 시나리오를 테스트에 넣어야 경계가 분명해졌다

- 상황: notification-service가 내려간 상태에서 drain을 호출하면 comment는 이미 생성됐지만 알림 소비는 실패할 수 있다.
- 수정: gateway client는 upstream request error를 503 `UPSTREAM_UNAVAILABLE`로 표준화했고, 복구 후 re-drain 경로를 system test에 넣었다.
- 효과: “comment 저장 성공”과 “notification 전달 성공”이 다른 사건이라는 점이 코드와 테스트에 같이 드러났다.

## 6. Docker 이미지가 조용히 손상되면 healthcheck보다 먼저 실행 명령이 사라질 수 있다

- 증상: `docker compose up -d --no-build`로 올린 컨테이너가 stderr도 남기지 않고 `Exited (0)` 상태가 됐다.
- 처음 의심한 것:
  - `uvicorn --reload`가 컨테이너 환경과 충돌했는지
  - healthcheck가 너무 빨라 프로세스를 죽였는지
  - compose dependency chain이 gateway 시작을 막았는지
- 실제 원인: local image 안의 `/usr/local/bin/uvicorn`, `site-packages/uvicorn/__main__.py`, `site-packages/pip/__main__.py`가 모두 0바이트였다. 즉, 런타임 명령 자체와 패키지 엔트리포인트가 손상된 이미지가 남아 있었다.
- 확인 순서:
  - `docker inspect`로 컨테이너 `Cmd`를 확인했다.
  - `docker run --rm ... sh -lc 'ls -l $(which uvicorn)'`와 Python snippet으로 파일 크기를 읽었다.
  - `uvicorn`뿐 아니라 `pip`도 0바이트라는 점을 보고 image corruption으로 결론냈다.
- 코드 수정:
  - H~K와 v2의 Compose command / Dockerfile CMD를 `uvicorn ...`에서 `python -m uvicorn ...`로 바꿨다.
  - 이 수정은 entrypoint script가 깨져도 모듈 실행 경로로 우회할 수 있게 하려는 목적이다.
- 로컬 복구:
  - `ensurepip --upgrade --default-pip`로 `pip`를 다시 설치했다.
  - 각 서비스 image에 대해 `pip install --ignore-installed --no-cache-dir -e ".[dev]"`를 다시 실행했다.
  - 복구한 image를 commit해서 같은 tag로 덮어썼다.
- 검증:
  - 복구 후 모든 서비스가 healthy 상태로 유지되는지 확인했다.
  - owner register -> verify -> login, collaborator Google login, invite accept, comment 저장, notification-service stop/start, recovery drain, websocket 수신까지 실제로 다시 확인했다.
