# workspace-backend FastAPI

## 이 구현이 다루는 범위

- 로컬 로그인과 Google 스타일 로그인
- 워크스페이스 멤버십과 역할
- 프로젝트 / 태스크 / 댓글 API
- queued notification과 realtime delivery
- `/api/v1/health/live`, `/api/v1/health/ready`

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

- `api`: 호스트 `8010` 포트로 노출됩니다.
- `db`: PostgreSQL 16, 데이터베이스 이름은 `workspace_backend`입니다.
- `redis`: Redis 7을 `6390` 포트로 노출합니다.

## 이 워크스페이스에서 확인할 점

- `make run`은 기본 SQLite 설정으로도 시작할 수 있습니다.
- `.env.example`은 PostgreSQL과 Redis가 있는 Compose 기준 값입니다.
- Compose는 API, PostgreSQL, Redis를 함께 띄웁니다.
- 이 capstone은 랩 코드를 import 하지 않고, 개념을 다시 조합한 통합 워크스페이스입니다.

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
