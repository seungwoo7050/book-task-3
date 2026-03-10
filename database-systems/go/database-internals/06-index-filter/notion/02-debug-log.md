# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. bloom filter가 false negative를 내는 경우
- 의심 파일: `../internal/bloomfilter/bloom_filter.go`, `../tests/index_filter_test.go`
- 깨지는 징후: 없는 key를 빨리 거르는 것보다, 있는 key를 없다고 말하지 않는 것이 훨씬 중요합니다.
- 확인 테스트: `TestBloomFilterHasNoFalseNegatives`
- 다시 볼 질문: hash 조합과 bit setting이 같은 규칙을 쓰고 있는가?

### 2. false positive rate가 비정상적으로 높은 경우
- 의심 파일: `../internal/bloomfilter/bloom_filter.go`
- 깨지는 징후: bit budget이나 hash count 계산이 어긋나면 filter가 사실상 아무 쓸모가 없어집니다.
- 확인 테스트: `TestBloomFilterFalsePositiveRateIsBounded`
- 다시 볼 질문: 예상 item 수와 목표 rate를 bit array 길이와 hash count로 제대로 변환했는가?

### 3. sparse index 경계가 틀려 bounded scan이 깨지는 경우
- 의심 파일: `../internal/sparseindex/sparse_index.go`, `../internal/sstable/sstable.go`
- 깨지는 징후: 잘못된 block range를 고르면 필요한 block을 놓치거나 너무 많이 읽습니다.
- 확인 테스트: `TestSparseIndexFindsExpectedBlock`, `TestSSTableBloomRejectAndBoundedScan`
- 다시 볼 질문: 선택한 block range와 실제 scan byte 수가 `LookupStats`와 일치하는가?
