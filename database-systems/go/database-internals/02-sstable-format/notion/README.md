# 학습 노트 안내

정렬된 memtable 출력을 immutable SSTable 파일로 굳히며, index와 footer를 이용한 point lookup 계약을 만드는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 정렬된 key/value 집합을 디스크에 저장하면서 빠른 lookup과 전체 재검토용 scan을 함께 제공하려면 어떤 파일 배치가 필요한가?
- 다음 단계 `03 Mini LSM Store`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../internal/sstable/sstable.go`, `../tests/sstable_test.go`, `../cmd/sstable-format/main.go`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `TestRoundTripSortedEntries`, `TestMissingKey`, `TestTombstones`, `TestReadAll`입니다.
4. 데모 경로 `../cmd/sstable-format/main.go`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 정렬된 key/value 집합을 디스크에 저장하면서 빠른 lookup과 전체 재검토용 scan을 함께 제공하려면 어떤 파일 배치가 필요한가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: footer에서 index 시작점을 거꾸로 찾는다, index는 한 번 읽어 메모리에 올리고 lookup은 그 위에서 시작한다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: footer offset 계산이 틀리는 경우, missing key와 tombstone을 같은 상태로 다루는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `TestRoundTripSortedEntries`, `TestMissingKey`, `TestTombstones`, `TestReadAll`
- 데모 경로: `../cmd/sstable-format/main.go`
- 데모가 보여 주는 장면: 몇 개의 sample entry를 파일로 쓴 뒤 `alpha`, `beta`, `gamma` lookup을 출력해 live value, missing, tombstone을 함께 보여 줍니다.
- 개념 문서: `../docs/concepts/lookup-path.md`, `../docs/concepts/sstable-layout.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
