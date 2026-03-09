# 디버그 기록 — 캐시와 동시성에서 만나는 함정들

## 캐시에서 읽은 값이 DB와 다름

`UpdateItem`에서 `delete(s.cache, item.ID)`를 빼먹으면, 이후 `GetItem`이 오래된 캐시 값을 반환한다. 테스트 `TestInvalidationOnUpdate`가 이 상황을 잡는다: update 후 다시 get하면 `cacheMisses`가 2여야 한다(첫 읽기 + invalidation 후 재읽기).

**교훈**: 캐시 invalidation은 update 성공 "후"에 해야 한다. update 전에 삭제하면, update가 실패했을 때 불필요하게 캐시 miss가 발생한다.

## Mutex로 캐시 보호 시 데드락

초기 구현에서 `GetItem` 전체를 Mutex로 감쌌다. DB 조회까지 포함. 그러면 동시 요청이 모두 대기하게 되어, 캐시 없이 직접 DB를 조회하는 것보다 느려질 수 있다.

해결: 캐시 맵 접근만 Lock/Unlock하고, DB 조회는 락 밖에서 수행한다.

```go
s.mu.Lock()
if item, ok := s.cache[id]; ok {
    s.mu.Unlock()
    return item, nil
}
s.mu.Unlock()
// DB 조회 (락 없이)
```

## atomic.Int64 vs Mutex로 카운터

카운터에 Mutex를 쓰면:
```go
s.mu.Lock()
s.cacheHits++
s.mu.Unlock()
```

atomic을 쓰면:
```go
s.metrics.cacheHits.Add(1)
```

atomic이 훨씬 간결하고 빠르다. Mutex는 내부적으로 OS 스케줄러와 상호작용하지만, atomic은 CPU 명령어 한 개로 처리된다.

## rand.Seed 경고

Go 1.20부터 `rand.Seed`는 deprecated다. `math/rand/v2`를 쓰거나, 세계적으로 자동 시드되기 때문이다. 이 프로젝트에서는 `init()`에서 `rand.Seed(time.Now().UnixNano())`를 호출하는데, Go 1.24에서는 경고가 나올 수 있다. trace ID 생성에 `crypto/rand`를 쓰면 더 안전하다.

## X-Trace-ID가 응답에 없음

`withTrace`에서 `w.Header().Set("X-Trace-ID", traceID)` 호출은 `WriteHeader` 전에 해야 한다. `WriteHeader`가 먼저 호출되면 이후 `Set`은 무시된다. 이 프로젝트에서는 `withTrace`가 핸들러 전에 실행되고, `writeJSON`이 `WriteHeader`를 호출하므로 순서가 맞다.

## /metrics 경로가 v1 프리픽스 없음

`/metrics`는 `/v1/metrics`가 아니라 루트에 두었다. 메트릭은 API 버저닝과 무관한 인프라 엔드포인트이기 때문이다. Prometheus가 스크래핑할 때 `/metrics` 경로를 기본으로 기대한다.
