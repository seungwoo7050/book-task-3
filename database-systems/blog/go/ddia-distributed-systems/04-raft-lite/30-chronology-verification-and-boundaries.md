# 30 04 Raft Lite를 다시 돌려 보며 검증 신호와 경계를 정리하기

이 시리즈의 마지막 글이다. 구현 설명을 닫고, 테스트와 demo가 약속하는 범위를 다시 확인한다. 이때 남는 한계도 함께 적어 둔다.

## Phase 3 — 검증 신호와 한계를 확인하는 구간

이번 글에서는 먼저 테스트가 남긴 회귀 신호를 다시 읽고, 이어서 demo가 공개하는 표면과 README가 남겨 둔 한계를 함께 정리한다.

### Session 1 — 테스트가 남긴 회귀 신호 다시 보기

이번 세션의 목표는 테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인하는 것이었다. 초기 가설은 pass 수치만 확인하면 충분할 거라고 생각했다.

막상 다시 펼쳐 보니 `GOWORK=off go test ./...`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다. 특히 `go test ok, 4 tests`가 이번 판단을 굳혀 줬다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/tests/raft_test.go`

CLI:

```bash
$ GOWORK=off go test ./...
?   	study.local/go/ddia-distributed-systems/projects/04-raft-lite/cmd/raft-lite	[no test files]
?   	study.local/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft	[no test files]
ok  	study.local/go/ddia-distributed-systems/projects/04-raft-lite/tests	(cached)
```

검증 신호:
- `go test ok, 4 tests`
- `TestLogReplicationAndCommit`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```go
func TestLogReplicationAndCommit(t *testing.T) {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := electLeader(cluster, 20)
	if leader == nil {
		t.Fatalf("expected leader")
	}

	cluster.ClientRequest("SET x 1")
	cluster.ClientRequest("SET y 2")
	for i := 0; i < 20; i++ {
		cluster.Tick()
	}
```

왜 여기서 판단이 바뀌었는가:

`TestLogReplicationAndCommit`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 더 중요했던 건, 어떤 경계가 계속 회귀 테스트로 남아 있느냐였다.

이번 구간에서 새로 이해한 것:
- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음으로 넘긴 질문:
- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2 — demo가 공개하는 표면과 한계 정리하기

이 구간에서 먼저 붙잡으려 한 것은 demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리하는 것이었다. 처음 읽을 때는 demo는 테스트의 축약판일 뿐이라고 생각했다.

그런데 `GOWORK=off go run ./cmd/raft-lite`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다. 특히 demo 핵심 줄: `leader=n1 commit=0 log_len=1`라는 출력이 마지막 확인 지점이 됐다.

변경 단위:
- `database-systems/go/ddia-distributed-systems/projects/04-raft-lite/cmd/raft-lite/main.go`

CLI:

```bash
$ GOWORK=off go run ./cmd/raft-lite
leader=n1 commit=0 log_len=1
```

검증 신호:
- demo 핵심 줄: `leader=n1 commit=0 log_len=1`
- 경계 메모: 현재 범위 밖: production-grade persistence, membership change, snapshotting은 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: 실제 네트워크 transport와 disk-backed log는 후속 확장으로 남깁니다.

핵심 코드:

```go
package main

import (
	"fmt"

	"study.local/go/ddia-distributed-systems/projects/04-raft-lite/internal/raft"
)

func main() {
	cluster := raft.NewCluster([]string{"n1", "n2", "n3"})
	leader := waitLeader(cluster)
	cluster.ClientRequest("SET alpha 1")
	for i := 0; i < 10; i++ {
		cluster.Tick()
	}
	fmt.Printf("leader=%s commit=%d log_len=%d\n", leader.ID, leader.CommitIdx, len(leader.Log))
```

왜 여기서 판단이 바뀌었는가:

demo entry point는 내부 구현을 전부 보여 주지는 않지만, 독자가 처음 마주치는 공개 표면을 결정한다. 테스트가 invariant를 지키는 장치라면, demo는 그중 무엇을 밖으로 보여 줄지 고르는 자리였다.

이번 구간에서 새로 이해한 것:
- `Commit Rule`에서 정리한 요점처럼, leader는 단순히 local append 했다고 commit하지 않는다. 현재 term의 entry가 과반수 노드에 replicate 되었을 때만 `commitIndex`를 올린다.

다음으로 넘긴 질문:
- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
