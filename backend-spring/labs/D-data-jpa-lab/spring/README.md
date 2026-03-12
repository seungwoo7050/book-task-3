# D-data-jpa-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: JPA CRUD, pagination, optimistic locking, search-ready structure

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

- Querydsl은 구조만 준비했고 깊은 검색 조합은 아직 다루지 않는다
- larger catalog graph보다 핵심 aggregate 하나에 집중한다
