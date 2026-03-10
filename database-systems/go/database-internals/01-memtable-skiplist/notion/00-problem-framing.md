# 문제 프레이밍

## 왜 이 프로젝트를 하는가
LSM write path의 출발점인 active memtable을 독립된 SkipList로 구현해, 정렬된 삽입과 tombstone semantics를 먼저 고정하는 단계입니다.

## 커리큘럼 안에서의 위치
- 트랙: Database Internals / Go
- 이전 단계: 없음
- 다음 단계: 02 SSTable Format
- 지금 답하려는 질문: 정렬된 삽입 구조 안에서 갱신, tombstone, 대략적 byte size를 동시에 유지하려면 어떤 상태 표현이 필요한가?

## 이번 구현에서 성공으로 보는 것
- `Put(key, value)`가 새 key 삽입과 기존 key 갱신을 모두 처리하면서 key 오름차순을 유지해야 합니다.
- `Get(key)`가 live value, tombstone, 미존재를 구분해야 합니다.
- `Delete(key)`가 physical remove가 아니라 tombstone 기록으로 남아야 합니다.
- `Entries()`가 tombstone을 포함한 전체 상태를 정렬 순서대로 내놓아야 합니다.
- `ByteSize()`가 flush threshold 판단에 쓸 수 있을 만큼 일관되게 갱신되어야 합니다.

## 먼저 열어 둘 파일
- `../internal/skiplist/skiplist.go`: `SkipList`, `Entry`, `ValueState`가 모여 있는 핵심 구현입니다.
- `../tests/skiplist_test.go`: 정렬 순서, tombstone 유지, byte size 추적이 어디서 깨지는지 바로 확인할 수 있는 검증 앵커입니다.
- `../cmd/skiplist-demo/main.go`: `banana` 삭제 후 ordered entries와 `size`/`byteSize`를 함께 출력하는 데모입니다.
- `../docs/concepts/skiplist-invariants.md`: 탐색과 순회에서 어떤 invariant를 지켜야 하는지 정리한 개념 메모입니다.

## 의도적으로 남겨 둔 범위 밖 항목
- 동시성 제어와 lock-free skip list는 다루지 않습니다.
- range seek, prefix iterator, probabilistic tuning은 다음 확장 과제로 남깁니다.

## 데모에서 바로 확인할 장면
- `banana`, `apple`, `carrot`를 넣고 `banana`를 tombstone으로 바꾼 뒤 ordered entries와 `size`/`byteSize`를 같이 출력합니다.
