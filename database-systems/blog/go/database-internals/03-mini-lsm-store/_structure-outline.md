# Structure Outline

## Chosen arc

1. memtable과 SSTable을 다시 묶는 orchestration 단계라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 cross-level lookup 결과를 먼저 보여 준다.
3. immutable swap, newest-first ordering, tombstone precedence, reopen sequence 복원을 invariant로 정리한다.
4. 마지막에 durability와 compaction이 아직 빠져 있다는 점을 따로 못 박는다.

## Why this structure

- 이 랩은 앞선 두 프로젝트를 묶는 연결점이라, 개별 자료구조보다 lifecycle 설명이 우선이다.
- demo 출력만으로도 tombstone과 overwrite precedence를 보여 줄 수 있어 초반 evidence로 적합하다.
- flush failure rollback 부재는 테스트에 안 나오지만 source-only risk라서 invariant 장에 포함했다.

## Rejected alternatives

- LSM 일반론 위주 설명은 버렸다.
- MemTable과 SSTable 구현 세부를 다시 길게 반복하는 구조도 버렸다.
- production durability를 암시하는 서사는 source-first 원칙에 맞지 않아 제외했다.
