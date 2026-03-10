# 지식 인덱스

## 핵심 용어
- `bloom filter`: 존재하지 않는 key를 빠르게 거르기 위한 확률적 집합 구조입니다.
- `false positive`: 실제로 없는데 있을 수도 있다고 답하는 경우입니다.
- `false negative`: 실제로 있는데 없다고 답하는 경우로, bloom filter에서는 허용되지 않습니다.
- `sparse index`: 일부 key만 잡아 대략적인 data block 위치를 찾는 인덱스입니다.
- `lookup stats`: 최적화가 실제로 얼마만큼 읽기를 줄였는지 보여 주는 보조 정보입니다.

## 다시 볼 파일
- `../internal/bloomfilter/bloom_filter.go`: filter 계산과 lookup 통계를 확인할 수 있는 핵심 파일입니다. 특히 MurmurHash3 두 개로 double hashing을 만든 bloom filter 구현입니다.
- `../internal/sparseindex/sparse_index.go`: 희소 인덱스가 어느 block을 읽을지 결정하는 부분을 볼 수 있습니다.
- `../internal/sstable/sstable.go`: filter, sparse index, 실제 block scan이 하나의 lookup path에서 만나는 지점을 확인할 수 있습니다.
- `../tests/index_filter_test.go`: false negative 금지, false positive bound, bounded scan을 검증합니다.

## 개념 문서
- `../docs/concepts/bloom-filter-sizing.md`: false positive rate와 bit budget의 trade-off를 정리합니다.
- `../docs/concepts/sparse-index-scan.md`: 희소 인덱스가 디스크 scan 범위를 어떻게 줄이는지 설명합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/index_filter_test.go`
- 다시 돌릴 테스트 이름: `TestBloomFilterHasNoFalseNegatives`, `TestBloomFilterFalsePositiveRateIsBounded`, `TestSparseIndexFindsExpectedBlock`, `TestSSTableBloomRejectAndBoundedScan`
- 데모 경로: `../cmd/index-filter/main.go`
- 데모가 보여 주는 장면: `durian` lookup 결과와 `bytes_read`를 함께 출력합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
