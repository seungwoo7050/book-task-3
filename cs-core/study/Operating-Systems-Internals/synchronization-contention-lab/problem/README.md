# Problem Guide

## 문제 핵심

- `counter` 시나리오는 mutex로 shared counter를 보호한다.
- `gate` 시나리오는 POSIX semaphore로 동시 진입 수를 제한한다.
- `buffer` 시나리오는 mutex + condition variable로 bounded buffer를 보호한다.
- 출력은 timing보다 correctness invariant를 우선 보고, elapsed time과 wait count는 보조 지표로만 기록한다.

## 이번 범위에서 일부러 뺀 것

- lock-free queue
- rwlock
- spin lock
- priority inversion mitigation

## canonical 검증

```bash
make test
make run-demo
```

## 성공 기준

- counter final count가 expected count와 일치한다.
- semaphore gate의 max concurrency가 permit limit를 넘지 않는다.
- bounded buffer에서 underflow/overflow 없이 생산량과 소비량이 일치한다.
