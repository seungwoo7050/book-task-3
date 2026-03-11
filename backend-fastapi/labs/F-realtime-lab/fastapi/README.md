# F-realtime-lab FastAPI

이 문서는 F-realtime-lab의 실행과 검증 진입점입니다. 문제 정의나 설계 해설보다 먼저 손을 움직여 보고 싶을 때 여기서 시작합니다.

## 이 워크스페이스가 제공하는 답

- WebSocket 인증
- presence heartbeat
- fan-out delivery
- reconnect 보조 endpoint
- `/api/v1/health/live`, `/api/v1/health/ready`

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

- `api`: 호스트 `8004` 포트로 노출됩니다.
- `redis`: Redis 7을 `6381` 포트로 노출합니다.

## 실행 전에 알아둘 점

- `make run`은 기본 SQLite 설정으로도 바로 뜹니다.
- `.env.example`은 TTL과 CORS 같은 공유 설정을 담고 있어 로컬 실행과 Compose 실행 모두에 쓸 수 있습니다.
- Compose는 API와 Redis만 포함합니다.
- 실시간 확장 경계는 Redis까지 열어 두되, 이 랩의 핵심은 연결 모델 설명입니다.

## 역할이 다른 관련 문서

- 문제 요약과 답안 인덱스: [상위 README](../README.md)
- canonical problem statement: [problem/README.md](../problem/README.md)
- 설계 설명: [docs/README.md](../docs/README.md)
- 학습 로그: [notion/README.md](../notion/README.md)
