# Problem Framing

정적 토폴로지와 정적 리더 배치를 가진 소규모 클러스터형 KV store를 구현한다. Python v1 범위는 shard router, single-node disk-backed storage engine, leader-follower replication, follower catch-up, routed read, 그리고 FastAPI 서비스 경계의 연결이다.

## Success Criteria

- key를 shard로 라우팅하고 shard별 leader/follower group 선택
- leader write가 log-backed store에 기록됨
- follower가 watermark 이후 entry만 catch-up
- follower restart 뒤에도 disk에서 상태 복원
- leader read와 follower read 모두 가능

## Source Provenance

- 직접적인 레거시 원본은 없다.
- 입력 개념은 `legacy/distributed-cluster/rpc-network`, `replication`, `sharding`과 `legacy/storage-engine/*` 프로젝트들에서 가져온다.
- Python 축소 이유: Go 트랙의 Raft/합의 심화는 제외하고 static topology 기반 흐름만 검증한다.
