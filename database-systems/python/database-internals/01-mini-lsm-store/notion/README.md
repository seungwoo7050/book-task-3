# 학습 노트 안내

memtable, immutable snapshot, SSTable을 한 프로젝트 안에서 묶어 최소 LSM read/write path가 어떻게 이어지는지 확인하는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 최근 write와 delete가 여러 저장 계층에 흩어져 있을 때, 어떤 우선순위로 읽어야 최신 논리 상태를 얻을 수 있는가?
- 다음 단계 `02 WAL Recovery`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../src/mini_lsm_store/store.py`, `../src/mini_lsm_store/store.py`, `../src/mini_lsm_store/store.py`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `test_put_and_get`, `test_missing_key`, `test_update`, `test_delete`입니다.
4. 데모 경로 `../src/mini_lsm_store/__main__.py`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 최근 write와 delete가 여러 저장 계층에 흩어져 있을 때, 어떤 우선순위로 읽어야 최신 논리 상태를 얻을 수 있는가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: 읽기 우선순위를 메모리에서 디스크 순으로 고정한다, flush 동안 immutable snapshot을 분리한다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: flush handoff가 잘못돼 최신 값이 사라지는 경우, read precedence가 뒤집히는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `test_put_and_get`, `test_missing_key`, `test_update`, `test_delete`
- 데모 경로: `../src/mini_lsm_store/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 `banana`를 갱신하고 `apple`을 tombstone으로 만든 뒤 lookup 결과를 출력합니다. Python 데모는 JSON lines SSTable로 flush한 뒤 `alpha` 조회와 SSTable 개수를 함께 출력합니다.
- 개념 문서: `../docs/concepts/flush-lifecycle.md`, `../docs/concepts/read-path.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
