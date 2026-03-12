# F-cache-concurrency-lab

캐시, 멱등성, 재고 경합을 한 시나리오에서 같이 설명하는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- 실제 서비스에서는 캐시, 중복 요청, 동시성 문제가 따로 오지 않고 한 흐름 안에서 겹칩니다.
- 학습 단계에서는 Redis와 분산 락을 바로 과시하기보다, 어떤 문제가 먼저 보이는지 설명할 수 있어야 합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- inventory 조회와 reservation endpoint를 중심으로 cacheable read path와 idempotency key 처리를 구현했습니다.
- `synchronized` 기반 in-process 제어로 재고 차감 경합을 먼저 드러냈습니다.
- 분산 락과 Redis-backed cache로 확장되기 전 단계의 baseline을 남겼습니다.

## 핵심 설계 선택

- 캐시와 동시성을 분리하지 않고 하나의 inventory 시나리오에 묶었습니다.
- in-memory `CacheManager`와 in-process lock으로 문제의 shape를 먼저 고정했습니다.
- Redisson과 Redis는 "다음 단계"로 남겨 키워드 인플레이션을 피했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- Redis-backed cache assertion
- distributed lock implementation
- idempotency persistence 분리 심화

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
