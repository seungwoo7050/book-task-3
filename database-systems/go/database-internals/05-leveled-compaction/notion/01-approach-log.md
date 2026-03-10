# 접근 기록

## 재현 순서 제안
이 프로젝트는 처음부터 한 번에 쓰기보다, 아래 4단계로 나눠 쌓는 편이 실패가 적습니다.

### 1. 입력과 출력 포맷을 먼저 고정한다
- 관련 파일: `../internal/sstable/sstable.go`
- 이유: compaction 결과를 어디에 어떻게 쓸지 먼저 알아야 merge 함수가 무엇을 반환해야 하는지 분명해집니다.
- 체크 포인트: `ReadAll`, `Get`, 파일명 규칙(`000001.sst`)을 먼저 이해합니다.

### 2. `mergeTwo`와 `KWayMerge`만 독립적으로 맞춘다
- 관련 파일: `../internal/compaction/compaction.go`, `../tests/compaction_test.go`
- 이유: compaction 전체 흐름보다 먼저 “같은 key면 누구를 남기는가”를 확정해야 나머지 상태 관리가 단순해집니다.
- 먼저 돌릴 테스트:

```bash
cd go/database-internals/05-leveled-compaction
go test ./... -run 'TestKWayMergeKeepsNewerValue|TestKWayMergeDropsTombstonesAtDeepestLevel' -v
```

### 3. `Manager`와 manifest를 붙인다
- 관련 파일: `../internal/compaction/compaction.go`, `../docs/concepts/manifest-atomicity.md`
- 이유: compaction은 merge만 맞으면 끝나는 작업이 아니라, 파일 집합과 metadata를 함께 바꾸는 작업이기 때문입니다.
- 구현 순서:
  1. `AddToLevel`
  2. `NeedsL0Compaction`
  3. `CompactL0ToL1`
  4. `SaveManifest`
  5. `LoadManifest`

### 4. 마지막에 데모와 통합 테스트로 닫는다
- 관련 파일: `../cmd/leveled-compaction/main.go`, `../tests/compaction_test.go`
- 이유: 단위 merge가 맞아도 L0 순서 뒤집기, 파일 삭제, manifest 저장 타이밍은 통합 흐름에서만 드러납니다.
- 닫는 명령:

```bash
cd go/database-internals/05-leveled-compaction
go test ./... -run 'TestCompactL0ToL1|TestManifestRoundTrip' -v
go run ./cmd/leveled-compaction
```

## 코드가 택한 핵심 판단
### L0를 newest-first source로 뒤집는다
- 관련 파일: `../internal/compaction/compaction.go`
- 판단: flush된 L0 파일은 old-to-new 순으로 쌓이므로, merge 입력에 넣기 직전 newest-first로 뒤집어야 최신 값이 우선권을 가집니다.

### tombstone 제거 조건을 `dropTombstones`로 명시한다
- 관련 파일: `../internal/compaction/compaction.go`
- 판단: tombstone 제거는 merge 알고리즘의 부수 효과가 아니라 깊이에 따라 바뀌는 정책입니다. 그래서 boolean 계약으로 밖에 드러내는 쪽이 읽기 쉽습니다.

### 결과 파일과 manifest 저장을 같은 함수 흐름 안에 둔다
- 관련 파일: `../internal/compaction/compaction.go`
- 판단: compaction에서 가장 위험한 버그는 merge 자체보다 metadata drift이므로, `CompactL0ToL1`이 파일 추가와 manifest 갱신을 직접 책임지게 했습니다.

## 기대 출력으로 닫는 방법
데모가 정상이라면 다음 세 줄이 나옵니다.

```text
apple=red
banana=gold
pear=green
```

여기서 가장 중요한 줄은 `banana=gold`입니다. 이 값이 `yellow`로 나오면 merge ordering이 틀린 것입니다.

## 포트폴리오 설명으로 바꿀 때 남길 장면
- `banana=gold` 한 줄로 newest-first merge 규칙을 설명할 수 있습니다.
- `c` tombstone이 deepest level에서만 사라진다는 테스트는 삭제 의미를 어떻게 보존했는지 보여 줍니다.
- `Result`와 `MANIFEST`를 함께 설명하면 compaction이 파일 정리가 아니라 metadata 포함 작업이라는 점이 드러납니다.
