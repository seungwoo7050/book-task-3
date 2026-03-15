# Scope, Merge Surface, And First Compaction

## 1. 문제는 scheduler가 아니라 semantics-preserving merge다

[`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/problem/README.md)는 newer-first 우선순위가 있는 k-way merge, deepest level에서만 tombstone drop, 새 SSTable 이후 manifest atomic write, 입력 파일 cleanup을 요구한다. background scheduler, multi-level balancing, compression, block cache는 뺀다.

즉 이 랩의 focus는 "언제 compaction을 돌릴까"가 아니라, "돌렸을 때 어떤 결과를 안전하게 남길까"다.

## 2. 코드 표면은 Manager 하나에 모인다

[`compaction.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/internal/compaction/compaction.go)의 중심은 `Manager`다.

- `Levels map[int][]string`
- `NextSequence`
- `ManifestPath`
- `CompactL0ToL1()`
- `SaveManifest()`
- `LoadManifest()`

즉 compaction은 data merge 로직과 metadata 관리가 같은 객체 안에서 만난다. 현재는 L0->L1만 구현돼 있지만, 이 제한 덕분에 merge와 manifest atomicity를 더 선명하게 읽을 수 있다.

## 3. demo는 overwrite 우선순위를 짧게 보여 준다

2026-03-14에 아래 명령을 다시 실행했다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction
rm -rf .demo-data
GOWORK=off go run ./cmd/leveled-compaction
rm -rf .demo-data
```

출력은 아래와 같았다.

```text
apple=red
banana=gold
pear=green
```

demo는 L0 파일 두 개를 seed하고 compaction을 한 번 돌린다. 여기서 `banana=gold`가 중요한 이유는 older file의 `banana=yellow`보다 newer file의 값이 살아남는다는 걸 즉시 보여 주기 때문이다. 즉 merge는 단순 sort/concat이 아니라 source ordering semantics를 보존한다.

## 4. 추가 재실행으로 tombstone drop 조건도 고정했다

이번에 project root 내부 임시 Go 파일로 아래 결과를 추가로 확인했다.

```text
drop_at_deepest true 000003.sst [000003.sst]
lookup_after_drop false true
keep_above_deepest false 000003.sst
lookup_after_keep true true
```

이 결과는 tombstone handling이 level depth에 따라 달라진다는 걸 보여 준다.

- level 2가 비어 있으면 compaction 결과에서 tombstone이 아예 제거된다
- level 2에 더 깊은 데이터가 있다고 가정하면 tombstone은 유지된다

즉 "tombstone은 언제나 drop"도 아니고 "언제나 keep"도 아니다. deepest 여부가 조건이다.
