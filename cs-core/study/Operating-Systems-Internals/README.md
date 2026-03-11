# Operating-Systems-Internals

`Operating-Systems-Internals`는 `Systems-Programming`에서 손으로 구현한 감각을 scheduler, VM, filesystem, synchronization 실험으로 확장하는 breadth 트랙이다.

## 프로젝트 지도

| 프로젝트 | 문제 | 이 레포의 답 | 검증 시작점 | 상태 |
| --- | --- | --- | --- | --- |
| [`scheduling-simulator`](scheduling-simulator/README.md) | scheduling policy가 waiting/response/turnaround를 어떻게 바꾸는지 비교 | `python/` 구현, fixture, replay CLI | [`problem`](scheduling-simulator/problem/README.md), [`python`](scheduling-simulator/python/README.md) | `public verified` |
| [`virtual-memory-lab`](virtual-memory-lab/README.md) | replacement policy와 locality가 fault 수를 어떻게 바꾸는지 비교 | `python/` 구현, trace fixture, replay CLI | [`problem`](virtual-memory-lab/problem/README.md), [`python`](virtual-memory-lab/python/README.md) | `public verified` |
| [`filesystem-mini-lab`](filesystem-mini-lab/README.md) | inode/block allocation과 journaling recovery를 toy filesystem으로 설명 | `python/` 구현, JSON disk image, demo fixture | [`problem`](filesystem-mini-lab/problem/README.md), [`python`](filesystem-mini-lab/python/README.md) | `public verified` |
| [`synchronization-contention-lab`](synchronization-contention-lab/README.md) | mutex, semaphore, condvar가 contention invariant를 어떻게 드러내는지 실험 | `c/` 구현, scenario test, demo binary | [`problem`](synchronization-contention-lab/problem/README.md), [`c`](synchronization-contention-lab/c/README.md) | `public verified` |

## 권장 순서

1. [`scheduling-simulator`](scheduling-simulator/README.md)
2. [`virtual-memory-lab`](virtual-memory-lab/README.md)
3. [`filesystem-mini-lab`](filesystem-mini-lab/README.md)
4. [`synchronization-contention-lab`](synchronization-contention-lab/README.md)

- `필수 코어`: `scheduling-simulator -> virtual-memory-lab`
- `심화/선택`: `filesystem-mini-lab -> synchronization-contention-lab`

## 검증 원칙

- 네 프로젝트 모두 `problem/` 아래 canonical `make test`, `make run-demo` 경로를 유지한다.
- Python 기반 프로젝트는 `python/README.md`가 구현 entrypoint이고, synchronization 프로젝트는 `c/README.md`가 구현 entrypoint다.
- replay output과 fixture 비교가 핵심이라, README는 성공 신호를 짧게 명시하고 긴 해설은 `docs/`, `notion/`으로 내린다.

## 공개 경계

- 이 트랙은 self-authored fixture와 구현만 사용하므로 공개 범위가 넓다.
- README는 실험 범위와 검증 경로를 먼저 보여 주고, 이론 배경과 확장 아이디어는 하위 문서로 보낸다.
- 실제 커널 소스 독해나 `xv6-bridge` 같은 후속 브리지는 현재 범위 밖으로 남겨 둔다.
