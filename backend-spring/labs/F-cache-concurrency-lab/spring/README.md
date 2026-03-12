# F-cache-concurrency-lab Spring 워크스페이스

- 상태: `verified scaffold`
- 현재 범위: cache/idempotency 패턴과 reservation flow 모델링

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

- 테스트는 in-memory `CacheManager`를 사용한다
- distributed lock은 다음 단계이며 현재는 `synchronized` 기반이다
