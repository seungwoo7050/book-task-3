# 지식 인덱스

## 핵심 용어
- `MVCC`: 여러 version을 유지해 concurrent transaction이 서로 다른 snapshot을 읽게 하는 기법입니다.
- `version chain`: 한 key에 대해 tx_id 기준으로 정렬된 version 목록입니다.
- `snapshot isolation`: transaction 시작 시점의 committed state만 읽는 규칙입니다.
- `first-committer-wins`: 같은 key를 두 transaction이 쓸 때 먼저 commit한 쪽만 성공시키는 규칙입니다.
- `GC`: 어떤 active snapshot에서도 더 이상 필요 없는 오래된 version을 제거하는 작업입니다.

## 재현 순서용 파일 맵
- `../src/mvcc_lab/core.py`: 구현 전체가 있는 중심 파일입니다.
- `../tests/test_mvcc.py`: 규칙별 시나리오가 정리된 테스트 파일입니다.
- `../src/mvcc_lab/__main__.py`: 가장 짧은 데모 진입점입니다.
- `../docs/concepts/snapshot-visibility.md`: 읽기 규칙을 먼저 정리할 때 좋습니다.

## 바로 실행할 명령
```bash
cd python/database-internals/05-mvcc
source .venv/bin/activate
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_snapshot_isolation -v
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_write_write_conflict -v
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_gc -v
PYTHONPATH=src python -m mvcc_lab
```

## 기대 결과
### 데모 출력
```text
{'tx': 1, 'read_your_own_write': 10}
```

### 테스트가 확인하는 대표 사실
- `test_snapshot_isolation`: `t2`는 `x=100`을 읽어야 함
- `test_write_write_conflict`: 두 번째 commit은 예외를 던져야 함
- `test_gc`: 최신 읽기 결과는 유지하면서 version chain 길이가 줄어야 함

## 개념 문서
- `../docs/concepts/snapshot-visibility.md`: visible version 선택 규칙
- `../docs/concepts/write-conflict.md`: first-committer-wins 충돌 규칙

## 다음 단계 연결
- 이 트랙은 여기서 끝나지만, 다음 확장 주제는 “이 version chain을 실제 저장 계층과 분산 복제 위에 어떻게 올릴 것인가”입니다.
- 현재 프로젝트가 고정한 핵심은 “가시성 규칙이 먼저고, 저장 매체는 그 다음”이라는 점입니다.

## 검증 앵커
- 확인일: 2026-03-10
- 테스트 파일: `../tests/test_mvcc.py`
- 다시 돌릴 테스트 이름: `test_basic_read_write`, `test_snapshot_isolation`, `test_latest_committed_value`, `test_write_write_conflict`, `test_different_keys_no_conflict`, `test_abort_and_delete`, `test_gc`

- 더 긴 이전 기록은 `../notion-archive/`에 남겨 두고, 여기에는 다시 구현할 때 바로 필요한 정보만 남깁니다.
