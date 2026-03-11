# C 구현 안내

## 구현 범위

- mutex-protected counter
- named POSIX semaphore gate
- mutex + condvar bounded buffer
- 공통 metrics 출력 CLI

## 어디서부터 읽으면 좋은가

1. `c/include/contention_lab.h`: 세 시나리오가 공유하는 metric shape를 먼저 본다.
2. `c/src/contention_lab.c`: counter, gate, buffer 각각의 synchronization 규칙을 읽는다.
3. `c/src/main.c`: CLI 파라미터와 exit code 계약을 확인한다.
4. `c/tests/test_cases.sh`: shell invariant test가 무엇을 고정하는지 본다.

## 디렉터리 구조

```text
c/
  README.md
  Makefile
  include/
    contention_lab.h
  src/
    contention_lab.c
    main.c
  tests/
    test_cases.sh
  bin/
```

## 기준 명령

- 검증: `make -C . test`
- demo: `make -C . bench`
- 직접 실행: `./bin/contention_lab --scenario counter --threads 8 --iterations 10000`

## 구현에서 먼저 볼 포인트

- correctness 판단은 `ok=1`과 invariant field에서 끝낸다. elapsed time은 참고값이다.
- semaphore 시나리오는 macOS 호환성을 위해 named POSIX semaphore를 사용한다.
- bounded buffer는 `while` 루프와 condvar를 같이 써 spurious wakeup을 견딘다.
