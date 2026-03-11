# 지식 인덱스

## 핵심 용어
- `SSTable`: 정렬된 key/value 집합을 immutable file로 저장한 구조입니다.
- `footer`: 파일 끝에서 index 위치를 알려 주는 메타데이터입니다.
- `index entry`: 특정 key 범위가 어느 파일 offset에 있는지 가리키는 항목입니다.
- `point lookup`: 전체 scan 대신 특정 key 하나를 빠르게 찾는 읽기 경로입니다.
- `ReadAll`: 검증과 디버깅을 위해 파일 전체 내용을 순서대로 복원하는 도구입니다.

## 다시 볼 파일
- `../internal/sstable/sstable.go`: `SSTable`, `IndexEntry`, footer 처리와 `Lookup` 구현이 모여 있습니다.
- `../tests/sstable_test.go`: round-trip, tombstone, large dataset, malformed footer를 직접 검증합니다.
- `../cmd/sstable-format/main.go`: `alpha`, `beta`, `gamma`를 파일로 쓴 뒤 lookup 결과를 출력합니다.
- `../docs/concepts/sstable-layout.md`: data 영역, index, footer의 배치를 먼저 이해할 때 도움이 됩니다.

## 개념 문서
- `../docs/concepts/lookup-path.md`: footer와 index를 거쳐 원하는 key가 있는 데이터 구간을 찾는 순서를 설명합니다.
- `../docs/concepts/sstable-layout.md`: data 영역, index, footer가 파일 안에서 어떻게 배치되는지 요약합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/sstable_test.go`
- 다시 돌릴 테스트 이름: `TestRoundTripSortedEntries`, `TestMissingKey`, `TestTombstones`, `TestReadAll`, `TestLargeDataset`, `TestMalformedFooter`
- 데모 경로: `../cmd/sstable-format/main.go`
- 데모가 보여 주는 장면: 몇 개의 sample entry를 파일로 쓴 뒤 `alpha`, `beta`, `gamma` lookup을 출력해 live value, missing, tombstone을 함께 보여 줍니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
