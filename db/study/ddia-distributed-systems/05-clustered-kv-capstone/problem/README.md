# Problem Framing

정적 토폴로지와 정적 리더 배치를 가진 소규모 클러스터형 KV store를 구현한다. v1 범위는 shard router, single-node disk-backed storage engine, leader-follower replication, follower catch-up, routed read의 연결이다.

## Success Criteria

- key를 shard로 라우팅하고 shard별 leader/follower group 선택
- leader write가 log-backed store에 기록됨
- follower가 watermark 이후 entry만 catch-up
- follower restart 뒤에도 disk에서 상태 복원
- leader read와 follower read 모두 가능

## Source Provenance

- 직접적인 레거시 원본은 없다.
- 입력 개념은 `legacy/distributed-cluster/rpc-network`, `replication`, `sharding`과 `legacy/storage-engine/*` 프로젝트들에서 가져온다.
- 추가 이유: 레거시에는 분산 모듈과 저장 엔진을 실제 하나의 흐름으로 연결하는 프로젝트가 없었다.
