# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. leader election이 반복되거나 leader가 둘 생기는 경우
- 의심 파일: `../internal/raft/raft.go`, `../tests/raft_test.go`
- 깨지는 징후: term/vote 전환 규칙이 어긋나면 cluster authority 설명이 무너집니다.
- 확인 테스트: `TestLeaderElection`, `TestLeaderFailover`
- 다시 볼 질문: 한 term에서 vote와 role transition이 한 번만 확정되도록 상태가 정리되는가?

### 2. 복제는 되었지만 commit index가 안 올라가는 경우
- 의심 파일: `../internal/raft/raft.go`, `../tests/raft_test.go`
- 깨지는 징후: append는 성공해도 commit rule이 틀리면 state machine에 적용할 수 없습니다.
- 확인 테스트: `TestLogReplicationAndCommit`
- 다시 볼 질문: majority replication을 만족한 가장 높은 index만 commit하도록 계산하는가?

### 3. higher term을 봐도 기존 leader가 내려오지 않는 경우
- 의심 파일: `../internal/raft/raft.go`, `../tests/raft_test.go`
- 깨지는 징후: term authority를 인정하지 않으면 failover 후 cluster가 둘로 갈립니다.
- 확인 테스트: `TestHigherTermForcesStepDown`
- 다시 볼 질문: RPC 처리 경로마다 “더 높은 term이면 step down” 분기가 빠짐없이 들어가 있는가?
