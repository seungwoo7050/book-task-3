# Evidence Ledger

## Source files used

- `problem/README.md`
  - 범위에서 빼는 항목이 명시돼 있어 capstone 과대해석을 막아 준다.
- `README.md`
  - 검증 명령과 공개 surface를 다시 확인하는 기준점으로 사용했다.
- `docs/concepts/static-topology.md`
  - topology가 왜 초기화 시점에 고정되는지 문장으로 확인했다.
- `docs/concepts/replicated-write-pipeline.md`
  - routing -> leader append -> follower catch-up -> read라는 설명을 코드와 대조했다.
- `internal/capstone/capstone.go`
  - `Store`, `shardRing`, `Cluster`, `SyncFollower`, `RestartNode`를 직접 추적했다.
- `tests/capstone_test.go`
  - replicated write, lagging follower catch-up, restart replay가 실제 회귀 테스트인지 확인했다.
- `cmd/clustered-kv/main.go`
  - 공개 demo가 어떤 표면까지만 보여 주는지 확인했다.

## Commands rerun

```bash
GOWORK=off go test ./...
rm -rf .demo-data && GOWORK=off go run ./cmd/clustered-kv
find .demo-data -type f | sort
```

## Key outputs

```text
ok  	study.local/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/tests	(cached)
key=alpha shard=shard-a follower=node-2 value=1 ok=true
.demo-data/node-1/shard-a.log
.demo-data/node-2/shard-a.log
```

## Manual boundary check

임시 테스트를 추가했다가 바로 삭제하고 다음 결과를 확보했다.

```text
restart_without_sync_ok=false
```

이 결과는 `RestartNode`가 lagging follower를 자동 catch-up하지 않고, 자신의 local log만 다시 읽는다는 점을 실행으로 확인한 것이다.

## Inferences called out explicitly

- stale follower read 가능성은 `ReadFromNode`가 freshness 검사 없이 local store만 읽는 코드에서 나온다.
- ordinary `Read`가 아니라 demo와 수동 경계 체크가 `ReadFromNode`를 직접 호출할 때만 follower freshness가 노출된다는 점을 같이 적었다.
- restart boundary는 위 임시 실행 결과와 `RestartNode` 구현을 함께 근거로 삼았다.
