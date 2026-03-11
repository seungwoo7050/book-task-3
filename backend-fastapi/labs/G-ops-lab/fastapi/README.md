# G-ops-lab FastAPI

이 문서는 G-ops-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- liveness / readiness health endpoint
- 최소 metrics surface
- 구조화 로그
- container-friendly startup

## 빠른 실행

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

## 런타임 구성

- `api`: 호스트 `8005` 포트로 노출됩니다.

## 실행 전에 알아둘 점

- `make run`은 기본 SQLite 설정으로 바로 뜹니다.
- `.env.example`은 로컬과 Compose에서 같은 health/metrics shape를 맞추기 위한 값입니다.
- Compose는 가장 작은 형태의 API 부팅 검증만 담당합니다.
- 운영성 랩의 배포 가정은 [docs/aws-deployment.md](../docs/aws-deployment.md)에서 문서로 설명합니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
