# 학습 노트 안내

flush 이전의 memtable 상태를 WAL에 먼저 기록하고, crash 이후 replay로 복원하는 durability 기본기를 익히는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 메모리 상태가 사라진 뒤에도 마지막 정상 record까지 재구성하려면 WAL은 어떤 순서와 어떤 검증 규칙을 가져야 하는가?
- 다음 단계 `03 Index Filter`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../src/wal_recovery/store.py`, `../src/wal_recovery/store.py`, `../tests/test_wal_recovery.py`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `test_recover_put_records`, `test_recover_delete_records`, `test_recover_many_records`, `test_stop_at_corrupted_record`입니다.
4. 데모 경로 `../src/wal_recovery/__main__.py`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 메모리 상태가 사라진 뒤에도 마지막 정상 record까지 재구성하려면 WAL은 어떤 순서와 어떤 검증 규칙을 가져야 하는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: append-ahead 규칙을 먼저 세운다, checksum이 어긋나는 지점에서 replay를 멈춘다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: 손상된 trailing record를 끝까지 읽는 경우, delete replay가 live value 삭제와 tombstone 기록을 혼동하는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `test_recover_put_records`, `test_recover_delete_records`, `test_recover_many_records`, `test_stop_at_corrupted_record`
- 데모 경로: `../src/wal_recovery/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 `name`, `city`를 쓴 뒤 store를 닫고 다시 열어 복원된 값을 출력합니다. Python 데모도 같은 복구 장면을 JSON 형태로 보여 줍니다.
- 개념 문서: `../docs/concepts/recovery-policy.md`, `../docs/concepts/wal-record-format.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
