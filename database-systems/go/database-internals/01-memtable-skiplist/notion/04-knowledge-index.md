# 지식 인덱스

## 핵심 용어
- `memtable`: flush 전까지 최신 쓰기를 담는 in-memory 정렬 구조입니다.
- `tombstone`: 삭제를 “없앰”이 아니라 “삭제되었다고 기록함”으로 표현하는 marker입니다.
- `byte size`: 대략적 메모리 사용량으로 flush threshold 판단에 쓰는 값입니다.
- `skip list level`: 탐색 속도를 높이기 위해 여러 높이의 forward pointer를 두는 층입니다.
- `ordered scan`: key 오름차순 전체 순회로, SSTable flush의 입력이 됩니다.

## 다시 볼 파일
- `../internal/skiplist/skiplist.go`: `SkipList`, `Entry`, `ValueState`가 모여 있는 핵심 구현입니다.
- `../tests/skiplist_test.go`: 정렬 순서, tombstone 유지, byte size 추적이 어디서 깨지는지 바로 확인할 수 있는 검증 앵커입니다.
- `../cmd/skiplist-demo/main.go`: `banana` 삭제 후 ordered entries와 `size`/`byteSize`를 함께 출력하는 데모입니다.
- `../docs/concepts/skiplist-invariants.md`: 탐색과 순회에서 어떤 invariant를 지켜야 하는지 정리한 개념 메모입니다.

## 개념 문서
- `../docs/concepts/skiplist-invariants.md`: 탐색 경로와 정렬 순회가 어떤 불변식 위에서 성립하는지 정리합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/skiplist_test.go`
- 다시 돌릴 테스트 이름: `TestPutAndGet`, `TestMissingKey`, `TestUpdateKeepsLogicalSize`, `TestManyInserts`, `TestDeleteProducesTombstone`, `TestEntriesStaySorted`, `TestEntriesIncludeTombstones`, `TestByteSizeTracking`, `TestClear`
- 데모 경로: `../cmd/skiplist-demo/main.go`
- 데모가 보여 주는 장면: `banana`, `apple`, `carrot`를 넣고 `banana`를 tombstone으로 바꾼 뒤 ordered entries와 `size`/`byteSize`를 같이 출력합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
