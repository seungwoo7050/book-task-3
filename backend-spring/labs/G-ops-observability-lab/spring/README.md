# G-ops-observability-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: health, metrics, logs, CI, deployment-facing scaffolding

## 실행과 검증 명령

```bash
cp .env.example .env
make run
make lint
make test
make smoke
docker compose up --build
```

## 현재 한계

- alert rule과 dashboard는 아직 없다
- AWS 배포는 문서화된 방향이지 live infra는 아니다
