# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. flush handoff가 잘못돼 최신 값이 사라지는 경우
- 의심 파일: `../src/mini_lsm_store/store.py`
- 깨지는 징후: flush 직후 읽기에서 key가 비거나 이전 값으로 돌아가면 immutable snapshot handoff가 끊긴 것입니다.
- 확인 테스트: `test_flush_creates_sstable`, `test_read_after_force_flush`
- 다시 볼 질문: flush 직전에 snapshot을 떼고, 파일 기록 후에만 목록을 교체하는가?

### 2. read precedence가 뒤집히는 경우
- 의심 파일: `../src/mini_lsm_store/store.py`
- 깨지는 징후: memtable보다 오래된 SSTable을 먼저 읽으면 최신 update가 가려집니다.
- 확인 테스트: `test_memtable_wins_over_sstable`
- 다시 볼 질문: active memtable과 immutable snapshot을 disk보다 항상 먼저 확인하는가?

### 3. tombstone 또는 reopen path가 오래된 value를 되살리는 경우
- 의심 파일: `../src/mini_lsm_store/store.py`, `../src/mini_lsm_store/store.py`
- 깨지는 징후: 삭제 뒤 재오픈에서 예전 live value가 다시 보이면 tombstone masking이나 파일 로드 순서가 틀린 것입니다.
- 확인 테스트: `test_tombstone_across_levels`, `test_persistence_after_reopen`
- 다시 볼 질문: SSTable 목록을 newest-first로 유지하고 재시작 시 같은 순서로 다시 로드하는가?
