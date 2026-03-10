# F-realtime-lab FastAPI

## 이 구현이 다루는 범위

- WebSocket 인증
- presence heartbeat
- fan-out delivery
- reconnect 보조 endpoint
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

- `api`: 호스트 `8004` 포트로 노출됩니다.
- `redis`: Redis 7을 `6381` 포트로 노출합니다.

## 이 워크스페이스에서 확인할 점

- `make run`은 기본 SQLite 설정으로도 바로 뜹니다.
- `.env.example`은 TTL과 CORS 같은 공유 설정을 담고 있어 로컬 실행과 Compose 실행 모두에 쓸 수 있습니다.
- Compose는 API와 Redis만 포함합니다.
- 실시간 확장 경계는 Redis까지 열어 두되, 이 랩의 핵심은 연결 모델 설명입니다.

## 함께 읽을 문서

- [상위 README](../README.md)
- [문제 정의](../problem/README.md)
- [문서 지도](../docs/README.md)
