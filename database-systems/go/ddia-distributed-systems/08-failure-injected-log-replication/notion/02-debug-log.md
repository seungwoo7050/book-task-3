# 디버그 로그

### 1. dropped append 뒤 follower가 영원히 못 따라오는 경우
- 깨졌을 때 보이는 징후: `nextIndex`가 그대로인데도 retry가 다시 보내지지 않습니다.
- 확인 포인트: leader tick마다 follower별 `nextIndex` 이후 entry를 다시 보내는지 확인합니다.

### 2. duplicate append가 상태를 두 번 바꾸는 경우
- 깨졌을 때 보이는 징후: follower log length가 2가 되거나 apply count가 2로 증가합니다.
- 확인 포인트: 같은 index의 동일 entry는 watermark만 돌려주고 append하지 않는지 봅니다.

### 3. paused follower가 복귀해도 commit index만 보고 따라오지 못하는 경우
- 깨졌을 때 보이는 징후: leader commit은 올라갔는데 follower watermark는 그대로 멈춥니다.
- 확인 포인트: resume 뒤에도 leader가 lagging follower에게 missing entry를 계속 보내는지 확인합니다.
