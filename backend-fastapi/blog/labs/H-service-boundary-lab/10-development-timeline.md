# H-service-boundary-lab: 공유 DB를 끊고, identity와 workspace를 claims로만 이어 보기

이 글은 `labs/H-service-boundary-lab/README.md`, `problem/README.md`, `docs/README.md`, `labs/H-service-boundary-lab/fastapi/compose.yaml::__compose__`, `labs/H-service-boundary-lab/fastapi/tests/test_system.py::test_identity_token_then_workspace_creation`, `backend-fastapi/docs/verification-report.md`를 바탕으로 실제 구현 순서를 다시 복원한다.

H 랩을 읽을 때 가장 먼저 해야 할 일은 '폴더에 무엇이 있는가'보다 '무엇이 실제로 실행되는가'를 구분하는 것이다. README.md와 problem/README.md는 identity와 workspace 경계만을 핵심으로 잡고, compose.yaml도 실제 runtime을 두 서비스로 제한한다. 그래서 이 글도 MSA 전체를 소개하는 대신, 가장 작은 서비스 분해가 어디까지 가능한지에 집중한다.

## 1. 서비스 분리를 기능 추가가 아니라 경계 선택 문제로 보기
문제 정의부터 굉장히 좁다. 핵심 질문은 gateway도, 이벤트 브로커도, websocket도 아니다. 그보다 먼저 'identity-service가 token을 발급하고, workspace-service가 그 claims만으로 workspace를 만들 수 있는가'가 성공 기준으로 들어온다. 서비스 분해를 시작할 때 일부러 범위를 줄인 셈이다.

## 2. compose runtime을 두 서비스로 제한하기
이 태도는 compose에서 더 분명해진다. 실제 runtime에는 identity-service와 workspace-service 두 개만 올라오고, 각자 자기 DB volume을 가진다. 폴더에는 더 많은 디렉터리가 남아 있지만, 이 랩의 독립 프로젝트 범위는 compose가 결정한다. 블로그가 source-first여야 하는 이유가 정확히 여기 있다.

```yaml
services:
  identity-service:
    build:
      context: ./services/identity-service
    env_file:
      - .env
    environment:
      DATABASE_URL: ${IDENTITY_DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
      TOKEN_ISSUER: ${TOKEN_ISSUER}
    ports:
      - "8111:8000"
    command: >
      sh -c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    volumes:
      - ./services/identity-service:/app
      - identity_data:/data
    healthcheck:
      test:
        [
          "CMD-SHELL",
          "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health/live')\"",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
```

이 장면이 보여 주는 건 실제 runtime이 identity-service와 workspace-service 두 개로 닫힌다는 사실이다.

## 3. system test로 claims-only 협업을 고정하기
system test도 그 최소 증명을 따른다. test_identity_token_then_workspace_creation은 identity-service에 register/verify/login을 수행한 뒤, 반환된 access token을 workspace-service /internal/workspaces 호출에 그대로 넘긴다. 그 뒤에 성공한 workspace 이름만 확인한다. 공유 ORM도, cross-DB join도 없다. 이 시나리오 하나가 경계 선택의 핵심을 대신 설명한다.

```python
def test_identity_token_then_workspace_creation() -> None:
    with compose_stack():
        identity = httpx.Client(base_url="http://127.0.0.1:8111/api/v1", timeout=10.0)
        workspace = httpx.Client(base_url="http://127.0.0.1:8011/api/v1", timeout=10.0)

        register = identity.post(
            "/internal/auth/register",
            json={"handle": "owner", "email": "owner@example.com", "password": "super-secret-1"},
        )
        assert register.status_code == 200
        verify = identity.post("/internal/auth/verify-email", json={"token": _latest_token("owner@example.com")})
        assert verify.status_code == 200
```

테스트는 identity에서 받은 claims만으로 workspace를 만드는 최소 협업 경계를 증명한다.

## 4. 2026-03-10 재검증으로 MSA 시작점을 닫기
검증 보고서에 따르면 2026-03-10에 lint, service unit test, system test, smoke가 다시 통과했다. 이 기록이 중요한 이유는 H 랩이 나중의 I/J/K/v2를 위한 출발점이기 때문이다. 가장 작은 경계 선택이 실제로 돌아간다는 사실이 먼저 있어야, 이후 복잡성을 더해도 비교가 가능해진다.

```bash
make lint
make test
make smoke
docker compose up --build
```

2026-03-10에 lint, service unit test, system test, smoke가 통과했다. 이 랩은 폴더 안의 모든 서비스 디렉터리가 아니라 compose와 system test가 실제 범위를 결정한다.

## 정리
H 랩의 가치는 기능이 적다는 데 있지 않다. 오히려 그 반대다. 기능을 일부러 덜 싣고 나니, 어디서 경계를 끊는지와 claims가 왜 경계 계약이 되는지가 훨씬 또렷하게 보인다. 이것이 이후 이벤트 통합과 gateway 도입을 설명하는 바닥선이 된다.
