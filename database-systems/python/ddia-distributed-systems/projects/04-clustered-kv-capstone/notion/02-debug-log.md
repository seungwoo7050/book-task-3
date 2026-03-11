# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. write가 잘못된 shard나 follower 없는 leader로 가는 경우
- 의심 파일: `../src/clustered_kv/core.py`
- 깨지는 징후: routing과 replica group 매핑이 어긋나면 이후 단계가 모두 무의미해집니다.
- 확인 테스트: `test_write_routes_to_leader_and_replicates`
- 다시 볼 질문: key -> shard -> replica group -> leader 경로가 한 함수 체인으로 일관되게 연결되는가?

### 2. follower catch-up이 delete를 놓치는 경우
- 의심 파일: `../src/clustered_kv/core.py`
- 깨지는 징후: live value는 따라왔는데 tombstone이 빠지면 follower가 leader와 다른 세계를 보게 됩니다.
- 확인 테스트: `test_follower_catch_up_and_delete`
- 다시 볼 질문: follower가 watermark 이후 operation을 읽을 때 delete도 같은 log entry로 적용하는가?

### 3. 재시작 후 disk state가 복원되지 않는 경우
- 의심 파일: `../src/clustered_kv/core.py`
- 깨지는 징후: 메모리 상태만 맞고 restart 후 빈 store가 뜨면 durability 설명이 무너집니다.
- 확인 테스트: `test_restart_node_loads_from_disk`
- 다시 볼 질문: node 초기화 시 on-disk op log를 읽어 현재 map과 watermark를 재구성하는가?

### 4. HTTP boundary와 core logic이 서로 다른 결과를 내는 경우
- 의심 파일: `../src/clustered_kv/app.py`, `../tests/test_clustered_kv.py`
- 깨지는 징후: core 테스트는 통과하지만 API round trip이 틀리면 service boundary 설계가 어긋난 것입니다.
- 확인 테스트: `test_fastapi_round_trip`
- 다시 볼 질문: FastAPI handler가 core `Cluster` 인터페이스만 호출하고 별도 state를 갖지 않는가?
