# 02 Debug Log

## 실제로 다시 확인한 포인트

### 1. prepared discard 시 leaked block

crash after prepare에서 새 block을 회수하지 않으면 leaked block이 남는다. metadata만 롤백했다고 끝이 아니라 allocation 흔적도 같이 정리해야 한다.

### 2. committed replay와 old block free

committed write replay가 old block free를 빼먹으면 block bitmap이 틀어진다. 결과적으로 `cat`은 맞아도 free list는 틀린 상태가 될 수 있다.

### 3. root mapping과 inode table 일관성

root mapping에서 이름을 지웠는데 inode bitmap을 내리지 않거나, 반대로 inode만 지우고 root mapping을 남기면 곧바로 dangling reference가 생긴다.
