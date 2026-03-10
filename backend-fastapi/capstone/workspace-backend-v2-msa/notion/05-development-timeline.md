# 개발 타임라인

## `2026-03-10` 오전: 구조를 먼저 고정했다

- `workspace-backend/`는 경로를 바꾸지 않고 v1 baseline으로 남기기로 결정했다.
- 새 비교 대상으로 `capstone/workspace-backend-v2-msa/`를 만들었다.
- v2의 기본 런타임 구조를 `gateway + identity-service + workspace-service + notification-service + redis`로 고정했다.

근거 파일:
- [../README.md](../README.md)
- [../fastapi/compose.yaml](../fastapi/compose.yaml)

## `2026-03-10` 낮: 기능보다 경계부터 옮겼다

- `identity-service`로 사용자, refresh token, email token 책임을 뺐다.
- `workspace-service`에 workspace, membership, invite, project, task, comment, outbox를 모았다.
- `notification-service`에는 notification 저장, idempotent receipt, Redis Streams consumer, pub/sub fan-out을 넣었다.
- `gateway`는 브라우저 쿠키, public REST shape 유지, websocket edge를 맡도록 정리했다.

근거 파일:
- [../fastapi/services/identity-service/app/api/v1/routes/auth.py](../fastapi/services/identity-service/app/api/v1/routes/auth.py)
- [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)
- [../fastapi/services/notification-service/app/domain/services/notifications.py](../fastapi/services/notification-service/app/domain/services/notifications.py)
- [../fastapi/gateway/app/api/v1/routes/platform.py](../fastapi/gateway/app/api/v1/routes/platform.py)

## `2026-03-10` 오후: H~K 랩과 공통 기준을 v2에 맞췄다

- 루트 README, 커리큘럼, repo standards를 `A~G -> capstone v1 -> H~K -> capstone v2` 흐름으로 바꿨다.
- H~K를 v2에서 파생한 MSA 브리지 랩으로 추가했다.
- copied Makefile을 `python -m pytest`, `python -m ruff` 기준으로 정리했다.
- `workspace-service` 설정과 테스트를 정리하면서 `access_token_ttl_seconds` 누락, 잘못된 UUID claim, Compose harness project name 충돌을 수정했다.
- `gateway`와 `workspace-service`에 `argon2-cffi`를 추가해 로컬 테스트와 컨테이너 의존성 차이를 줄였다.

증거 경로:
- [../../../README.md](../../../README.md)
- [../../../docs/labs-curriculum.md](../../../docs/labs-curriculum.md)
- [../../../docs/repo-standards.md](../../../docs/repo-standards.md)
- [../fastapi/Makefile](../fastapi/Makefile)
- [../fastapi/tests/compose_harness.py](../fastapi/tests/compose_harness.py)

## `2026-03-10` 저녁: 문서와 notion을 1차로 채웠다

- H~K와 v2의 `docs/README.md`를 개념 지도, 단순화 지점, 실행/검증 기준 중심으로 다시 썼다.
- H~K와 v2의 `notion/` 파일 세트를 문제 정의, 의사결정, 디버깅, 회고, 지식 인덱스, 타임라인 관점으로 확장했다.
- 새 프로젝트에는 `notion-archive/`를 만들지 않았다.

문서 근거:
- [../docs/README.md](../docs/README.md)
- [README.md](README.md)

## `2026-03-10` 밤: 1차 검증에서 Docker 문제가 먼저 드러났다

- service unit test는 통과했지만, fresh build 경로의 `docker pull` / `docker build`가 `python:3.12-slim` metadata 단계에서 멈추거나 containerd I/O 오류를 냈다.
- Docker Desktop을 재시작한 뒤 기존 local image를 검사했더니 `uvicorn`과 `pip` 엔트리포인트 파일이 0바이트였다.
- 이 문제를 숨기지 않기 위해 [02-debug-log.md](02-debug-log.md)와 [../../../docs/verification-report.md](../../../docs/verification-report.md)에 실제 장애 양상을 적었다.

실제 명령 메모:
- `docker compose up --build -d`
- `docker build --progress=plain -t workspace-v2-identity-fresh ./services/identity-service`
- `docker pull python:3.12-slim`

이때 배운 점:
- 분산 구조 학습에서는 코드 오류와 Docker 런타임 오류를 먼저 분리해야 한다.
- image corruption은 애플리케이션 로그가 아니라 entrypoint 파일 크기 확인으로 드러날 수 있다.

## `2026-03-10` 밤 늦게: 우회가 아니라 원인과 검증을 같이 남겼다

- Compose command와 Dockerfile CMD를 `uvicorn ...`에서 `python -m uvicorn ...`로 바꿨다.
- local image는 `ensurepip --upgrade --default-pip`와 `pip install --ignore-installed --no-cache-dir -e ".[dev]"`로 복구했다.
- 복구한 image를 기준으로 `docker compose -p workspace-backend-v2-msa-dd63448c -f compose.yaml up -d --no-build`를 실행했다.

근거 파일:
- [../fastapi/compose.yaml](../fastapi/compose.yaml)
- [../fastapi/gateway/Dockerfile](../fastapi/gateway/Dockerfile)
- [../fastapi/services/identity-service/Dockerfile](../fastapi/services/identity-service/Dockerfile)
- [../fastapi/services/workspace-service/Dockerfile](../fastapi/services/workspace-service/Dockerfile)
- [../fastapi/services/notification-service/Dockerfile](../fastapi/services/notification-service/Dockerfile)

## `2026-03-10` 최종 runtime 검증에서 실제로 확인한 흐름

아래 흐름은 [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)와 같은 사용자 여정을 기준으로 다시 확인했다.

1. owner 로컬 회원가입, 이메일 검증, 로그인
2. collaborator Google 스타일 로그인
3. workspace 생성, invite 발급, invite 수락
4. project/task/comment 생성
5. first drain 성공과 websocket notification 수신
6. notification-service 중단 중 second comment 저장 성공
7. recovery 후 re-drain 성공과 두 번째 websocket notification 수신

이 검증이 증명한 것:
- public route shape는 gateway에서 유지된다.
- 댓글 저장은 consumer 장애와 분리되어 성공할 수 있다.
- recovery 후 drain을 다시 호출하면 websocket fan-out까지 회복된다.

이 검증이 증명하지 않은 것:
- fresh image rebuild가 같은 날 안정적으로 성공했다는 사실
- 장시간 운영, 부하, 재배포까지 견딘다는 사실

## `2026-03-11` notion 2차 보강

- `01-approach-log.md`에 대안 비교 표와 재평가 신호를 추가했다.
- `04-knowledge-index.md`를 용어집 중심 문서에서 판단 규칙 중심 문서로 바꿨다.
- 이 타임라인도 “작업 순서”만이 아니라 “근거 파일과 실제 명령”을 같이 남기는 형태로 다시 썼다.

이번 보강의 목적:
- 나중에 구현 세부를 잊어도 “왜 이 선택을 했는가”와 “어떤 명령으로 어디까지 확인했는가”를 다시 추적할 수 있게 만들기 위함이다.

## 나중에 다시 볼 체크포인트

- fresh build 경로가 정상화되면 `docker compose up --build -d`와 `python -m tests.smoke`를 같은 날짜로 다시 기록한다.
- event versioning, retry policy, tracing backend는 v2 다음 확장 과제로 남겨 둔다.
