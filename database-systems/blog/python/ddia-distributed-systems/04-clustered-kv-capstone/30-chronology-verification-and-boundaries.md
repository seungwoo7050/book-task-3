# Verification And Boundaries

## 1. 자동 검증은 통합 경로 네 개를 잡는다

2026-03-14 기준으로 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/04-clustered-kv-capstone
PYTHONPATH=src python3 -m pytest
```

결과는 아래와 같았다.

```text
4 passed, 1 warning in 0.23s
```

테스트는 네 갈래를 본다.

- write가 leader에 기록되고 follower에도 복제되는가
- auto replication을 끈 뒤 follower가 manual catch-up으로 따라잡는가
- node restart가 disk에서 상태를 복원하는가
- FastAPI route가 write/get/delete round trip을 통과하는가

## 2. 수동 재실행이 드러낸 중요한 차이

이번 재작성에서 추가로 확인한 결과는 아래와 같다.

- demo: `{'key': 'alpha', 'value': '1', 'found': True, 'shard_id': 'shard-b'}`
- `alpha_shard shard-b ('1', True, 'shard-b')`
- `beta_before_sync ('', False)`
- `beta_sync_applied 1`
- `beta_after_sync ('2', True)`
- `beta_leader_after_delete ('', False, 'shard-b')`
- `beta_follower_after_restart ('2', True)`

마지막 두 줄은 특히 중요하다. leader 쪽 delete는 즉시 반영되지만, auto replication이 꺼진 follower는 stale state를 로컬 디스크에서 그대로 되살린다. 즉 restart는 consistency repair가 아니라 local durability recovery다.

또 하나 중요한 분리는 read surface다. FastAPI round trip test와 demo가 보여 주는 공개 읽기 경로는 `cluster.read()`로 leader만 읽는다. follower stale/readiness를 보는 장면은 extra snippet처럼 `read_from_node()`를 직접 호출할 때만 드러난다. 그래서 HTTP layer만 보고 "follower read도 현재 API가 지원한다"고 쓰면 과장이다.

## 3. 현재 구현이 일부러 다루지 않는 것

capstone이라는 이름 때문에 범위를 과대평가하기 쉽지만, 비워 둔 부분이 분명하다.

- dynamic shard membership
- automatic failover와 leader election
- cross-node transport, timeout, retry, split brain
- quorum read/write와 consistency level
- background repair, anti-entropy, snapshot install
- follower lag나 health에 대한 observability

즉 이 프로젝트는 "작은 통합 경로"이지 "운영 가능한 분산 KV 완성본"이 아니다.

## 4. 이 문서에서 피한 과장

이번 재작성에서는 아래 같은 표현을 일부러 쓰지 않았다.

- "FastAPI 기반 분산 KV 서버를 완성했다"
- "restart 후 cluster consistency가 자동 복구된다"
- "follower read까지 HTTP에서 안정적으로 제공한다"

소스와 테스트가 실제로 보여 주는 것은 정적 topology 안에서 route, append, catch-up, reload, leader-read surface가 이어진다는 사실이다. 그보다 큰 주장은 근거가 없다.
