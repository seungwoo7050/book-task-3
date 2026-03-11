# 02 Debug Log

## 실제로 다시 확인한 포인트

### 1. RR enqueue 순서

RR에서 quantum이 끝날 때 새 arrival을 먼저 enqueue하지 않으면 ready queue 순서가 뒤틀린다. 테스트는 통과해도 replay가 사람이 기대한 순서와 다르게 보일 수 있다.

### 2. MLFQ boost 시점

boost를 tick 도중에 넣을지, dispatch 경계에서만 넣을지 애매하면 golden timeline이 흔들린다. 이 프로젝트에서는 dispatch boundary로 고정했다.

### 3. metric 계산 중복

timeline을 다시 훑어 response time을 계산하려 하면 idle tick과 첫 실행 시점을 따로 처리해야 한다. process state에 `start`와 `completion`을 남기는 쪽이 더 단순했다.
