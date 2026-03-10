# 검증 보고서

- 마지막 기록된 검증 실행일: `2026-03-10`
- 문서 갱신일: `2026-03-10`
- 문서 갱신 범위: MSA 학습 트랙 H~K 추가, capstone v2 추가, 실제 재실행 결과 반영
- 주의: 이 문서는 날짜별로 실제 실행한 결과만 적습니다. 다시 실행하지 않은 경로는 이전 기록을 유지합니다.

## 이번에 재실행한 기준 경로

- GitHub Actions 워크플로우: [.github/workflows/labs-fastapi.yml](../.github/workflows/labs-fastapi.yml)
- `2026-03-10` 대상:
  - `labs/H-service-boundary-lab/fastapi`
  - `labs/I-event-integration-lab/fastapi`
  - `labs/J-edge-gateway-lab/fastapi`
  - `labs/K-distributed-ops-lab/fastapi`
  - `capstone/workspace-backend-v2-msa/fastapi`
- `2026-03-09` 대상:
  - `labs/A-auth-lab/fastapi` ~ `labs/G-ops-lab/fastapi`
  - `capstone/workspace-backend/fastapi`

## 이번에 실제 실행한 명령

`2026-03-10`에는 저장소 루트 가상환경의 Python을 명시해서 새 MSA 트랙을 재검증했습니다.

- `labs/H-service-boundary-lab/fastapi`
  - `make lint`
  - `make test`
  - `make smoke`
- `labs/I-event-integration-lab/fastapi`
  - `make lint`
  - `make test`
  - `make smoke`
- `labs/J-edge-gateway-lab/fastapi`
  - `make test`의 service unit test 구간
  - `python -m pytest tests/test_system.py -q`
  - `python -m tests.smoke`
- `labs/K-distributed-ops-lab/fastapi`
  - `make test`
  - `make smoke`
- `capstone/workspace-backend-v2-msa/fastapi`
  - `make test`의 service unit test 구간
  - `docker compose up --build -d` 재시도
  - `docker build --progress=plain -t workspace-v2-identity-fresh ./services/identity-service`
  - `docker pull python:3.12-slim`
  - Docker Desktop 재시작 후 prebuilt local image를 복구한 뒤 `docker compose -p workspace-backend-v2-msa-dd63448c -f compose.yaml up -d --no-build`
  - `tests/test_system.py`와 같은 흐름을 수행하는 inline Python script로 register -> verify -> login -> Google login -> invite -> comment -> drain -> notification-service stop/start -> recovery drain -> websocket notification 확인

`2026-03-09`에는 기존 일곱 개 lab과 capstone v1에서 아래 순서로 확인했습니다.

- 새 가상환경 생성
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`

## 마지막 기록된 결과 요약

### `2026-03-10` MSA 트랙

- `labs/H-service-boundary-lab/fastapi`: lint, service unit test, system test, smoke 통과
- `labs/I-event-integration-lab/fastapi`: lint, service unit test, system test, smoke 통과
- `labs/J-edge-gateway-lab/fastapi`: gateway/identity/workspace/notification unit test 통과, system test 통과, smoke 통과
- `labs/K-distributed-ops-lab/fastapi`: gateway/identity/workspace/notification unit test 통과, system test 통과, smoke 통과
- `capstone/workspace-backend-v2-msa/fastapi`: gateway/identity/workspace/notification unit test 통과. fresh build 경로는 Docker Desktop 문제로 성공 기록을 남기지 못했지만, Docker Desktop 재시작 후 손상된 local image를 복구하고 prebuilt image 기준 Compose runtime + end-to-end 협업 흐름 검증을 완료함

### `2026-03-09` 기존 트랙

- `labs/A-auth-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과
- `labs/B-federation-security-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. PostgreSQL 데이터베이스 이름을 `DATABASE_URL`과 맞춘 뒤 재검증
- `labs/C-authorization-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화
- `labs/D-data-api-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화
- `labs/E-async-jobs-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 API 스키마 자동 초기화
- `labs/F-realtime-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과
- `labs/G-ops-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과
- `capstone/workspace-backend/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화

## v2 검증에 남아 있는 단서

- `capstone/workspace-backend-v2-msa/fastapi`의 fresh image rebuild 경로는 `2026-03-10`에 안정적으로 성공했다고 기록하지 않습니다.
- 같은 날 실제로 확인한 실패/비정상 징후는 아래 두 가지였습니다.
  - Docker Desktop containerd 저장소의 `input/output error`
  - `docker pull` / `docker build`가 `load metadata for docker.io/library/python:3.12-slim...` 단계에서 멈추는 현상
- 재시작 후 남아 있던 local image를 검사했더니 `/usr/local/lib/python3.12/site-packages/uvicorn/__main__.py`, `/usr/local/lib/python3.12/site-packages/pip/__main__.py`, `/usr/local/bin/uvicorn` 같은 파일이 0바이트였다.
- 그래서 v2의 최종 runtime 검증은 “fresh build 성공”이 아니라 “손상된 local image를 `ensurepip` + `pip install -e .[dev]`로 복구한 뒤, `docker compose up -d --no-build`로 올린 Compose stack에서 end-to-end 흐름을 다시 확인했다”는 의미다.
- late patch note:
  - 같은 원인 때문에 H~K와 v2의 Compose command / Dockerfile CMD를 `uvicorn ...`에서 `python -m uvicorn ...`으로 바꿨다.
  - 이 container command patch는 v2 runtime에서 실제 재확인했다.
  - H~K는 같은 날 earlier smoke 성공 기록이 있고, 이 좁은 patch 자체는 별도로 다시 돌리지 않았다.

## 이 보고서가 증명하는 것

- 문서에 적힌 Python 워크스페이스가 설치되고 실행됐다.
- 추적 중인 테스트 스위트가 당시 기준으로 통과했다.
- 로컬 Docker Compose 스택이 부팅되고 health endpoint에 응답했다.
- v2에서는 owner/local login, collaborator/google login, invite accept, comment 저장, drain 실패 후 recovery, websocket notification 전달까지 실제로 다시 확인했다.

## 이 보고서가 증명하지 않는 것

- AWS나 기타 클라우드에 실제 배포가 성공했다는 사실
- 장시간 부하, 성능, 복구 시나리오
- 테스트가 덮지 못한 보안 검토
- worker와 websocket client의 장시간 운영 안정성

학습 저장소의 검증 목표는 "제품 수준 보증"이 아니라 "다시 실행 가능하고 설명 가능한 상태"입니다.
