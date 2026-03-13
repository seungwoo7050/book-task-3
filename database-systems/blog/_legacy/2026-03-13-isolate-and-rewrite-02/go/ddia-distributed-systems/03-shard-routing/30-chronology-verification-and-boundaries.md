# 30 03 Shard Routing를 다시 검증하고 경계를 닫기

이 글은 프로젝트의 마지막 구간이다. 테스트와 demo를 모두 남겨, 통과 신호와 구현 한계를 한 화면에 붙여 둔다.

## Phase 3
### Session 1

- 당시 목표:
  테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/tests/routing_test.go`
- 처음 가설:
  pass 수치만 확인하면 충분할 거라고 생각했다.
- 실제 진행:
  `GOWORK=off go test ./...`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다.

CLI:

```bash
$ GOWORK=off go test ./...
?   	study.local/go/ddia-distributed-systems/projects/03-shard-routing/cmd/shard-routing	[no test files]
?   	study.local/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing	[no test files]
ok  	study.local/go/ddia-distributed-systems/projects/03-shard-routing/tests	(cached)
```

검증 신호:

- `go test ok, 3 tests`
- `TestBatchRouting`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```go
func TestBatchRouting(t *testing.T) {
	ring := routing.NewRing(100)
	ring.AddNode("node-a")
	ring.AddNode("node-b")
	router := routing.NewRouter(ring)

	grouped := router.RouteBatch([]string{"k1", "k2", "k3", "k4", "k5"})
	total := 0
	for _, keys := range grouped {
		total += len(keys)
	}
	if total != 5 {
		t.Fatalf("expected 5 routed keys, got %d", total)
	}
```

왜 이 코드가 중요했는가:

`TestBatchRouting`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 중요한 건, 어떤 경계가 계속 회귀 대상으로 남아 있느냐였다.

새로 배운 것:

- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음:

- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2

- 당시 목표:
  demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리한다.
- 변경 단위:
  `database-systems/go/ddia-distributed-systems/projects/03-shard-routing/cmd/shard-routing/main.go`
- 처음 가설:
  demo는 테스트의 축약판일 뿐이라고 생각했다.
- 실제 진행:
  `GOWORK=off go run ./cmd/shard-routing`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다.

CLI:

```bash
$ GOWORK=off go run ./cmd/shard-routing
alpha -> node-a
beta -> node-c
gamma -> node-b
```

검증 신호:

- demo 핵심 줄: `gamma -> node-b`
- 경계 메모: 현재 범위 밖: dynamic membership protocol과 gossip은 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: 실제 데이터 이동과 rebalancing execution은 capstone 이후 확장 범위입니다.

핵심 코드:

```go
package main

import (
	"fmt"

	"study.local/go/ddia-distributed-systems/projects/03-shard-routing/internal/routing"
)

func main() {
	ring := routing.NewRing(64)
	ring.AddNode("node-a")
	ring.AddNode("node-b")
	ring.AddNode("node-c")
```

왜 이 코드가 중요했는가:

demo entry point는 내부 구현 전체를 보여 주지 않지만, 독자에게 어떤 표면을 공개할지 결정한다. 테스트가 불변식을 지키는 동안 demo는 그중 무엇을 드러낼지 고르는 자리였다.

새로 배운 것:

- `Rebalance Accounting`에서 정리한 요점처럼, consistent hashing의 핵심 가치는 membership 변화가 있을 때 전체 key를 거의 다 움직이지 않는다는 점이다. 그래서 구현을 검증할 때는 "새 ring이 얼마나 적은 key를 옮겼는가"를 함께 본다.

다음:

- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
