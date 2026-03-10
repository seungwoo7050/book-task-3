# 지식 인덱스

## 핵심 용어
- `bloom filter`: 존재하지 않는 key를 빠르게 거르기 위한 확률적 집합 구조입니다.
- `false positive`: 실제로 없는데 있을 수도 있다고 답하는 경우입니다.
- `false negative`: 실제로 있는데 없다고 답하는 경우로, bloom filter에서는 허용되지 않습니다.
- `sparse index`: 일부 key만 잡아 대략적인 data block 위치를 찾는 인덱스입니다.
- `lookup stats`: 최적화가 실제로 얼마만큼 읽기를 줄였는지 보여 주는 보조 정보입니다.

## 다시 볼 파일
- `../src/index_filter/table.py`: filter 계산과 lookup 통계를 확인할 수 있는 핵심 파일입니다. 특히 MurmurHash 기반 비트 위치 계산과 JSON block decode를 함께 다루는 구현입니다.
- `../src/index_filter/table.py`: 희소 인덱스가 어느 block을 읽을지 결정하는 부분을 볼 수 있습니다.
- `../src/index_filter/table.py`: filter, sparse index, 실제 block scan이 하나의 lookup path에서 만나는 지점을 확인할 수 있습니다.
- `../tests/test_index_filter.py`: false negative 금지, false positive bound, bounded scan을 검증합니다.

## 개념 문서
- `../docs/concepts/bloom-filter-sizing.md`: false positive rate와 bit budget의 trade-off를 정리합니다.
- `../docs/concepts/sparse-index-scan.md`: 희소 인덱스가 디스크 scan 범위를 어떻게 줄이는지 설명합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/test_index_filter.py`
- 다시 돌릴 테스트 이름: `test_bloom_filter_has_no_false_negatives`, `test_bloom_filter_false_positive_rate_is_bounded`, `test_sparse_index_finds_expected_block`, `test_sstable_bloom_reject_and_bounded_scan`
- 데모 경로: `../src/index_filter/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 `durian` lookup 결과와 `bytes_read`를 같이 출력합니다. Python 데모도 동일한 정보를 dict 형태로 출력해 filter가 실제로 scan을 줄였는지 보여 줍니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
