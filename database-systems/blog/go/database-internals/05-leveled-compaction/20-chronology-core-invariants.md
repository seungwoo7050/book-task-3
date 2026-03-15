# Core Invariants

## 1. L0 input은 newest-first로 뒤집어서 merge에 들어간다

docs의 [`merge-ordering.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/docs/concepts/merge-ordering.md)는 L0 file list를 reverse 해서 newest-first source 배열로 만든다고 설명한다. 소스도 그대로다.

```go
for i := len(l0Files) - 1; i >= 0; i-- {
    records, err := readAll(filepath.Join(manager.DataDir, l0Files[i]))
    ...
    sources = append(sources, records)
}
```

이 reversal이 없으면 flush append 순서 때문에 oldest 값이 최신 값을 가릴 수 있다. 즉 compaction semantics의 첫 번째 invariant는 input ordering부터 시작한다.

## 2. mergeTwo는 같은 key에서 항상 왼쪽, 즉 newer source를 남긴다

`KWayMerge()`는 sources를 왼쪽에서 오른쪽으로 pairwise merge한다. `mergeTwo(newer, older)`의 충돌 분기는 아래처럼 구현돼 있다.

```go
case newer[i].Key == older[j].Key:
    merged = append(merged, newer[i])
    i++
    j++
```

즉 동일 key가 충돌하면 무조건 newer source record가 이긴다. tombstone도 예외가 아니다. 최신 tombstone이 있으면 오래된 live value는 결과에서 가려진다.

## 3. tombstone은 deepest level일 때만 제거된다

`CompactL0ToL1()`은 `dropTombstones := len(manager.Levels[2]) == 0`로 deepest 여부를 결정한다. 그리고 `KWayMerge(..., dropTombstones)`가 true면 merge 결과에서 `Value == nil`인 record를 걸러 낸다.

추가 재실행 결과도 이 조건을 뒷받침한다.

- `drop_at_deepest true ...` 뒤 `lookup_after_drop false true`
- `keep_above_deepest false ...` 뒤 `lookup_after_keep true true`

즉 더 깊은 level에 older version이 남아 있을 가능성이 있으면 tombstone을 남겨야 하고, 더 이상 아래가 없을 때만 삭제 표지를 실제로 없앨 수 있다.

## 4. manifest atomicity는 "새 결과 파일 먼저" 순서에 걸려 있다

docs의 [`manifest-atomicity.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/05-leveled-compaction/docs/concepts/manifest-atomicity.md)가 설명하는 순서는 소스와 같다.

1. 새 SSTable write
2. 메모리상의 `Levels` 갱신
3. `SaveManifest()` 호출
4. old input file removal

`SaveManifest()`는 shared `fileio.AtomicWrite()`를 사용한다. 즉 manifest 자체는 temp file write 후 rename으로 바뀐다. 이 설계 덕분에 적어도 "새 manifest가 절반만 써진 상태"는 피한다.

## 5. 하지만 메모리 state는 manifest write 전에 먼저 바뀐다

소스만 읽으면 보이는 중요한 경계도 있다. `CompactL0ToL1()`은 새 SSTable write 뒤 곧바로 `manager.Levels[0] = []string{}`와 `manager.Levels[1] = []string{newFileName}`를 적용하고, 그 다음에야 `SaveManifest()`를 호출한다.

즉 process 내부 메모리 state는 manifest atomic write보다 먼저 바뀐다. manifest 저장이 실패하면 in-memory state와 on-disk metadata가 잠시 어긋날 수 있다. 지금 프로젝트는 이 실패 복구를 다루지 않는다. 이것도 현재 범위의 분명한 한계다.
