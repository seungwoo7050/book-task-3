# Virtual Memory Lab

`virtual-memory-lab`는 page reference trace를 따라가며 replacement policy와 locality가 page fault 수를 어떻게 바꾸는지 보여 주는 실험이다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| FIFO, LRU, Clock, OPT를 같은 trace에서 비교해 page fault와 dirty eviction 차이를 설명한다. | trace-driven 모델만 다루고, page table이나 TLB는 범위 밖으로 둔다. | 구현은 [`python/`](python/README.md)의 replacement simulator, trace fixture, replay CLI로 정리한다. | [`problem/README.md`](problem/README.md), [`python/README.md`](python/README.md) | locality, Belady anomaly, replacement policy, dirty page 해석 | `public verified` |

## 디렉터리 역할

- `problem/`: 문제 범위와 canonical `make` entrypoint
- `python/`: simulator 구현과 CLI
- `docs/`: replacement policy, locality, dirty page 개념 정리
- `notion/`: fixture 설계와 재검증 기록

## 검증 빠른 시작

```bash
cd problem
make test
make run-demo
```

검증에서 보는 핵심 신호:

- FIFO에서 Belady anomaly 예제가 실제로 재현된다.
- locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다.
- dirty trace에서 dirty eviction count가 고정된 값으로 나온다.

## 공개 경계

- 이 프로젝트는 실제 MMU나 TLB를 구현하지 않고 page replacement 핵심만 다룬다.
- README는 trace와 결과 해석에 집중하고, 긴 개념 설명은 `docs/`와 `notion/`으로 분리한다.

## 현재 한계

- page table, TLB, swap subsystem은 범위 밖이다.
- snapshot은 frame slot보다 resident page set을 보여 주는 쪽으로 단순화돼 있다.
