# workspace-backend-v2-msa: 단일 백엔드 기준선을 MSA로 다시 풀고, 장애 복구까지 public API로 증명하기

이 글은 `capstone/workspace-backend-v2-msa/README.md`, `problem/README.md`, `docs/README.md`, `capstone/workspace-backend-v2-msa/fastapi/compose.yaml::__compose__`, `capstone/workspace-backend-v2-msa/fastapi/tests/test_system.py::test_v2_system_flow_and_notification_recovery`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

v2 capstone을 읽을 때는 두 가지를 동시에 봐야 한다. 하나는 workspace-backend v1과 같은 public 협업 흐름을 gateway 아래에서 유지하는 일이고, 다른 하나는 notification-service 장애처럼 v1에는 없던 분산 실패 경로를 사실대로 드러내는 일이다. docs/README.md와 docs/verification-report.md가 둘 다 필요한 이유도 여기 있다.

## 1. v1 단일 백엔드 기준선을 다시 분해하기
출발점은 비교다. README는 v1과 같은 public /api/v1/auth/*, /api/v1/platform/*를 유지한다고 말하면서도, 내부는 identity, workspace, notification 세 서비스와 gateway로 나뉜다고 적는다. 즉 이 프로젝트는 새 도메인을 만드는 capstone이 아니라, 같은 도메인을 다른 경계로 다시 푸는 capstone이다.

## 2. gateway와 세 서비스의 runtime scope를 compose로 고정하기
runtime scope도 그 비교를 위해 분명히 고정된다. compose에는 gateway, identity-service, workspace-service, notification-service, redis가 모두 올라오고, 각자 live healthcheck를 갖는다. gateway route는 public path를 유지하면서 내부 서비스 URL로 fan-out 하고, browser cookie와 websocket edge를 자신에게 남긴다. 여기서부터 v1과의 차이가 물리적인 runtime으로 바뀐다.

```yaml
services:
  gateway:
    build:
      context: ./gateway
    env_file:
      - .env
    environment:
      SECRET_KEY: ${SECRET_KEY}
      TOKEN_ISSUER: ${TOKEN_ISSUER}
      IDENTITY_SERVICE_URL: http://identity-service:8000/api/v1
      WORKSPACE_SERVICE_URL: http://workspace-service:8000/api/v1
      NOTIFICATION_SERVICE_URL: http://notification-service:8000/api/v1
      REDIS_URL: ${REDIS_URL}
      REDIS_PUBSUB_CHANNEL: ${REDIS_PUBSUB_CHANNEL}
    depends_on:
      identity-service:
        condition: service_healthy
      workspace-service:
        condition: service_healthy
      notification-service:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8015:8000"
    command: >
      sh -c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    volumes:
```

이 장면은 gateway, identity, workspace, notification, redis가 비교 가능한 runtime을 어떻게 이루는지 보여 준다.

## 3. system test로 public flow와 recovery를 한 번에 묶기
system test는 그 차이를 가장 잘 보여 주는 증거다. owner는 로컬 회원가입/검증/로그인을 거치고, collaborator는 Google 로그인으로 들어온다. 둘은 gateway만 호출해 workspace, invite, project, task, comment 흐름을 끝낸다. 그리고 notification-service를 일부러 멈춘 뒤 두 번째 comment를 남겨 drain이 503으로 실패하는지, 복구 뒤 recovery drain으로 websocket 알림을 다시 받는지 확인한다. 이 시나리오는 v2가 단순 분해가 아니라 장애 경로까지 public flow로 끌어왔다는 사실을 보여 준다.

```python
def test_v2_system_flow_and_notification_recovery() -> None:
    with compose_stack() as project_name:
        owner = httpx.Client(base_url="http://127.0.0.1:8015", timeout=10.0)
        collaborator = httpx.Client(base_url="http://127.0.0.1:8015", timeout=10.0)

        register = owner.post(
            "/api/v1/auth/register",
            json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
        )
        assert register.status_code == 200
        verify = owner.post("/api/v1/auth/verify-email", json={"token": _latest_token("owner@example.com")})
        assert verify.status_code == 200
```

테스트는 public API, invite, comment, drain failure, recovery, websocket fan-out을 한 흐름으로 묶는다.

## 4. 2026-03-10 재검증과 fresh build 문제를 사실대로 남기기
마지막 검증 기록은 특히 중요하다. 2026-03-10 보고서는 service unit tests 통과는 명시하지만, fresh image rebuild는 Docker Desktop의 containerd 저장소 오류와 0-byte 실행 파일 문제 때문에 안정적인 성공 기록을 남기지 않았다고 분명히 적는다. 대신 재시작 후 prebuilt local image를 복구해 Compose stack을 올리고, end-to-end 협업 흐름과 recovery, websocket notification까지 실제로 다시 확인했다고 남긴다. 이 정직한 구분이야말로 v2 문서의 가장 강한 부분이다.

```bash
make test
docker compose up --build -d
docker build --progress=plain -t workspace-v2-identity-fresh ./services/identity-service
docker pull python:3.12-slim
docker compose -p workspace-backend-v2-msa-dd63448c -f compose.yaml up -d --no-build
inline Python end-to-end flow for register -> verify -> login -> invite -> comment -> drain -> recovery -> websocket
```

2026-03-10에 service unit tests는 통과했고, fresh build 경로는 Docker Desktop 문제로 성공 기록을 남기지 못했지만 prebuilt image 기준 Compose runtime과 end-to-end 협업 흐름 검증은 완료했다. 이 capstone은 성공 기록뿐 아니라 실패한 fresh build 경로를 숨기지 않는 점이 중요하다.

## 정리
v2 capstone은 MSA가 더 멋져 보인다는 이야기를 하지 않는다. 오히려 무엇이 더 복잡해졌는지, 어떤 실패 경로가 새로 생겼는지, 어떤 검증은 아직 불안정한지까지 같이 보여 준다. 그래서 이 시리즈의 끝점으로서 설득력이 있다. 결과 요약이 아니라 비교 가능한 증거 묶음으로 남기 때문이다.
