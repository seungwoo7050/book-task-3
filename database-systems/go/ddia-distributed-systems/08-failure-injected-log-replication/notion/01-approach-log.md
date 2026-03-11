# 접근 로그

## 1. 메시지 종류를 `append`와 `ack` 두 개로 고정했습니다
하네스가 흔드는 대상이 분명해야 failure injection이 읽기 쉬워집니다. 그래서 replication path를 최소 메시지 집합으로 줄였습니다.

## 2. pause는 queue가 아니라 blackhole로 뒀습니다
이번 단계의 핵심은 “복귀 후 retry로 따라잡는가”이지 지연 큐 재전송이 아닙니다. 그래서 pause 중 메시지는 버리고, resume 뒤 leader가 다시 보내는 방식으로 단순화했습니다.

## 3. duplicate handling은 follower에서 막습니다
같은 index의 동일 entry가 다시 와도 log와 state mutation을 늘리지 않도록 follower가 idempotent하게 처리하게 했습니다.
