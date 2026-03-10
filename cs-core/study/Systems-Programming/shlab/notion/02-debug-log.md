# 02. 디버그 기록

## 실제로 다시 확인한 포인트

### 1. `fork` 직후 `SIGCHLD` race

가장 먼저 잡아야 했던 문제다.
`addjob` 전에 `SIGCHLD`가 도착하면 job table이 바로 어긋난다.

### 2. process group 전환 누락

child가 자기 process group을 만들지 않으면,
Ctrl-C와 Ctrl-Z가 셸 자신에게까지 잘못 전달될 수 있다.

### 3. `fg`와 `bg` 상태 갱신

stopped job을 다시 `Running`으로 바꾸는 타이밍이 조금만 어긋나도
`jobs` 출력과 실제 상태가 달라진다.

### 4. direct harness의 가치

단순 compile이나 단발 실행만으로는 signal 관련 버그를 잡기 어렵다.
FIFO 기반 self-owned harness가 실제로 많이 도움이 됐다.
