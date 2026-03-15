# Structure Outline

## Chosen arc

1. scheduler가 아니라 merge semantics와 manifest atomicity가 중심이라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 overwrite precedence와 tombstone drop 조건을 먼저 보여 준다.
3. newest-first merge, conditional tombstone drop, manifest write 순서를 invariant로 정리한다.
4. 마지막에 multi-level balancing과 rollback 부재를 별도 boundary로 분리한다.

## Why this structure

- 이 랩은 compaction을 설명하면서도 metadata atomicity를 같이 다뤄야 해서, merge와 manifest를 같은 축에 두는 편이 맞다.
- tombstone drop은 deepest 여부에 따라 달라지므로 demo만으로는 부족했고, 추가 관찰값을 early evidence로 포함했다.
- in-memory level mutation이 manifest write보다 먼저 일어나는 점은 source-only nuance라 invariant 장에서 분명히 적는 편이 좋다.

## Rejected alternatives

- compaction 일반론을 길게 설명하는 구조는 버렸다.
- 테스트 요약만 나열하는 구조도 버렸다.
- scheduler나 benchmark 얘기를 상상으로 확장하는 서사는 현재 범위를 벗어나 제외했다.
