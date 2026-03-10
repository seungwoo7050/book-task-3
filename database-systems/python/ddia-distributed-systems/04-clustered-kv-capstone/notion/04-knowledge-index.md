# 지식 인덱스

## 핵심 용어
- `shard`: key 공간을 나눠 각 replica group이 맡는 단위입니다.
- `replica group`: 같은 shard를 가진 leader와 follower 집합입니다.
- `catch-up`: 뒤처진 follower가 leader의 mutation log를 따라잡는 과정입니다.
- `watermark`: follower가 어디까지 operation을 적용했는지 나타내는 위치입니다.
- `restart recovery`: 프로세스 재시작 후 disk 기록으로 현재 상태를 복원하는 동작입니다.

## 다시 볼 파일
- `../src/clustered_kv/core.py`: `Store`/`DiskStore`, `ReplicaGroup`, `Cluster`가 묶여 있는 핵심 구현입니다.
- `../src/clustered_kv/__main__.py`: 한 key write가 shard, follower, value로 이어지는 end-to-end 데모입니다.
- `../src/clustered_kv/app.py`: Python은 FastAPI boundary를 여기서 확인하고, Go는 테스트가 cluster 동작 전부를 보여 줍니다.
- `../tests/test_clustered_kv.py`: route-to-leader, follower catch-up, restart recovery, API round trip을 검증합니다.

## 개념 문서
- `../docs/concepts/replicated-write-pipeline.md`: write가 leader, disk, follower에 어떤 순서로 반영되는지 정리합니다.
- `../docs/concepts/static-topology.md`: 정적 shard와 replica 구성이 구조를 단순화하는 대신 무엇을 포기하는지 설명합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/test_clustered_kv.py`
- 다시 돌릴 테스트 이름: `test_write_routes_to_leader_and_replicates`, `test_follower_catch_up_and_delete`, `test_restart_node_loads_from_disk`, `test_fastapi_round_trip`
- 데모 경로: `../src/clustered_kv/__main__.py`, `../src/clustered_kv/app.py`
- 데모가 보여 주는 장면: Go 데모는 `alpha` write 후 shard ID, follower ID, 읽은 value, 성공 여부를 함께 출력합니다. Python 데모는 FastAPI `PUT/GET /kv/alpha` round trip JSON을 바로 보여 줍니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
