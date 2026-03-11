# 02 Debug Log

## 실제로 다시 확인한 포인트

### 1. condvar와 `while` discipline

condvar는 `if` 한 번으로 감싸면 spurious wakeup이나 경쟁적 wakeup에서 쉽게 깨진다. bounded buffer는 반드시 `while` loop로 조건을 다시 확인해야 했다.

### 2. semaphore 테스트 기준

semaphore 시나리오는 elapsed time보다 max concurrency invariant를 보는 편이 훨씬 안정적이다. 시간만 보면 머신 상태에 따라 쉽게 흔들린다.

### 3. counter wait signal

mutex 경합을 눈으로 보이기 위해 `pthread_mutex_trylock` 실패를 wait event로 세었다. correctness와는 별개지만 contention이 있었는지 설명하기 좋은 보조 신호였다.
