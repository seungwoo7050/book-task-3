# 문제 프레이밍

## 왜 이 프로젝트를 하는가
앞서 만든 routing, replication, durability를 한 시스템 안에서 묶어 clustered key-value store의 최소 end-to-end 흐름을 보여 주는 캡스톤입니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Python
- 이전 단계: 03 Shard Routing
- 다음 단계: 이 트랙의 마지막 프로젝트
- 지금 답하려는 질문: key 하나의 write가 shard routing, leader 처리, follower catch-up, restart recovery를 거칠 때 어떤 경계와 책임 분리가 필요한가?

## 이번 구현에서 성공으로 보는 것
- key가 올바른 shard와 leader로 라우팅되어야 합니다.
- leader write가 follower catch-up까지 이어져 replica group 상태가 맞아야 합니다.
- delete도 같은 파이프라인을 따라가야 합니다.
- node 재시작 후 on-disk log를 읽어 상태를 복원해야 합니다.
- HTTP boundary에서 PUT/GET round trip까지 확인되어야 합니다.

## 먼저 열어 둘 파일
- `../src/clustered_kv/core.py`: `Store`/`DiskStore`, `ReplicaGroup`, `Cluster`가 어떤 경계로 나뉘는지 확인합니다.
- `../src/clustered_kv/app.py`: HTTP 요청을 core 로직에 얇게 연결하는 API boundary를 확인합니다.
- `../src/clustered_kv/__main__.py`: shard, follower, value가 한 번에 보이는 end-to-end 데모 진입점입니다.
- `../tests/test_clustered_kv.py`: route-to-leader, follower catch-up, restart recovery, API round trip이 어디서 깨지는지 바로 확인합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- 동적 membership과 자동 failover는 다루지 않습니다.
- full Raft integration, anti-entropy, rebalancing migration도 아직 없습니다.

## 데모에서 바로 확인할 장면
- FastAPI `PUT/GET /kv/alpha` round trip JSON을 바로 보여 줍니다.
