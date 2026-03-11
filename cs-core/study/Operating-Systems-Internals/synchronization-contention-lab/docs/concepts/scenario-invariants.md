# Scenario Invariants

## counter

- 모든 thread가 끝난 뒤 `final_count == threads * iterations`
- wait event는 많아질 수 있어도 lost update는 없어야 한다

## gate

- 동시에 critical section 안에 있는 thread 수가 permit limit를 넘지 않는다
- 총 통과 횟수는 `threads * iterations`와 같아야 한다

## buffer

- produced와 consumed가 최종적으로 같아야 한다
- buffer occupancy는 `0 <= count <= capacity`를 항상 만족해야 한다
- condvar wakeup 순서가 바뀌어도 underflow/overflow는 없어야 한다
