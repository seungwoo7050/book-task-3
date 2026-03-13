# 30 Integration And Tradeoffs

## Day 1
### Session 5

이 프로젝트의 장점은 boundary가 얇다는 점이다. FastAPI layer는 core 결과를 거의 그대로 반환한다.

```python
@app.get("/kv/{key}")
def get_value(key: str):
    value, found, shard_id = cluster.read(key)
    return {"key": key, "value": value if found else None, "found": found, "shard_id": shard_id}
```

framework가 분산 로직을 숨기지 않는다. 그래서 system을 이해하기 쉽다.

tradeoff:

- 장점:
  - routing/replication/durability 흐름이 코드에서 직접 보임
  - 테스트가 core와 API 경계를 분리해 검증 가능
- 한계:
  - topology 고정(static groups)
  - leader election, quorum commit 없음
  - partition/recovery 시나리오 없음

CLI:

```bash
cd python/ddia-distributed-systems/projects/04-clustered-kv-capstone
PYTHONPATH=src python3 -m pytest -q
```

`test_fastapi_round_trip`의 역할도 명확하다.

- PUT에서 `shard_id` 반환
- GET에서 `found/value/shard_id` 확인
- DELETE 이후 not found 확인

즉 API는 단순 CRUD wrapper가 아니라 cluster core semantics를 외부에 투명하게 노출하는 표면이다.

다음 질문:

- control plane(data plane과 분리된 membership/election)을 어디서 도입할까
- shard rebalance 중 write path를 멈추지 않으려면 어떤 메타데이터가 더 필요할까