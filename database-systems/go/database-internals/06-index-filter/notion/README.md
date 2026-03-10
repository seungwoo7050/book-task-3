# 학습 노트 안내

logical semantics는 그대로 둔 채 bloom filter와 sparse index를 붙여 point lookup의 읽기 비용을 줄이는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 정확한 negative answer를 보장하면서도 디스크 scan 범위를 줄이려면 filter와 index를 어떤 순서로 적용해야 하는가?
- 다음 단계 `07 Buffer Pool`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/bloomfilter/bloom_filter.go`, `../internal/sparseindex/sparse_index.go`, `../internal/sstable/sstable.go`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `TestBloomFilterHasNoFalseNegatives`, `TestBloomFilterFalsePositiveRateIsBounded`, `TestSparseIndexFindsExpectedBlock`, `TestSSTableBloomRejectAndBoundedScan`입니다.
4. 데모 경로 `../cmd/index-filter/main.go`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 정확한 negative answer를 보장하면서도 디스크 scan 범위를 줄이려면 filter와 index를 어떤 순서로 적용해야 하는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: filter는 빠른 negative check, index는 scan 범위 축소로 역할을 나눈다, lookup 결과에 통계를 포함해 최적화 효과를 보이게 한다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: bloom filter가 false negative를 내는 경우, false positive rate가 비정상적으로 높은 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestBloomFilterHasNoFalseNegatives`, `TestBloomFilterFalsePositiveRateIsBounded`, `TestSparseIndexFindsExpectedBlock`, `TestSSTableBloomRejectAndBoundedScan`
- 데모 경로: `../cmd/index-filter/main.go`
- 데모가 보여 주는 장면: `durian` lookup 결과와 `bytes_read`를 함께 출력합니다.
- 개념 문서: `../docs/concepts/bloom-filter-sizing.md`, `../docs/concepts/sparse-index-scan.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
