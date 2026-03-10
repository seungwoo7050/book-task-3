# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. footer offset 계산이 틀리는 경우
- 의심 파일: `../internal/sstable/sstable.go`, `../tests/sstable_test.go`
- 깨지는 징후: index를 읽을 시작 위치가 어긋나면 모든 lookup이 실패하거나 잘못된 block을 가리킵니다.
- 확인 테스트: `TestRoundTripSortedEntries`, `TestMalformedFooter`
- 다시 볼 질문: write 시점에 기록한 index offset과 read 시점의 footer decode가 같은 byte convention을 쓰는가?

### 2. missing key와 tombstone을 같은 상태로 다루는 경우
- 의심 파일: `../internal/sstable/sstable.go`, `../tests/sstable_test.go`
- 깨지는 징후: 삭제된 key와 처음부터 없는 key가 같은 결과로 보이면 상위 LSM read path가 잘못된 결정을 내립니다.
- 확인 테스트: `TestMissingKey`, `TestTombstones`
- 다시 볼 질문: lookup 결과에 “found but tombstoned” 상태를 남길 수 있는가?

### 3. 큰 데이터셋에서 index 경계가 틀리는 경우
- 의심 파일: `../internal/sstable/sstable.go`, `../tests/sstable_test.go`
- 깨지는 징후: 작은 예제는 통과하지만 dataset이 커지면 offset 산술 실수나 search boundary 오류가 드러납니다.
- 확인 테스트: `TestLargeDataset`, `TestReadAll`
- 다시 볼 질문: binary search가 선택한 index entry가 실제 data block 경계와 일치하는가?
