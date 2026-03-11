# 디버그 포인트

이 파일은 “틀리면 어떤 증상이 보이는가”를 빠르게 재현하기 위한 메모입니다. 05번 문서는 특히 재현성이 중요하므로, 각 항목마다 바로 돌릴 명령과 기대 현상을 같이 적어 둡니다.

## 1. newest-first 순서를 놓쳐 오래된 value가 남는 경우
- 의심 파일: `../internal/compaction/compaction.go`
- 재현 명령:

```bash
cd go/database-internals/projects/05-leveled-compaction
go run ./cmd/leveled-compaction
```

- 정상 출력:

```text
apple=red
banana=gold
pear=green
```

- 깨졌을 때 보이는 징후: `banana=yellow`가 나오거나 `TestKWayMergeKeepsNewerValue`가 깨집니다.
- 확인 테스트: `TestKWayMergeKeepsNewerValue`
- 다시 볼 질문: L0 파일 목록을 merge source로 만들기 전에 newest-first로 뒤집었는가?

## 2. tombstone을 너무 일찍 지워 delete가 되살아나는 경우
- 의심 파일: `../internal/compaction/compaction.go`, `../tests/compaction_test.go`
- 재현 명령:

```bash
cd go/database-internals/projects/05-leveled-compaction
go test ./... -run TestCompactL0ToL1 -v
```

- 정상 기대: compacted SSTable에서 `c`는 조회되지 않아야 합니다.
- 깨졌을 때 보이는 징후: `compacted.Get("c")`가 다시 값을 반환하거나, 테스트가 tombstone 제거 조건에서 실패합니다.
- 확인 테스트: `TestKWayMergeDropsTombstonesAtDeepestLevel`, `TestCompactL0ToL1`
- 다시 볼 질문: 지금 compaction하는 대상이 실제로 deepest level인지 확인한 뒤에만 tombstone을 제거하는가?

## 3. manifest와 실제 파일 집합이 어긋나는 경우
- 의심 파일: `../internal/compaction/compaction.go`
- 재현 명령:

```bash
cd go/database-internals/projects/05-leveled-compaction
go test ./... -run 'TestCompactL0ToL1|TestManifestRoundTrip' -v
```

- 정상 기대:
  - `result.Added`는 1개 파일
  - `result.Removed`는 기존 L0 파일 4개
  - manifest load 후 `Levels`와 `NextSequence`가 저장 직전과 같음
- 깨졌을 때 보이는 징후: 테스트는 통과하지 않거나, manifest에는 새 파일이 있는데 실제 파일이 없고, 또는 반대로 파일은 있는데 manifest가 옛 상태를 가리킵니다.
- 확인 테스트: `TestManifestRoundTrip`
- 다시 볼 질문: 새 SSTable을 먼저 쓴 뒤 manifest를 atomic write로 저장하고, 마지막에 입력 파일을 지우는 순서를 지키는가?

## 4. 입력 파일 삭제를 빠뜨려 compaction이 끝났는데 공간이 안 줄어드는 경우
- 의심 파일: `../internal/compaction/compaction.go`
- 재현 명령:

```bash
cd go/database-internals/projects/05-leveled-compaction
go test ./... -run TestCompactL0ToL1 -v
```

- 정상 기대: `result.Removed`에 들어 있는 파일은 실제 디스크에서 사라져야 합니다.
- 깨졌을 때 보이는 징후: 테스트 끝부분의 `os.Stat` 검사에서 removed 파일이 계속 존재합니다.
- 확인 테스트: `TestCompactL0ToL1`
- 다시 볼 질문: level map만 갱신하고 실제 입력 파일 삭제를 빼먹지 않았는가?
