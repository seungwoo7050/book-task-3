# Virtual Memory Lab 문서

## 이 디렉터리가 가르치는 것

이 디렉터리는 virtual memory 전체 구현을 다루기보다, trace와 frame 수를 바꿨을 때 왜 page fault 수가 달라지는지 설명한다. 특히 locality, replacement policy, dirty eviction을 같은 자리에서 읽을 수 있게 하는 것이 목표다.

## 누구를 위한 문서인가

- FIFO와 LRU를 이름만 아는 상태에서 벗어나고 싶은 학습자
- Belady anomaly가 실제 trace에서 어떻게 드러나는지 보고 싶은 사람
- OPT를 “현실 정책”이 아니라 비교 기준선으로 이해하고 싶은 사람

## 먼저 읽을 곳

1. [`concepts/locality-and-faults.md`](concepts/locality-and-faults.md)
2. [`concepts/replacement-policies.md`](concepts/replacement-policies.md)
3. [`concepts/dirty-pages-and-writeback.md`](concepts/dirty-pages-and-writeback.md)
4. [`references/verification.md`](references/verification.md)
5. [`references/README.md`](references/README.md)

## 디렉터리 구조

```text
docs/
  README.md
  concepts/
    locality-and-faults.md
    replacement-policies.md
    dirty-pages-and-writeback.md
  references/
    verification.md
    README.md
```

## 검증과 연결되는 파일

- trace fixture는 [`../problem/data/`](../problem/data/)에 있다.
- policy 구현과 replay formatter는 [`../python/src/os_virtual_memory/core.py`](../python/src/os_virtual_memory/core.py)에 있다.
- anomaly/locality/dirty assertion은 [`../python/tests/test_os_virtual_memory.py`](../python/tests/test_os_virtual_memory.py)에 있다.
- 현재 검증 기준은 [`references/verification.md`](references/verification.md)에 정리했다.

## 포트폴리오로 확장하는 힌트

- frame 수를 바꿔 faults를 표로 쌓으면 locality 실험 보고서처럼 읽기 좋다.
- dirty page write-back cost를 별도 metric으로 추가하면 filesystem이나 buffer cache 이야기로 자연스럽게 이어진다.
