# 개발 타임라인

## 이 문서의 목적

- 운영성 랩을 다시 열었을 때 “무슨 기능이 있나”보다 “무슨 운영 질문에 답하나”를 기준으로 재현 순서를 잡는다.
- health, readiness, metrics, Compose probe가 실제로 맞물리는지 빠르게 확인하는 절차를 남긴다.

## 1. 시작 위치를 고정한다

```bash
cd labs/G-ops-lab/fastapi
python3 -m venv .venv
source .venv/bin/activate
make install
cp .env.example .env
```

- 이 랩은 기본적으로 SQLite를 쓰고 Redis 의존성도 없다.
- `.env.example`을 복사해도 로컬 실행과 Compose 실행이 크게 갈라지지 않는다.

## 2. 가장 빠른 자동 재현 경로

```bash
pytest tests/integration/test_ops.py -q
make smoke
```

- 테스트는 `/api/v1/health/live`, `/api/v1/ops/ready`, `/api/v1/ops/metrics` 세 엔드포인트가 기대 shape를 반환하는지 확인한다.
- `make smoke`는 앱 부팅과 `/api/v1/health/live`를 다시 한 번 확인한다.

## 3. 로컬 편집 루프를 연다

```bash
make run
```

다른 터미널에서:

```bash
curl http://127.0.0.1:8000/api/v1/health/live
curl http://127.0.0.1:8000/api/v1/ops/ready
curl http://127.0.0.1:8000/api/v1/ops/metrics
```

- 세 번째 응답 본문에 `app_requests_total`이 포함되면 metrics surface가 살아 있는 것이다.
- 로컬 기본 DB는 `g_ops_lab.db`다.

## 4. Compose probe 경로를 확인한다

```bash
docker compose up --build -d
docker compose ps
curl http://127.0.0.1:8005/api/v1/health/live
curl http://127.0.0.1:8005/api/v1/ops/ready
curl http://127.0.0.1:8005/api/v1/ops/metrics
```

- Compose에서는 API가 `8005` 포트로 노출된다.
- `docker compose ps`에서 health 상태가 `healthy`로 올라오는지 확인한다.
- 정리할 때는 `docker compose down -v`를 쓴다.

## 5. 운영성 확인 순서를 고정한다

재현 순서는 항상 아래처럼 가져간다.

1. `live`로 프로세스가 살아 있는지 본다.
2. `ready`로 애플리케이션이 요청을 받을 준비가 되었는지 본다.
3. `metrics`로 관측 표면이 실제로 열려 있는지 본다.
4. Compose healthcheck가 위 세 엔드포인트 중 무엇을 기준으로 삼는지 다시 확인한다.
5. 마지막으로 [../docs/aws-deployment.md](../docs/aws-deployment.md)를 읽고, 이 랩이 실제 배포 검증이 아니라 문서 수준 target shape라는 점을 다시 확인한다.

## 6. 막히면 먼저 확인할 것

- `ready`만 실패하면 보통 애플리케이션 초기화나 의존성 확인이 readiness에만 묶여 있는지 본다.
- metrics 본문이 비어 보이면 `app_requests_total` 문자열이 있는지부터 확인한다.
- 운영성 랩은 기능 추가보다 검증 관점이 중요하므로, 새 endpoint를 더 만들기 전에 기존 probe가 어떤 질문에 답하는지 먼저 적는 편이 낫다.
