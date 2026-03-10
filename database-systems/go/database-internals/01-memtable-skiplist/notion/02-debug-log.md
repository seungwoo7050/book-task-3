# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. overwrite에서 byte size가 이중 집계되는 경우
- 의심 파일: `../internal/skiplist/skiplist.go`, `../tests/skiplist_test.go`
- 깨지는 징후: 같은 key를 갱신했는데 `Size`와 `ByteSize`가 함께 증가하면 flush threshold 판단이 틀어집니다.
- 확인 테스트: `TestUpdateKeepsLogicalSize`, `TestByteSizeTracking`
- 다시 볼 질문: 기존 value 길이를 차감한 뒤 새 value 길이를 더하는가?

### 2. delete가 physical remove로 처리되는 경우
- 의심 파일: `../internal/skiplist/skiplist.go`, `../tests/skiplist_test.go`
- 깨지는 징후: 삭제 후 순회 결과에서 key가 완전히 사라지면 이후 SSTable flush에서 tombstone semantics가 끊깁니다.
- 확인 테스트: `TestDeleteProducesTombstone`, `TestEntriesIncludeTombstones`
- 다시 볼 질문: 삭제는 노드 제거가 아니라 tombstone 값으로의 상태 전환인가?

### 3. 삽입 경로가 정렬 invariant를 깨는 경우
- 의심 파일: `../internal/skiplist/skiplist.go`, `../tests/skiplist_test.go`
- 깨지는 징후: 많은 key를 넣은 뒤 `Entries()` 결과가 뒤섞이면 skip list level 연결이나 predecessor 업데이트가 틀린 것입니다.
- 확인 테스트: `TestManyInserts`, `TestEntriesStaySorted`
- 다시 볼 질문: 각 level에서 predecessor 배열이 올바르게 갱신되는가?
