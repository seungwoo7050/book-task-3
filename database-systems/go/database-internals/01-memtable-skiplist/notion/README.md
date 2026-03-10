# 학습 노트 안내

LSM write path의 출발점인 active memtable을 독립된 SkipList로 구현해, 정렬된 삽입과 tombstone semantics를 먼저 고정하는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 정렬된 삽입 구조 안에서 갱신, tombstone, 대략적 byte size를 동시에 유지하려면 어떤 상태 표현이 필요한가?
- 다음 단계 `02 SSTable Format`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/skiplist/skiplist.go`, `../tests/skiplist_test.go`, `../cmd/skiplist-demo/main.go`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `TestPutAndGet`, `TestMissingKey`, `TestUpdateKeepsLogicalSize`, `TestManyInserts`입니다.
4. 데모 경로 `../cmd/skiplist-demo/main.go`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 정렬된 삽입 구조 안에서 갱신, tombstone, 대략적 byte size를 동시에 유지하려면 어떤 상태 표현이 필요한가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: 값 상태를 분리해 tombstone을 명시한다, 학습용 테스트를 위해 level 선택을 결정적으로 만든다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: overwrite에서 byte size가 이중 집계되는 경우, delete가 physical remove로 처리되는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestPutAndGet`, `TestMissingKey`, `TestUpdateKeepsLogicalSize`, `TestManyInserts`
- 데모 경로: `../cmd/skiplist-demo/main.go`
- 데모가 보여 주는 장면: `banana`, `apple`, `carrot`를 넣고 `banana`를 tombstone으로 바꾼 뒤 ordered entries와 `size`/`byteSize`를 같이 출력합니다.
- 개념 문서: `../docs/concepts/skiplist-invariants.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
