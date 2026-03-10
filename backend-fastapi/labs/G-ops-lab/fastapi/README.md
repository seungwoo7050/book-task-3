# G-ops-lab FastAPI

## 이 구현이 다루는 범위

- liveness / readiness health endpoint
- 최소 metrics surface
- 구조화 로그
- container-friendly startup

## 빠른 시작

가장 빠른 로컬 확인:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make run
```

Compose 전체 확인:

```bash
cp .env.example .env
docker compose up --build
```

## 검증 명령

```bash
make lint
make test
make smoke
docker compose up --build
```

## Compose 구성

- `api`: 호스트 `8005` 포트로 노출됩니다.

## 이 워크스페이스에서 확인할 점

- `make run`은 기본 SQLite 설정으로 바로 뜹니다.
- `.env.example`은 로컬과 Compose에서 같은 health/metrics shape를 맞추기 위한 값입니다.
- Compose는 가장 작은 형태의 API 부팅 검증만 담당합니다.
- 운영성 랩의 배포 가정은 [docs/aws-deployment.md](../docs/aws-deployment.md)에서 문서로 설명합니다.

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
