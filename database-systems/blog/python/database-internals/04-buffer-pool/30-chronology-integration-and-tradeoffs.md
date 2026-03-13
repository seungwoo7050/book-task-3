# 30 Integration And Tradeoffs

## Day 1
### Session 5

이 단계의 통합 포인트는 `parse_page_id -> file handle -> fixed-size page` 흐름이다.

```python
file_path, page_number = parse_page_id(page_id)
handle = self._get_handle(file_path)
handle.seek(page_number * self.page_size)
data = bytearray(handle.read(self.page_size))
```

`page_id`가 `"/path/to/file:page_no"` 형태로 고정되어 있어서, buffer pool은 파일 포맷을 몰라도 페이지 단위 접근이 가능하다.

tradeoff도 분명하다.

- 장점:
  - 구현 단순, 학습 관찰 지점 선명
  - file handle 재사용(`self.file_handles`)로 기본 I/O 비용 절감
- 한계:
  - pinned victim 만났을 때 대체 victim 탐색 없음
  - 비동기 flush/background writer 없음
  - latch/lock 없는 단일 스레드 가정

CLI:

```bash
cd python/database-internals/projects/04-buffer-pool
PYTHONPATH=src python3 -m pytest -q
```

테스트 구조를 보면 04의 의도가 더 분명해진다.

- `test_lru_*`: 교체 정책 자체의 정확성
- `test_fetch/dirty/eviction`: buffer manager의 상태 전이

즉 LRU와 buffer pool을 분리해 읽어야 한다. LRU는 후보 생성기이고, safety/integrity 판단은 buffer pool이 맡는다.

다음 단계 연결:

`05-mvcc`에서는 같은 key에 여러 버전이 생긴다. 04에서 배운 "메모리 프레임 수명 관리" 위에, 05는 "버전 가시성 수명 관리"를 올린다.