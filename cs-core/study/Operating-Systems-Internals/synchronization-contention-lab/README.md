# Synchronization Contention Lab

`synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다.

## 한눈에 보기

| 문제 | 중요 제약 | 이 레포의 답 | 검증 시작점 | 배우는 개념 | 상태 |
| --- | --- | --- | --- | --- | --- |
| counter, gate, bounded buffer 시나리오에서 synchronization primitive별 invariant를 검증한다. | correctness를 timing보다 먼저 검증하고, lock-free primitive나 kernel scheduler internals는 범위 밖으로 둔다. | 구현은 [`c/`](c/README.md)의 primitive별 시나리오 코드와 `problem/`의 shell test, demo binary로 정리한다. | [`problem/README.md`](problem/README.md), [`c/README.md`](c/README.md) | mutex, semaphore, condvar, contention invariant, scenario 기반 테스트 | `public verified` |

## 디렉터리 역할

- `problem/`: 문제 범위와 canonical `make` entrypoint
- `c/`: synchronization 시나리오 구현과 binary
- `docs/`: correctness-before-timing, primitive 비교, scenario invariant 정리
- `notion/`: 디버그 로그와 재검증 기록

## 검증 빠른 시작

```bash
cd problem
make test
make run-demo
```

검증에서 보는 핵심 신호:

- counter final count가 expected count와 같다.
- gate max concurrency가 permit limit를 넘지 않는다.
- buffer produced/consumed가 같고 underflow/overflow가 없다.

## 공개 경계

- 이 프로젝트는 lock-free primitive나 kernel scheduler internals는 다루지 않는다.
- README는 scenario와 검증 경로에 집중하고, 긴 설명은 `docs/`와 `notion/`으로 분리한다.

## 현재 한계

- lock-free primitive나 rwlock 비교는 아직 넣지 않았다.
- elapsed time은 머신 상태의 영향을 크게 받아 절대 비교 지표로 쓰지 않는다.
