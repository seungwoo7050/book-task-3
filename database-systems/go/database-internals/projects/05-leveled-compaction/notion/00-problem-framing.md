# 문제 프레이밍

## 왜 이 프로젝트를 하는가
03번 mini LSM store까지 오면 flush는 되지만 SSTable이 계속 쌓입니다. 그 상태에서는 newest-first read path가 맞더라도 읽기 비용이 계속 커집니다. 05번의 목적은 이 지점에서 “여러 정렬된 파일을 합치되, 최신 값과 삭제 의미를 잃지 않는 방법”을 직접 구현해 보는 것입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Go
- 이전 단계: 04 WAL Recovery
- 다음 단계: 06 Index Filter
- 지금 답하려는 질문: 여러 level에 흩어진 record를 합칠 때 최신 값을 유지하면서도 삭제를 너무 일찍 버리지 않으려면 어떤 merge 규칙이 필요한가?

## 이번 재현에서 먼저 고정할 입력
### 데모 입력
- `000001.sst`: `apple=red`, `banana=yellow`
- `000002.sst`: `banana=gold`, `pear=green`
- 기대 출력: `apple=red`, `banana=gold`, `pear=green`

### 통합 테스트 입력
- `TestCompactL0ToL1`은 L0에 4개 SSTable을 넣습니다.
- 같은 key가 여러 번 등장합니다. 예: `a=1`, `a=1-newer`
- tombstone도 들어갑니다. 예: `c=nil`
- deepest level compaction이므로 최종 결과에서 `c`는 살아남지 않아야 합니다.

## 이번 구현에서 성공으로 보는 것
- `KWayMerge`가 same key 충돌에서 최신 record를 남겨야 합니다.
- tombstone은 deepest level일 때만 제거되어야 합니다.
- `CompactL0ToL1`이 L0 파일들을 제거하고 새 L1 파일 하나를 추가해야 합니다.
- `Result{Added, Removed, DroppedTombstones}`가 실제 파일 변화와 일치해야 합니다.
- `SaveManifest`와 `LoadManifest`가 같은 level map과 `NextSequence`를 보존해야 합니다.

## 먼저 열어 둘 파일
- `../internal/compaction/compaction.go`: `mergeTwo`, `KWayMerge`, `CompactL0ToL1`, manifest 저장이 모두 모여 있습니다.
- `../internal/sstable/sstable.go`: compaction 결과를 읽고 다시 검증할 때 쓰는 포맷입니다.
- `../tests/compaction_test.go`: 규칙별 기대 결과가 가장 직접적으로 드러납니다.
- `../docs/concepts/manifest-atomicity.md`: “파일은 바뀌었는데 manifest가 안 바뀌면 어떻게 되는가”를 먼저 이해하게 해 줍니다.

## 재현할 때 꼭 붙잡을 불변식
- source 배열의 앞쪽이 더 최신이어야 합니다.
- L0 파일은 flush 순서대로 쌓이므로 merge 직전 newest-first 순서로 뒤집어야 합니다.
- deepest level이 아니면 tombstone을 남겨야 합니다.
- manifest는 새 파일 집합과 같은 시점의 truth를 가리켜야 합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- background compaction scheduler와 throttling은 없습니다.
- size-tiered 정책 비교와 multi-level planning도 없습니다.
- manifest journaling, crash injection, checksum 기반 recovery는 이 프로젝트 범위 밖입니다.

## 데모에서 바로 확인할 장면
- `go run ./cmd/leveled-compaction` 결과가 아래와 같이 나오면 merge ordering은 맞다고 봐도 됩니다.

```text
apple=red
banana=gold
pear=green
```
