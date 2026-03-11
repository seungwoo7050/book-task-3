# 지식 인덱스

## 핵심 용어
- `MVCC`: 여러 version을 유지해 concurrent transaction이 서로 다른 snapshot을 읽게 하는 기법입니다.
- `version chain`: 한 key에 대해 tx_id 기준으로 정렬된 version 목록입니다.
- `snapshot isolation`: transaction 시작 시점의 committed state만 읽는 규칙입니다.
- `first-committer-wins`: 같은 key를 두 transaction이 쓸 때 먼저 commit한 쪽만 성공시키는 규칙입니다.
- `GC`: 어떤 active snapshot에서도 더 이상 필요 없는 오래된 version을 제거하는 작업입니다.

## 다시 볼 파일
- `../src/mvcc_lab/core.py`: version chain, visibility, conflict detection, abort cleanup, GC가 한 파일 안에서 이어집니다.
- `../src/mvcc_lab/__main__.py`: read-your-own-write 데모를 가장 짧게 확인하는 진입점입니다.
- `../tests/test_mvcc.py`: snapshot isolation, write-write conflict, abort, GC 시나리오를 검증합니다.
- `../docs/concepts/snapshot-visibility.md`: visible version 선택 규칙을 먼저 복기할 때 좋습니다.

## 개념 문서
- `../docs/concepts/snapshot-visibility.md`: visible version 선택 규칙을 설명합니다.
- `../docs/concepts/write-conflict.md`: first-committer-wins 충돌 규칙을 정리합니다.

## 검증 앵커
- 확인일: 2026-03-11
- 테스트 파일: `../tests/test_mvcc.py`
- 다시 돌릴 테스트 이름: `test_basic_read_write`, `test_snapshot_isolation`, `test_latest_committed_value`, `test_write_write_conflict`, `test_different_keys_no_conflict`, `test_abort_and_delete`, `test_gc`
- 데모 경로: `../src/mvcc_lab/__main__.py`
- 데모가 보여 주는 장면: `{'tx': 1, 'read_your_own_write': 10}` 한 줄로 read-your-own-write 경로를 확인할 수 있습니다.
- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 읽을 때 바로 필요한 정보만 남깁니다.
