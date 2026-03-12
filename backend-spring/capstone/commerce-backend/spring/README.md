# commerce-backend Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: catalog, cart, order surface를 연결한 baseline commerce API

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

- modular monolith baseline이며 microservice split을 목표로 하지 않는다
- payment와 완전한 이벤트 연동은 아직 없다
