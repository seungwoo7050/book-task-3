# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. offset가 비거나 역전되는 경우
- 의심 파일: `../src/leader_follower/core.py`
- 깨지는 징후: 연속 offset이 깨지면 watermark 기반 재동기화가 성립하지 않습니다.
- 확인 테스트: `test_replication_log_assigns_sequential_offsets`
- 다시 볼 질문: append가 항상 마지막 offset 다음 값을 부여하는가?

### 2. duplicate delivery가 follower 상태를 또 바꾸는 경우
- 의심 파일: `../src/leader_follower/core.py`
- 깨지는 징후: 같은 batch를 두 번 적용해도 value와 watermark가 같아야 합니다.
- 확인 테스트: `test_follower_apply_is_idempotent`
- 다시 볼 질문: 이미 적용한 offset 이하의 entry를 명시적으로 건너뛰는가?

### 3. incremental sync에서 delete가 누락되는 경우
- 의심 파일: `../src/leader_follower/core.py`
- 깨지는 징후: follower는 최신 live value를 받더라도 delete entry를 놓치면 leader와 상태가 갈라집니다.
- 확인 테스트: `test_replicate_once_incremental_and_deletes`
- 다시 볼 질문: watermark 이후 slice를 보낼 때 delete record도 같은 흐름으로 포함하는가?
