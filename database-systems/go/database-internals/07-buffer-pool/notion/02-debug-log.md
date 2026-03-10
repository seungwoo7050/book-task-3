# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. cache hit인데 새 Page 객체를 만드는 경우
- 의심 파일: `../internal/bufferpool/buffer_pool.go`
- 깨지는 징후: 같은 page를 다시 읽을 때 pin count나 dirty 상태가 이어지지 않으면 buffer pool 의미가 사라집니다.
- 확인 테스트: `TestReturnCachedPage`
- 다시 볼 질문: page table이 page id를 기존 frame 객체에 정확히 매핑하는가?

### 2. pin이 남아 있는데 eviction하는 경우
- 의심 파일: `../internal/bufferpool/buffer_pool.go`
- 깨지는 징후: 사용 중인 page를 밀어내면 읽기 결과는 맞아도 writeback 시점이나 이후 참조가 깨집니다.
- 확인 테스트: `TestEvictionAfterUnpin`
- 다시 볼 질문: evict 후보를 고를 때 pin count 0인 frame만 보도록 막아 두었는가?

### 3. LRU promotion/delete 순서가 엉키는 경우
- 의심 파일: `../internal/lrucache/lru_cache.go`
- 깨지는 징후: buffer pool이 멀쩡해 보여도 내부 LRU가 잘못되면 결국 잘못된 page가 축출됩니다.
- 확인 테스트: `TestLRUBasicOperations`, `TestLRUEvictionAndPromotion`, `TestLRUOrderingAndDelete`
- 다시 볼 질문: hit, set, delete, eviction마다 doubly linked order가 기대와 일치하는가?
