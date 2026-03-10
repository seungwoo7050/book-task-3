# 지식 인덱스

## 핵심 용어
- `active memtable`: 현재 write가 바로 반영되는 mutable in-memory 상태입니다.
- `immutable snapshot`: flush 중 읽기 일관성을 위해 잠시 얼려 둔 memtable 복사본입니다.
- `read precedence`: 여러 계층 중 어디를 먼저 읽을지 정한 우선순위 규칙입니다.
- `flush`: in-memory state를 immutable on-disk SSTable로 굳히는 작업입니다.
- `reopen persistence`: 프로세스를 다시 시작해도 기존 SSTable에서 상태를 복원하는 성질입니다.

## 다시 볼 파일
- `../internal/lsmstore/store.go`: `LSMStore` 또는 `MiniLSMStore`가 memtable, immutable snapshot, SSTable 목록을 엮는 중심 파일입니다.
- `../internal/skiplist/skiplist.go`: active memtable 표현과 flush 직전 정렬 계약을 확인할 수 있습니다.
- `../internal/sstable/sstable.go`: flush 결과를 어떤 형식으로 저장하고 다시 읽는지 확인할 수 있습니다.
- `../tests/lsm_store_test.go`: flush, read precedence, tombstone masking, reopen persistence를 검증합니다.

## 개념 문서
- `../docs/concepts/flush-lifecycle.md`: active memtable이 immutable snapshot을 거쳐 SSTable로 굳는 과정을 정리합니다.
- `../docs/concepts/read-path.md`: 여러 저장 계층에서 최신 값을 찾는 우선순위를 설명합니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/lsm_store_test.go`
- 다시 돌릴 테스트 이름: `TestPutAndGet`, `TestMissingKey`, `TestUpdate`, `TestDelete`, `TestFlushCreatesSSTable`, `TestReadAfterForceFlush`, `TestMemtableWinsOverSSTable`, `TestTombstoneAcrossLevels`, `TestPersistenceAfterReopen`
- 데모 경로: `../cmd/mini-lsm-store/main.go`
- 데모가 보여 주는 장면: flush 후 `banana` 갱신과 `apple` 삭제가 어떤 precedence로 보이는지 출력합니다.

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 쓸 정보만 남깁니다.
