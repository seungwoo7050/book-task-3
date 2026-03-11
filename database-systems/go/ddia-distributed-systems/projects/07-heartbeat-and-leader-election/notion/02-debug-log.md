# 디버그 로그

### 1. follower가 healthy leader 아래에서도 계속 suspect 상태인 경우
- 깨졌을 때 보이는 징후: 리더는 있는데 `Suspected=true`가 계속 남습니다.
- 확인 포인트: heartbeat 수신 시 silence age와 suspicion flag를 함께 초기화하는지 봅니다.

### 2. isolated node가 leader가 되는 경우
- 깨졌을 때 보이는 징후: 다른 두 node가 down인데도 lone node가 leader로 승격됩니다.
- 확인 포인트: self vote만으로 majority를 만족시키는 계산 실수가 없는지 확인합니다.

### 3. old leader가 복귀 후에도 leader로 남는 경우
- 깨졌을 때 보이는 징후: recovered node와 current leader가 동시에 `leader` 상태입니다.
- 확인 포인트: higher term heartbeat를 받았을 때 follower로 강제 전환되는지 확인합니다.
