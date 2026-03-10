# 문제 프레이밍

## 왜 이 프로젝트를 하는가
leader-follower replication만으로는 리더 교체를 설명할 수 없기 때문에, in-memory cluster 위에서 Raft의 최소 election과 commit rule을 구현한 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Go
- 이전 단계: 03 Shard Routing
- 다음 단계: 05 Clustered KV Capstone
- 지금 답하려는 질문: 여러 node 중 누가 leader인지 합의하고, 어떤 log index까지를 committed라고 불러도 되는지 어떻게 결정할 것인가?

## 이번 구현에서 성공으로 보는 것
- leader election이 수행되어 한 term에 leader가 정해져야 합니다.
- leader failover 후 새 leader가 다시 선출되어야 합니다.
- leader가 복제한 log가 commit index까지 반영되어야 합니다.
- 더 높은 term 메시지를 받은 node는 즉시 step down 해야 합니다.
- cluster 상태를 테스트에서 재현 가능하게 조작할 수 있어야 합니다.

## 먼저 열어 둘 파일
- `../internal/raft/raft.go`: `Node`, `Cluster`, term/state transition, append/commit 로직이 모두 모여 있습니다.
- `../tests/raft_test.go`: election, failover, commit, higher-term stepdown을 검증합니다.
- `../cmd/raft-lite/main.go`: 선출된 leader ID, commit index, log length를 출력합니다.
- `../docs/concepts/commit-rule.md`: 어느 시점에 commit index를 올릴 수 있는지 먼저 읽어 두면 좋습니다.

## 의도적으로 남겨 둔 범위 밖 항목
- log compaction snapshot, membership change, persistent storage는 다루지 않습니다.
- 실제 네트워크와 timeout jitter도 생략한 학습용 in-memory 모델입니다.

## 데모에서 바로 확인할 장면
- 선출된 leader ID, commit index, log length를 출력해 election과 commit이 한 번에 보이게 합니다.
