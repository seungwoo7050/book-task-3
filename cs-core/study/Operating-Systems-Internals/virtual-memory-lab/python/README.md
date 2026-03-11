# Python 구현 안내

## 구현 범위

- trace parser
- FIFO, LRU, Clock, OPT replacement
- dirty bit와 dirty eviction count
- frame replay formatter와 policy summary

## 어디서부터 읽으면 좋은가

1. `python/src/os_virtual_memory/core.py`: trace를 따라 frame state를 업데이트하는 핵심 로직이다.
2. `python/src/os_virtual_memory/cli.py`: policy 선택과 replay 출력 인터페이스를 본다.
3. `python/tests/test_os_virtual_memory.py`: Belady anomaly, locality, dirty eviction assertion을 확인한다.

## 디렉터리 구조

```text
python/
  README.md
  src/os_virtual_memory/
    __main__.py
    cli.py
    core.py
  tests/
    test_os_virtual_memory.py
```

## 기준 명령

- 검증: `make -C ../problem test`
- demo: `make -C ../problem run-demo`
- 직접 실행: `PYTHONPATH=src python3 -m os_virtual_memory --trace ../problem/data/belady.trace --frames 3 --policy all --replay`

## 구현에서 먼저 볼 포인트

- `Frame`은 page 번호만이 아니라 `dirty`, `loaded_at`, `last_used`, `referenced`를 같이 들고 있다.
- Clock은 reference bit를 한 번에 모두 지우지 않고 hand가 지나갈 때만 내린다.
- snapshot은 frame index보다 어떤 page가 메모리에 남아 있는지가 잘 보이도록 page 번호 기준으로 정렬해서 출력한다.
