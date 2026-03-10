# 문제 프레이밍

## 왜 이 프로젝트를 하는가
정렬된 memtable 출력을 immutable SSTable 파일로 굳히며, index와 footer를 이용한 point lookup 계약을 만드는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Go
- 이전 단계: 01 MemTable SkipList
- 다음 단계: 03 Mini LSM Store
- 지금 답하려는 질문: 정렬된 key/value 집합을 디스크에 저장하면서 빠른 lookup과 전체 재검토용 scan을 함께 제공하려면 어떤 파일 배치가 필요한가?

## 이번 구현에서 성공으로 보는 것
- 정렬된 entries를 SSTable 파일로 쓰고 다시 읽었을 때 key 순서와 tombstone이 그대로 유지되어야 합니다.
- `Lookup`이 missing key, live value, tombstone을 올바르게 구분해야 합니다.
- `ReadAll`이 디버깅과 검증용으로 전체 내용을 순서대로 복원해야 합니다.
- footer가 index 시작 offset을 정확히 가리켜야 합니다.
- 손상된 footer나 잘못된 offset을 안전하게 거부해야 합니다.

## 먼저 열어 둘 파일
- `../internal/sstable/sstable.go`: `SSTable`, `IndexEntry`, footer 처리와 `Lookup` 구현이 모여 있습니다.
- `../tests/sstable_test.go`: round-trip, tombstone, large dataset, malformed footer를 직접 검증합니다.
- `../cmd/sstable-format/main.go`: `alpha`, `beta`, `gamma`를 파일로 쓴 뒤 lookup 결과를 출력합니다.
- `../docs/concepts/sstable-layout.md`: data 영역, index, footer의 배치를 먼저 이해할 때 도움이 됩니다.

## 의도적으로 남겨 둔 범위 밖 항목
- block compression, checksum, sparse index, bloom filter는 아직 포함하지 않습니다.
- multi-level manifest와 compaction metadata는 다음 단계로 넘깁니다.

## 데모에서 바로 확인할 장면
- 몇 개의 sample entry를 파일로 쓴 뒤 `alpha`, `beta`, `gamma` lookup을 출력해 live value, missing, tombstone을 함께 보여 줍니다.
