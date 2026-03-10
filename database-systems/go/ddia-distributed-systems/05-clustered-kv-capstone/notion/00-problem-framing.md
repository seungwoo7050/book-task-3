# 문제 프레이밍

## 왜 이 프로젝트를 하는가
이 캡스톤은 이전 프로젝트에서 따로 만들었던 라우팅, 복제, 합의 감각, 디스크 복원을 한 파이프라인으로 묶습니다. 핵심은 “새 알고리즘을 더 넣는 것”이 아니라 “이전 조각들이 실제로 함께 작동하는가”를 눈으로 확인하는 것입니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Go
- 이전 단계: 04 Raft Lite
- 다음 단계: 이 트랙의 마지막 프로젝트
- 지금 답하려는 질문: key 하나의 write가 shard routing, leader 처리, follower catch-up, restart recovery를 거칠 때 어떤 경계와 책임 분리가 필요한가?

## 이번 재현에서 먼저 고정할 topology
- shard 2개: `shard-a`, `shard-b`
- node 3개: `node-1`, `node-2`, `node-3`
- replica group:
  - `shard-a`: leader=`node-1`, follower=`node-2`
  - `shard-b`: leader=`node-2`, follower=`node-3`
- virtual nodes: 64

## 이번 구현에서 성공으로 보는 것
- `Put("alpha", "1")`가 올바른 shard leader로 라우팅되어야 합니다.
- leader write가 follower catch-up까지 이어져 follower에서도 같은 value가 보여야 합니다.
- `SetAutoReplicate(false)` 상태에서는 follower lag가 재현되어야 합니다.
- `SyncFollower`를 호출하면 lag가 해소되어야 합니다.
- `RestartNode` 뒤에도 디스크 로그를 읽어 값이 복원되어야 합니다.

## 먼저 열어 둘 파일
- `../internal/capstone/capstone.go`: `Store`, `ReplicaGroup`, `Node`, `Cluster`, `shardRing` 구현 전체가 있습니다.
- `../tests/capstone_test.go`: route, catch-up, restart recovery를 시나리오별로 재현합니다.
- `../cmd/clustered-kv/main.go`: 가장 짧은 end-to-end 데모 진입점입니다.
- `../docs/concepts/static-topology.md`: 왜 정적 topology를 먼저 택했는지 설명합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- 동적 membership과 자동 failover는 없습니다.
- full Raft integration과 leader election 연결도 없습니다.
- rebalancing migration, anti-entropy, cross-shard transaction도 범위 밖입니다.

## 데모에서 바로 확인할 장면
- `go run ./cmd/clustered-kv`를 실행했을 때 아래 한 줄이 나오면 route, write, replication 기본 경로는 맞습니다.

```text
key=alpha shard=shard-a follower=node-2 value=1 ok=true
```
