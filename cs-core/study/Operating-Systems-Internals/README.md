# Operating-Systems-Internals

## 이 트랙이 가르치는 것

이 트랙은 `Systems-Programming`에서 손으로 구현한 감각을 운영체제 breadth로 확장하는 구간이다. scheduling, virtual memory, filesystem, synchronization을 각각 작은 실험으로 나눠 읽는다.

## 누구를 위한 문서인가

- 운영체제 이론을 toy lab으로 다시 확인하고 싶은 학습자
- `Systems-Programming` 뒤에 이어질 개념 브리지가 필요한 사람
- Python과 C를 섞어도 읽기 쉬운 학습 저장소 구조를 보고 싶은 사람

## 먼저 읽을 곳

1. [`scheduling-simulator/README.md`](scheduling-simulator/README.md)
2. [`virtual-memory-lab/README.md`](virtual-memory-lab/README.md)
3. [`filesystem-mini-lab/README.md`](filesystem-mini-lab/README.md)
4. [`synchronization-contention-lab/README.md`](synchronization-contention-lab/README.md)
5. [`../../../guides/cs/operating-systems.md`](../../../guides/cs/operating-systems.md)

## 디렉터리 구조

```text
Operating-Systems-Internals/
  README.md
  scheduling-simulator/
  virtual-memory-lab/
  filesystem-mini-lab/
  synchronization-contention-lab/
```

## 필수 코어와 심화

| 순서 | 구분 | 프로젝트 | 이 단계에서 보는 질문 | 다음 단계 |
| --- | --- | --- | --- | --- |
| 1 | `필수 코어` | [`scheduling-simulator`](scheduling-simulator/README.md) | policy가 fairness와 latency를 어떻게 바꾸는가 | Virtual Memory |
| 2 | `필수 코어` | [`virtual-memory-lab`](virtual-memory-lab/README.md) | locality와 replacement가 fault 수를 어떻게 바꾸는가 | Filesystem |
| 3 | `심화/선택` | [`filesystem-mini-lab`](filesystem-mini-lab/README.md) | inode/block allocation과 journaling recovery를 어떻게 최소 모델로 설명할까 | Synchronization |
| 4 | `심화/선택` | [`synchronization-contention-lab`](synchronization-contention-lab/README.md) | mutex/semaphore/condvar는 어떤 contention invariant를 가져오는가 | deferred `xv6-bridge` |

## 검증 방법

- 각 프로젝트는 `problem/` 아래 canonical `make test`와 `make run-demo`를 가진다.
- Python 기반 프로젝트는 `python/` 구현과 `pytest`를 사용한다.
- synchronization 프로젝트는 `c/` binary와 shell test를 사용한다.

## 보완 관계

- `Systems-Programming`이 “직접 만들어 보는 시스템 프로그래밍” 축이라면, 이 트랙은 “운영체제 개념을 실험으로 재정리하는 breadth” 축이다.
- 이번 라운드의 끝은 `xv6-bridge`가 아니라 4개 verified lab까지다. `xv6-bridge`는 후속 브리지 프로젝트로 남겨 둔다.

## 포트폴리오로 확장하는 힌트

- 네 프로젝트를 같은 표 스타일과 demo shape로 맞추면 “개념별 실험 레포”라는 메시지가 선명해진다.
- 이후 `xv6-bridge`를 붙이면 toy model과 실제 커널 소스 독해를 연결하는 좋은 후속편이 된다.
