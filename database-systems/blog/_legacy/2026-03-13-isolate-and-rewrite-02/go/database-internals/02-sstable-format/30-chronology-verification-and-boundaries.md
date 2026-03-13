# 30 02 SSTable Format를 다시 검증하고 경계를 닫기

이 글은 프로젝트의 마지막 구간이다. 테스트와 demo를 모두 남겨, 통과 신호와 구현 한계를 한 화면에 붙여 둔다.

## Phase 3
### Session 1

- 당시 목표:
  테스트 명령을 다시 돌려 핵심 invariant가 실제 회귀 신호로 남아 있는지 확인한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/02-sstable-format/tests/sstable_test.go`
- 처음 가설:
  pass 수치만 확인하면 충분할 거라고 생각했다.
- 실제 진행:
  `GOWORK=off go test ./...`를 다시 실행하고, 어떤 테스트가 있는지 이미 알고 있는 상태에서 pass 신호를 다시 읽었다.

CLI:

```bash
$ GOWORK=off go test ./...
?   	study.local/go/database-internals/projects/02-sstable-format/cmd/sstable-format	[no test files]
?   	study.local/go/database-internals/projects/02-sstable-format/internal/sstable	[no test files]
ok  	study.local/go/database-internals/projects/02-sstable-format/tests	(cached)
```

검증 신호:

- `go test ok, 6 tests`
- `TestTombstones`가 실제로 회귀 테스트 묶음 안에 남아 있다는 점이 중요했다.

핵심 코드:

```go
func TestTombstones(t *testing.T) {
	tempDir := t.TempDir()
	filePath := filepath.Join(tempDir, "000001.sst")

	table := sstable.New(filePath)
	if err := table.Write([]serializer.Record{
		{Key: "alive", Value: serializer.StringPtr("yes")},
		{Key: "dead", Value: nil},
	}); err != nil {
		t.Fatalf("write failed: %v", err)
	}
```

왜 이 코드가 중요했는가:

`TestTombstones`는 구현의 뒷부분에서 생길 수 있는 붕괴 지점을 문장보다 정확하게 고정한다. pass 숫자보다 중요한 건, 어떤 경계가 계속 회귀 대상으로 남아 있느냐였다.

새로 배운 것:

- 테스트는 단순 성공 여부보다, 어떤 invariant를 공개적으로 약속하는지 보여 주는 문서에 가깝다.

다음:

- demo entry point를 다시 실행해 테스트보다 얇은 표면에서 무엇을 보여 주는지 확인한다.

### Session 2

- 당시 목표:
  demo 출력과 README의 한계를 함께 읽어, 공개 표면과 내부 경계를 분리한다.
- 변경 단위:
  `database-systems/go/database-internals/projects/02-sstable-format/cmd/sstable-format/main.go`
- 처음 가설:
  demo는 테스트의 축약판일 뿐이라고 생각했다.
- 실제 진행:
  `GOWORK=off go run ./cmd/sstable-format`를 다시 실행해 마지막 한 줄을 확인하고, README의 `한계와 확장` bullet과 나란히 읽었다.

CLI:

```bash
$ GOWORK=off go run ./cmd/sstable-format
alpha => 1
beta => 2
gamma => <tombstone>
missing => <missing>
```

검증 신호:

- demo 핵심 줄: `missing => <missing>`
- 경계 메모: 현재 범위 밖: compression, block cache, range tombstone은 포함하지 않습니다.
- 경계 메모: 현재 범위 밖: multi-level manifest 관리와 compaction 연결은 다음 프로젝트로 넘깁니다.

핵심 코드:

```go
package main

import (
	"fmt"
	"os"
	"path/filepath"

	"study.local/go/database-internals/projects/02-sstable-format/internal/sstable"
	"study.local/go/shared/serializer"
)

func main() {
	tempDir, err := os.MkdirTemp("", "sstable-demo-")
	if err != nil {
		panic(err)
	}
```

왜 이 코드가 중요했는가:

demo entry point는 내부 구현 전체를 보여 주지 않지만, 독자에게 어떤 표면을 공개할지 결정한다. 테스트가 불변식을 지키는 동안 demo는 그중 무엇을 드러낼지 고르는 자리였다.

새로 배운 것:

- `Lookup Path`에서 정리한 요점처럼, reopen 시점에는 footer를 읽어 index section 위치를 계산한다.

다음:

- 이 프로젝트 이후에는 다음 트랙/다음 슬롯으로 넘어가더라도, 지금 고정한 invariant를 더 큰 저장 엔진이나 분산 경로 안에서 다시 만날 수 있다.
