# 학습 노트 안내

앞서 만든 routing, replication, durability를 한 시스템 안에서 묶어 “clustered key-value store”의 최소 end-to-end 흐름을 보여 주는 캡스톤입니다.

## 이 노트를 읽기 전에 잡을 질문
- key 하나의 write가 shard routing, leader 처리, follower catch-up, restart recovery를 거칠 때 어떤 경계와 책임 분리가 필요한가?
- 이 트랙을 포트폴리오 설명으로 바꿀 때 어떤 장면을 남길 것인가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../src/clustered_kv/core.py`, `../src/clustered_kv/__main__.py`, `../src/clustered_kv/app.py`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `test_write_routes_to_leader_and_replicates`, `test_follower_catch_up_and_delete`, `test_restart_node_loads_from_disk`, `test_fastapi_round_trip`입니다.
4. 데모 경로 `../src/clustered_kv/__main__.py`, `../src/clustered_kv/app.py`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: key 하나의 write가 shard routing, leader 처리, follower catch-up, restart recovery를 거칠 때 어떤 경계와 책임 분리가 필요한가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: 정적 topology로 shard와 replica group을 먼저 고정한다, write pipeline을 leader local apply와 follower catch-up으로 나눈다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: write가 잘못된 shard나 follower 없는 leader로 가는 경우, follower catch-up이 delete를 놓치는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `test_write_routes_to_leader_and_replicates`, `test_follower_catch_up_and_delete`, `test_restart_node_loads_from_disk`, `test_fastapi_round_trip`
- 데모 경로: `../src/clustered_kv/__main__.py`, `../src/clustered_kv/app.py`
- 데모가 보여 주는 장면: Go 데모는 `alpha` write 후 shard ID, follower ID, 읽은 value, 성공 여부를 함께 출력합니다. Python 데모는 FastAPI `PUT/GET /kv/alpha` round trip JSON을 바로 보여 줍니다.
- 개념 문서: `../docs/concepts/replicated-write-pipeline.md`, `../docs/concepts/static-topology.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
