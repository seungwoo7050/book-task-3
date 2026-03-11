# 문제 프레이밍

## 왜 이 프로젝트를 하는가
memtable, immutable snapshot, SSTable을 한 프로젝트 안에서 묶어 최소 LSM read/write path가 어떻게 이어지는지 확인하는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Python
- 이전 단계: 없음
- 다음 단계: 02 WAL Recovery
- 지금 답하려는 질문: 최근 write와 delete가 여러 저장 계층에 흩어져 있을 때, 어떤 우선순위로 읽어야 최신 논리 상태를 얻을 수 있는가?

## 이번 구현에서 성공으로 보는 것
- `put`, `get`, `delete`가 기본 key-value semantics를 유지해야 합니다.
- flush가 발생하면 active memtable 내용이 새 SSTable로 굳어야 합니다.
- read path가 active memtable, immutable snapshot, SSTable 사이에서 최신 값을 우선해야 합니다.
- tombstone이 오래된 live value를 정확히 가려야 합니다.
- 재시작 후에도 기존 SSTable을 다시 읽어 상태를 복원할 수 있어야 합니다.

## 먼저 열어 둘 파일
- `../src/mini_lsm_store/store.py`: active memtable, immutable snapshot, SSTable 목록, reopen 경로가 한 파일 안에서 어떻게 맞물리는지 확인합니다.
- `../src/mini_lsm_store/__main__.py`: flush 이후 lookup과 SSTable 개수를 가장 짧게 보여 주는 데모 진입점입니다.
- `../tests/test_mini_lsm_store.py`: flush, read precedence, tombstone masking, reopen persistence가 어디서 깨지는지 바로 확인합니다.
- `../docs/concepts/read-path.md`: 여러 계층을 어떤 우선순위로 읽어야 하는지 먼저 맞출 때 도움이 됩니다.

## 의도적으로 남겨 둔 범위 밖 항목
- WAL 없이 메모리 flush만으로 durability를 해결하려 하지는 않습니다.
- background compaction과 manifest 관리도 아직 포함하지 않습니다.

## 데모에서 바로 확인할 장면
- JSON lines SSTable로 flush한 뒤 `alpha` 조회와 SSTable 개수를 함께 출력합니다.
