# 지식 인덱스

## 핵심 용어
- `active memtable`: 현재 write가 바로 반영되는 mutable in-memory 상태입니다.
- `immutable snapshot`: flush 중 읽기 일관성을 위해 잠시 얼려 둔 memtable 복사본입니다.
- `read precedence`: 여러 계층 중 어디를 먼저 읽을지 정한 우선순위 규칙입니다.
- `flush`: in-memory state를 immutable on-disk SSTable로 굳히는 작업입니다.
- `reopen persistence`: 프로세스를 다시 시작해도 기존 SSTable에서 상태를 복원하는 성질입니다.

## 다시 볼 파일
- `../src/mini_lsm_store/store.py`: memtable handoff, flush, reopen 로직이 한곳에서 어떻게 이어지는지 다시 확인합니다.
- `../src/mini_lsm_store/__main__.py`: flush 뒤 lookup 결과를 가장 짧게 확인하는 데모 진입점입니다.
- `../tests/test_mini_lsm_store.py`: flush, read precedence, tombstone masking, reopen persistence를 검증합니다.
- `../docs/concepts/flush-lifecycle.md`: active memtable이 immutable snapshot을 거쳐 SSTable로 굳는 과정을 먼저 복기할 때 좋습니다.

## 개념 문서
- `../docs/concepts/flush-lifecycle.md`: active memtable이 immutable snapshot을 거쳐 SSTable로 굳는 과정을 정리합니다.
- `../docs/concepts/read-path.md`: 여러 저장 계층에서 최신 값을 찾는 우선순위를 설명합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/test_mini_lsm_store.py`
- 다시 돌릴 테스트 이름: `test_put_and_get`, `test_missing_key`, `test_update`, `test_delete`, `test_flush_creates_sstable`, `test_read_after_force_flush`, `test_memtable_wins_over_sstable`, `test_tombstone_across_levels`, `test_persistence_after_reopen`
- 데모 경로: `../src/mini_lsm_store/__main__.py`
- 데모가 보여 주는 장면: JSON lines SSTable로 flush한 뒤 `alpha` 조회와 SSTable 개수를 함께 출력합니다.
- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 필요한 정보만 남깁니다.
