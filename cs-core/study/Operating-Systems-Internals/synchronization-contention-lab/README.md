# Synchronization Contention Lab

## 이 프로젝트가 가르치는 것

`synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다.

## 누구를 위한 문서인가

- race와 contention을 분리해서 설명하고 싶은 학습자
- `pthread_mutex_t`, POSIX semaphore, `pthread_cond_t` 사용 규칙을 비교해 보고 싶은 사람
- 절대 성능보다 invariant 검증이 왜 먼저인지 작은 실험으로 확인하고 싶은 사람

## 먼저 읽을 곳

1. [`problem/README.md`](problem/README.md)
2. [`c/README.md`](c/README.md)
3. [`docs/README.md`](docs/README.md)
4. [`notion/README.md`](notion/README.md)

## 디렉터리 구조

```text
synchronization-contention-lab/
  README.md
  problem/
  c/
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

- counter final count가 expected count와 같다.
- gate max concurrency가 permit limit를 넘지 않는다.
- buffer produced/consumed가 같고 underflow/overflow가 없다.

## 스포일러 경계

- 이 프로젝트는 lock-free primitive나 kernel scheduler internals는 다루지 않는다.
- README는 scenario와 검증 경로에 집중하고, 긴 설명은 `docs/`와 `notion/`으로 분리한다.

## 포트폴리오로 확장하는 힌트

- unsafe baseline을 추가해 race가 실제로 깨지는 모습을 비교하면 전달력이 커진다.
- perf, flamegraph, thread sanitizer 같은 도구를 붙이면 더 현실적인 debugging lab이 된다.

## 현재 한계

- lock-free primitive나 rwlock 비교는 아직 넣지 않았다.
- elapsed time은 머신 상태의 영향을 크게 받아 절대 비교 지표로 쓰지 않는다.
