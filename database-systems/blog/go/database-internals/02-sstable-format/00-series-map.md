# 02 SSTable Format

## 이 랩의 실제 질문

이 프로젝트는 "파일에 record를 저장한다"는 수준보다 훨씬 구체적인 질문을 다룬다. 정렬된 record stream을 immutable on-disk format으로 어떻게 고정할 것인가, point lookup이 전체 파일 scan 없이도 key 위치를 찾게 하려면 어떤 index와 footer가 필요한가, tombstone을 메모리 밖으로 내보낼 때 어떤 sentinel로 보존할 것인가가 핵심이다.

즉 이 랩은 flush orchestration보다 포맷 자체를 따로 떼어 읽게 만든다. 데이터 영역, index 영역, footer, reopen 시 index load, tombstone lookup까지가 이 프로젝트의 정확한 범위다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/problem/README.md), [`sstable.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/internal/sstable/sstable.go), [`serializer.go`](/Users/woopinbell/work/book-task-3/database-systems/go/shared/serializer/serializer.go), [`fileio.go`](/Users/woopinbell/work/book-task-3/database-systems/go/shared/fileio/fileio.go), [`sstable_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/02-sstable-format/tests/sstable_test.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- immutable file layout은 어떤 section들로 구성되는가
- sparse index와 footer는 lookup 시작 위치를 어떻게 줄여 주는가
- tombstone은 어떤 sentinel로 디스크에 남는가
- malformed footer나 truncated record는 어디서 에러로 다뤄지는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/02-sstable-format/10-chronology-scope-and-surface.md): 문제 범위, file layout, demo lookup surface를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/02-sstable-format/20-chronology-core-invariants.md): sorted write, footer sizing, tombstone sentinel, reopen path를 소스 기준으로 설명한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/02-sstable-format/30-chronology-verification-and-boundaries.md): go test와 demo 재실행을 바탕으로 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/02-sstable-format/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/02-sstable-format/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 immutable SSTable의 최소 포맷을 Go로 고정한다. compression, block cache, manifest, compaction은 아직 없다. 대신 sorted data section, serialized index, 8-byte footer, tombstone sentinel, reopen-safe lookup path는 명확히 드러난다.
