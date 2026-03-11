# 04 Knowledge Index

## 핵심 용어

- locality: 최근/근처 접근이 반복되는 패턴
- page fault: 필요한 page가 frame에 없어서 replacement가 필요한 상태
- Belady anomaly: frame이 늘었는데도 FIFO fault가 늘어나는 현상
- dirty eviction: 수정된 page를 교체하면서 write-back 비용이 생기는 상황

## 같이 보면 좋은 파일

- `../docs/concepts/locality-and-faults.md`
- `../docs/concepts/replacement-policies.md`
- `../docs/concepts/dirty-pages-and-writeback.md`
- `../python/tests/test_os_virtual_memory.py`
