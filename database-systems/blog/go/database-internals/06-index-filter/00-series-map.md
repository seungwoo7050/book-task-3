# 06 Index Filter

## 이 랩의 실제 초점

이 프로젝트는 SSTable lookup을 더 빠르게 만든다고 하지만, 핵심은 "왜 전체 파일을 다 읽지 않아도 되는가"를 source-first로 드러내는 데 있다. Bloom filter는 miss를 즉시 잘라내고, sparse index는 target key가 있을 법한 block 범위를 좁혀 준다. footer는 Bloom과 index의 위치를 reopen 시점에 다시 복원하게 해 준다.

즉 이 랩은 읽기 최적화 일반론보다, negative lookup을 0-byte read로 끝내는 경로와 positive lookup을 bounded block scan으로 제한하는 경로를 분리해서 보여 준다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/problem/README.md), [`sstable.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/sstable/sstable.go), [`bloom_filter.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/bloomfilter/bloom_filter.go), [`sparse_index.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/internal/sparseindex/sparse_index.go), [`index_filter_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/06-index-filter/tests/index_filter_test.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- Bloom filter는 miss 경로를 어디서 자르는가
- sparse index는 어떤 block만 읽게 만드는가
- footer는 filter/index 위치를 어떤 메타데이터로 기록하는가
- false positive는 허용하되 false negative는 어떻게 막는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/06-index-filter/10-chronology-scope-and-surface.md): 문제 범위, open/lookup 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/06-index-filter/20-chronology-core-invariants.md): Bloom sizing, Murmur double hashing, sparse block boundary, footer magic/offset layout를 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/06-index-filter/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 바탕으로 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/06-index-filter/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/06-index-filter/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 읽기 최적화를 "Bloom filter 하나 붙였다" 수준이 아니라, miss-fast path와 bounded positive scan path를 별도로 설명하는 단계다. learned index, adaptive filter, cache 연동은 아직 없다. 대신 footer-backed reopen, Bloom reject, sparse block scan은 분명하게 드러난다.
