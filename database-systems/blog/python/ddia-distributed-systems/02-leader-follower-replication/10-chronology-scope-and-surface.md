# Scope, Surface, First Sync

## 1. 문제를 다시 좁힌다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/problem/README.md)는 이번 랩의 요구를 네 가지로 자른다. 순차 offset을 갖는 mutation log, `put/delete` 복제, follower watermark 기반 incremental sync, 그리고 duplicate replay에도 깨지지 않는 idempotent apply다. 반대로 automatic leader election, consensus, quorum write, multi-leader replication은 이번 범위에서 뺀다고 못 박는다.

이 선언이 중요한 이유는, 코드를 읽을 때 "왜 장애 조치가 없지?" 같은 질문에 끌려가지 않게 해 주기 때문이다. 이 랩은 분산 합의를 설명하는 단계가 아니라, 복제를 가능하게 만드는 가장 작은 ordered log 모델을 분리해서 보여 주는 단계다.

## 2. 코드 표면은 세 층뿐이다

핵심 구현은 [`core.py`](/Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication/src/leader_follower/core.py) 하나에 모여 있다.

- `ReplicationLog`: `entries` 리스트에 `LogEntry(offset, operation, key, value)`를 append한다.
- `Leader`: `store`와 `ReplicationLog`를 함께 가진다.
- `Follower`: `store`와 `last_applied_offset`를 가진다.

여기에 orchestration helper로 `replicate_once(leader, follower)`가 붙는다. 이 함수는 `leader.log_from(follower.watermark() + 1)`로 follower가 아직 안 본 범위만 잘라 가져오고, `follower.apply(entries)`에 넘긴다. 즉, 이 랩의 "network protocol"은 사실상 `offset` 기반 incremental fetch 한 줄로 요약된다.

## 3. 첫 번째 write가 곧 첫 번째 replication contract다

leader의 `put()`과 `delete()`를 보면 둘 다 local store를 먼저 갱신하고 바로 뒤이어 log append를 수행한다.

```python
def put(self, key: str, value: str) -> int:
    self.store[key] = value
    return self.log.append("put", key, value)
```

```python
def delete(self, key: str) -> int:
    self.store.pop(key, None)
    return self.log.append("delete", key, None)
```

여기서 드러나는 현재 계약은 간단하다. leader 내부에서는 "store에 반영된 변화만 log entry로 남긴다." 반대로 write-ahead durability나 fsync, batch atomicity 같은 이야기는 아직 없다. 이 프로젝트가 보여 주는 것은 durable replication log가 아니라 ordered mutation stream의 shape다.

## 4. 실제 첫 sync를 다시 돌려 보면

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/ddia-distributed-systems/projects/02-leader-follower-replication
PYTHONPATH=src python3 -m leader_follower
```

출력은 아래와 같았다.

```python
{'applied': 1, 'value': '1'}
```

demo는 `leader.put("alpha", "1")` 뒤 `replicate_once()`를 한 번 실행해 follower가 정확히 한 entry만 받아 적용했다는 사실만 보여 준다. 이 짧은 출력이지만, 실제로는 세 가지를 동시에 확인한다.

- follower가 `watermark = -1`에서 시작한다
- `log_from(0)`이 첫 entry를 잘라 가져온다
- `apply()`가 `put`를 follower store에 반영한 뒤 applied count를 1로 돌려준다

## 5. 이 시점에서 보이는 한계

코드 표면만 봐도 이번 랩이 의도적으로 비워 둔 부분이 명확하다.

- follower는 leader와 네트워크로 연결돼 있지 않고 함수 호출로만 sync한다
- log compaction이나 snapshot install이 없어 log는 끝없이 늘어난다
- follower lag metric이나 commit acknowledgement가 없다
- invalid operation type을 방어하는 별도 검증이 없다

즉, 지금 단계의 문서는 "복제가 된다"는 막연한 진술보다, 어떤 최소 장치만으로 그 진술을 성립시키는지를 시간순으로 따라가는 쪽이 더 중요하다.
