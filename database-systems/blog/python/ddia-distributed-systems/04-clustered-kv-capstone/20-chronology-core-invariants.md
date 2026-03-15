# Core Invariants

## 1. DiskStore는 append-only log를 다시 읽어 메모리를 재구성한다

`DiskStore`의 중심은 `_load()`와 `apply()`다. `_load()`는 파일의 각 line을 JSON으로 읽어 `Operation`으로 만들고, `_apply_in_memory()`를 통해 현재 `data` dict를 복원한다. `apply()`는 새 operation을 JSON line으로 append한 뒤 메모리에 반영한다.

이 구조는 앞선 storage 랩의 메시지를 capstone 안에 다시 가져온다. durable state는 "현재 dict를 dump한 스냅샷"이 아니라 "append-only operation log를 replay해서 재구성되는 상태"다.

## 2. sequential offset이 leader와 follower 사이의 공통 계약이다

`append_put()`와 `append_delete()`는 새 operation의 offset을 `len(self.log)`로 잡는다. follower 측 `apply()`도 `if op.offset < len(self.log): return`과 `if op.offset != len(self.log): raise ValueError(...)`를 갖고 있다.

이 말은 곧, follower catch-up이 "같은 순서의 로그를 빠짐없이 이어 붙인다"는 가정 위에 선다는 뜻이다. 이미 가진 offset보다 낮으면 skip하고, 중간이 비어 있으면 바로 예외를 낸다. production replication처럼 gap repair나 out-of-order buffering은 없다.

## 3. follower catch-up은 leader watermark가 아니라 follower watermark에서 출발한다

`Cluster.sync_follower()`는 leader store에서 `entries_from(follower_store.watermark() + 1)`을 가져온다.

```python
entries = leader_store.entries_from(follower_store.watermark() + 1)
for entry in entries:
    follower_store.apply(entry)
```

즉 catch-up 범위는 leader가 알려 주는 committed watermark가 아니라, follower가 현재 어디까지 갖고 있는지를 바탕으로 잘린다. 이 설계는 앞선 leader-follower 랩과 같은 아이디어를 disk-backed store 위에 다시 얹은 것이다.

## 4. auto_replicate는 "즉시 복제 여부"만 바꾸고 write 자체는 멈추지 않는다

`Cluster.set_auto_replicate(False)`를 켜도 leader write는 계속 진행된다. 단지 follower sync loop를 건너뛴다. 2026-03-14에 추가 실행한 snippet 결과는 아래와 같았다.

```python
alpha_shard shard-b ('1', True, 'shard-b')
beta_before_sync ('', False)
beta_sync_applied 1
beta_after_sync ('2', True)
beta_leader_after_delete ('', False, 'shard-b')
beta_follower_after_restart ('2', True)
```

여기서 중요한 건 마지막 줄이다. auto replication을 끈 상태에서 follower가 한 번만 따라잡은 뒤, leader에서 delete가 일어나도 follower는 다시 sync하지 않으면 stale한 값을 계속 들고 있다. restart는 follower를 leader에 다시 맞춰 주는 기능이 아니라, 자기 로컬 로그를 다시 읽는 기능일 뿐이다.

## 5. FastAPI surface는 cluster semantics를 일부만 노출한다

`create_app()`의 세 route는 모두 `Cluster` 메서드로 연결되지만, 외부에 노출되는 semantics는 제한적이다.

- `PUT /kv/{key}`는 leader write와 shard id만 반환한다.
- `GET /kv/{key}`는 leader read 결과만 반환한다.
- `DELETE /kv/{key}`는 follower sync 상태를 따로 드러내지 않는다.

즉 follower read 가능성, replication lag, 특정 node 선택은 내부 테스트와 helper 메서드에서는 존재하지만 public API 계약으로는 노출되지 않는다. 이게 현재 capstone의 "분산 내부와 외부 표면 사이의 간극"이다.
