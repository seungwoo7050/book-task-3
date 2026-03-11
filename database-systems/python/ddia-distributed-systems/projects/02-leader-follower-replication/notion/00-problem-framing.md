# 문제 프레이밍

## 왜 이 프로젝트를 하는가
consensus를 넣기 전 단계에서 append-only mutation log와 watermark 기반 incremental sync만으로 leader-follower replication을 보여 주는 프로젝트입니다.

## 커리큘럼 안에서의 위치
- 트랙: DDIA Distributed Systems / Python
- 이전 단계: 01 RPC Framing
- 다음 단계: 03 Shard Routing
- 지금 답하려는 질문: follower가 중간에 끊겼다가 다시 붙어도 leader log에서 필요한 부분만 안전하게 따라오게 하려면 어떤 상태를 기억해야 하는가?

## 이번 구현에서 성공으로 보는 것
- leader log가 연속 offset을 부여해야 합니다.
- follower가 중복 entry를 다시 받아도 idempotent하게 적용해야 합니다.
- watermark 이후 entry만 incremental하게 전송해야 합니다.
- delete도 mutation log 안에서 같은 방식으로 복제되어야 합니다.
- replication 후 follower 상태와 watermark가 leader와 일관되게 맞아야 합니다.

## 먼저 열어 둘 파일
- `../src/leader_follower/core.py`: `ReplicationLog`, `Leader`, `Follower`, `replicate_once`가 어떤 상태를 공유하는지 확인합니다.
- `../src/leader_follower/__main__.py`: delete 이후 follower value와 watermark를 가장 짧게 보여 주는 데모 진입점입니다.
- `../tests/test_replication.py`: offset 부여, follower idempotence, incremental delete replication이 어디서 깨지는지 바로 확인합니다.
- `../docs/concepts/log-shipping.md`: leader가 follower에 어떤 단위로 log를 보내는지 먼저 복기합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- leader election과 quorum commit은 아직 없습니다.
- 네트워크 partition, batch retry, backpressure도 포함하지 않습니다.

## 데모에서 바로 확인할 장면
- `alpha` 삭제 후 적용된 entry 수와 follower value를 dict로 보여 줍니다.
