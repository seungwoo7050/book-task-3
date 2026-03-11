# 문제 프레이밍

## 왜 이 프로젝트를 하는가
logical semantics는 그대로 둔 채 bloom filter와 sparse index를 붙여 point lookup의 읽기 비용을 줄이는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Python
- 이전 단계: 02 WAL Recovery
- 다음 단계: 04 Buffer Pool
- 지금 답하려는 질문: 정확한 negative answer를 보장하면서도 디스크 scan 범위를 줄이려면 filter와 index를 어떤 순서로 적용해야 하는가?

## 이번 구현에서 성공으로 보는 것
- bloom filter가 false negative를 내지 않아야 합니다.
- false positive rate가 테스트에서 허용한 범위를 넘지 않아야 합니다.
- sparse index가 key가 있을 법한 block 범위를 좁혀 주어야 합니다.
- `GetWithStats` 또는 동등한 API가 실제 `bytes_read`와 `bloom_rejected` 정보를 보여 주어야 합니다.
- tombstone이 섞여 있어도 lookup semantics가 바뀌지 않아야 합니다.

## 먼저 열어 둘 파일
- `../src/index_filter/table.py`: bloom filter, sparse index, block scan이 하나의 lookup path에서 어떻게 만나는지 확인합니다.
- `../src/index_filter/__main__.py`: `durian` lookup과 `bytes_read`를 가장 짧게 보여 주는 데모 진입점입니다.
- `../tests/test_index_filter.py`: false negative 금지, false positive bound, bounded scan이 어디서 깨지는지 바로 확인합니다.
- `../docs/concepts/sparse-index-scan.md`: 희소 인덱스가 실제 scan 범위를 어떻게 줄이는지 먼저 복기합니다.

## 의도적으로 남겨 둔 범위 밖 항목
- adaptive filter sizing, block cache, prefix bloom 같은 production 최적화는 포함하지 않습니다.
- range scan 최적화나 compression은 다른 단계로 남깁니다.

## 데모에서 바로 확인할 장면
- `durian` lookup 결과와 `bytes_read`를 dict 형태로 출력해 filter가 실제로 scan을 줄였는지 보여 줍니다.
