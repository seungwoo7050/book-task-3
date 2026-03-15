# Scope, File Layout, And First Reopen

## 1. 문제는 flush 그 자체가 아니라 immutable file format이다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/problem/README.md)는 data section, index section, footer, tombstone 표현, reopen 뒤 lookup을 요구한다. 반대로 compression, block cache, range tombstone, manifest, compaction 연결은 밖에 둔다.

이 분리가 중요하다. 이 랩은 LSM pipeline 전체를 다루지 않고, "정렬된 record를 디스크에 어떻게 고정해 나중에 다시 찾을 것인가"만 떼어낸다.

## 2. 코드 표면은 Write, LoadIndex, Lookup, ReadAll 네 개면 충분하다

[`sstable.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go)의 public 표면은 아래 네 메서드로 요약된다.

- `Write(records []serializer.Record) error`
- `LoadIndex() error`
- `Lookup(key string) (*string, bool, error)`
- `ReadAll() ([]serializer.Record, error)`

이 구조만 봐도 storage lifecycle이 보인다. write 시점에는 sorted records를 file layout으로 밀어 넣고, reopen 시점에는 footer를 읽어 index 영역을 다시 메모리로 적재한 뒤 point lookup을 수행한다.

## 3. 실제 demo는 reopen 뒤 네 가지 상태를 한 번에 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format
GOWORK=off go run ./cmd/sstable-format
```

출력은 아래와 같았다.

```text
alpha => 1
beta => 2
gamma => <tombstone>
missing => <missing>
```

demo는 temp file에 record 셋을 쓴 뒤 새 reader로 `LoadIndex()`를 호출하고 lookup을 수행한다. 여기서 한 번에 확인되는 사실은 네 가지다.

- live value는 정상 복원된다
- tombstone은 `found=true, value=nil` 의미로 보존된다
- missing key는 `found=false`로 분리된다
- lookup은 write 직후 같은 인스턴스가 아니라 reopen된 reader에서도 동작한다

## 4. layout 설명은 docs와 소스가 정확히 맞물린다

docs의 [`sstable-layout.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/docs/concepts/sstable-layout.md)와 [`lookup-path.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/docs/concepts/lookup-path.md)는 각각 file section 배치와 reopen 후 lookup 순서를 요약한다. 실제 구현도 똑같이 움직인다.

- 먼저 data section을 append한다
- 다음으로 `(key, offset)` index records를 append한다
- 마지막 8바이트 footer에 두 section 길이를 big-endian uint32로 쓴다
- reopen 시 footer를 읽고 index section 위치를 계산한다

즉 문서와 구현이 같은 포맷 계약을 가리키고 있다.
