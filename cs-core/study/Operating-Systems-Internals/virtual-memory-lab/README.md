# Virtual Memory Lab

## 이 프로젝트가 가르치는 것

`virtual-memory-lab`는 page reference trace를 따라가며 page replacement policy와 locality가 page fault 수를 어떻게 바꾸는지 보여 주는 작은 실험이다.

## 누구를 위한 문서인가

- FIFO, LRU, Clock, OPT를 한 자리에서 비교하고 싶은 학습자
- locality와 Belady anomaly를 fixture로 다시 확인하고 싶은 사람
- page fault를 설명 가능한 replay 형태로 남기고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`python/README.md`](python/README.md)
3. [`docs/README.md`](docs/README.md)
4. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
virtual-memory-lab/
  README.md
  problem/
  python/
  docs/
  notion/
```

## 검증 방법

```bash
cd problem
make test
make run-demo
```

검증에서 보는 핵심 신호:

- FIFO에서 Belady anomaly 예제가 실제로 재현된다.
- locality trace에서 LRU/OPT가 FIFO보다 나쁘지 않다.
- dirty trace에서 dirty eviction count가 고정된 값으로 나온다.

## 스포일러 경계

- 이 프로젝트는 실제 MMU나 TLB를 구현하지 않고 page replacement 핵심만 다룬다.
- README는 trace와 결과 해석에 집중하고, 긴 개념 설명은 `docs/`와 `notion/`으로 분리한다.

## 포트폴리오로 확장하는 힌트

- frame 수를 sweep 하며 CSV를 뽑으면 시각화 과제로 확장하기 좋다.
- write-back cost를 더 현실적으로 모델링하면 buffer cache 이야기로 이어질 수 있다.

## 현재 한계

- page table, TLB, swap subsystem은 범위 밖이다.
- snapshot은 frame slot보다 resident page set을 보여 주는 쪽으로 단순화돼 있다.
