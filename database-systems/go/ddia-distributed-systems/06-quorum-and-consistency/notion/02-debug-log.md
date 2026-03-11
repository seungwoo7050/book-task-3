# 디버그 로그

### 1. version이 quorum 실패에서도 올라가는 경우
- 깨졌을 때 보이는 징후: 테스트는 실패했는데 다음 write가 `v2`부터 시작합니다.
- 확인 포인트: write quorum 확보 전에는 cluster-level version map을 건드리면 안 됩니다.

### 2. stale read가 재현되지 않는 경우
- 깨졌을 때 보이는 징후: `W=1, R=1` 시나리오에서도 항상 최신값이 읽힙니다.
- 확인 포인트: read quorum responder가 실행마다 달라지지 않는지, 그리고 stale replica가 실제로 최신 write를 놓쳤는지 봅니다.

### 3. read merge가 responder 순서에 휘둘리는 경우
- 깨졌을 때 보이는 징후: 늦게 온 responder가 최신인데도 오래된 값이 선택됩니다.
- 확인 포인트: responder 순서가 아니라 version 비교로 최신값을 고르는지 확인합니다.
