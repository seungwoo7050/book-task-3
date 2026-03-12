# C-authorization-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: invite, membership, RBAC 결정, ownership check

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

- authorization rule은 service logic 중심이며 method security는 아직 없다
- membership state는 인메모리로 유지한다
