# 문제 프레이밍

## 왜 이 프로젝트를 하는가
디스크 page를 메모리 frame으로 올려 재사용하는 buffer pool과, 그 위에서 eviction 순서를 정하는 LRU를 분리해 배우는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Go
- 이전 단계: 06 Index Filter
- 다음 단계: 08 MVCC
- 지금 답하려는 질문: 같은 page를 여러 번 읽을 때 어떤 객체를 다시 써야 하고, 어떤 조건에서만 eviction을 허용해야 안전한가?

## 이번 구현에서 성공으로 보는 것
- 디스크에서 page를 읽어 buffer pool에 올릴 수 있어야 합니다.
- 같은 page 재요청 시 캐시된 frame을 재사용해야 합니다.
- dirty page와 pin count를 추적해야 합니다.
- pin이 풀린 page만 eviction 대상이 되어야 합니다.
- LRU 자료구조가 promotion, delete, eviction을 일관되게 수행해야 합니다.

## 먼저 열어 둘 파일
- `../internal/bufferpool/buffer_pool.go`: `BufferPool`과 `Page`의 책임, pin/dirty bookkeeping을 확인할 수 있습니다.
- `../internal/lrucache/lru_cache.go`: eviction 순서만 담당하는 LRU 구현을 읽을 수 있습니다.
- `../tests/buffer_pool_test.go`: disk fetch, cache hit, dirty tracking, unpin after eviction을 검증합니다.
- `../tests/lru_cache_test.go`: LRU 기본 연산과 promotion, delete가 깨지지 않는지 봅니다.

## 의도적으로 남겨 둔 범위 밖 항목
- concurrent page table, async flush, recovery manager 연동은 다루지 않습니다.
- clock, ARC 같은 대체 정책 비교도 아직 포함하지 않습니다.

## 데모에서 바로 확인할 장면
- sample file에서 page 1을 읽어 prefix를 출력합니다.
