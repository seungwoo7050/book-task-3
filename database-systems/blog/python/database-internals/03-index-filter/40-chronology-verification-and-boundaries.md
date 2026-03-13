# 40 Verification And Boundaries

## Day 1
### Session 6

최종 검증은 두 신호를 같이 본다.

CLI:

```bash
cd python/database-internals/projects/03-index-filter
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m index_filter
```

검증 포인트:

- 테스트: `4 passed`
- demo: `{'found': True, 'value': 'value-k023', 'bytes_read': ...}`

demo 출력에 `bytes_read`가 포함된다는 점이 중요하다. "찾았다"만으로는 03의 목적을 증명하지 못한다. read amplification이 줄었는지까지 같이 봐야 한다.

또 하나의 핵심은 footer 복원.

```python
footer = FOOTER_MAGIC + struct.pack(
    ">QQQQI",
    self.bloom_offset,
    self.bloom_size,
    self.index_offset,
    self.index_size,
    self.block_size,
)
```

`SSTable.load()`가 이 footer를 읽어 Bloom/index 위치를 복원한다. 즉 보조 구조는 메모리 캐시가 아니라 파일 포맷의 일부로 저장된다.

이 단계의 boundary:

- 다루는 것:
  - point lookup cost reduction (reject + bounded scan)
  - footer 기반 metadata 복원
- 다루지 않는 것:
  - range scan acceleration
  - block cache / read-ahead
  - compaction-level index/filter 관리

다음 질문:

- buffer pool을 붙이면 bounded scan 블록은 얼마나 재사용될까
- MVCC와 결합할 때 visibility 판정은 어느 계층에서 처리할까