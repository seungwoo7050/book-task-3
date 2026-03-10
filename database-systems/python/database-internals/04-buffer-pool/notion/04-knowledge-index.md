# 지식 인덱스

## 핵심 용어
- `buffer pool`: 디스크 page를 메모리 frame에 올려 재사용하는 계층입니다.
- `page frame`: 메모리에 올라온 page 한 장의 자리입니다.
- `pin count`: 현재 사용 중이어서 eviction하면 안 되는 정도를 나타내는 카운터입니다.
- `dirty page`: 디스크와 달라져 writeback이 필요한 page입니다.
- `LRU`: 가장 오래 쓰지 않은 항목을 먼저 내보내는 eviction 정책입니다.

## 다시 볼 파일
- `../src/buffer_pool/core.py`: `BufferPool`과 `Page`의 책임, pin/dirty bookkeeping을 확인할 수 있습니다.
- `../src/buffer_pool/core.py`: eviction 순서만 담당하는 LRU 구현을 읽을 수 있습니다.
- `../tests/test_buffer_pool.py`: disk fetch, cache hit, dirty tracking, unpin after eviction을 검증합니다.
- `../tests/test_buffer_pool.py`: LRU 기본 연산과 promotion, delete가 깨지지 않는지 봅니다.

## 개념 문서
- `../docs/concepts/lru-eviction.md`: recently used ordering과 eviction 조건을 정리합니다.
- `../docs/concepts/pin-and-dirty.md`: pin count와 dirty flag가 eviction, writeback과 어떻게 연결되는지 설명합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/test_buffer_pool.py`
- 다시 돌릴 테스트 이름: `test_lru_basic_operations`, `test_lru_eviction_and_promotion`, `test_lru_ordering_and_delete`, `test_fetch_page_from_disk`, `test_return_cached_page`, `test_track_dirty_pages`, `test_eviction_after_unpin`
- 데모 경로: `../src/buffer_pool/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 page 1을 읽어 앞부분 문자열을 출력합니다. Python 데모도 page id, pin count, prefix를 dict로 출력해 disk fetch와 cache state를 함께 보여 줍니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
