# 회고

## 이번 단계에서 명확해진 것
- LSM의 어려움은 자료구조가 아니라 “최신 값을 어느 계층에서 먼저 보느냐”라는 precedence에 있다는 점이 분명해졌습니다.
- flush는 단순 저장이 아니라 읽기 계약을 깨지 않게 handoff하는 작업입니다.
- 재시작 복원까지 들어가면 file ordering과 naming convention도 설계의 일부가 됩니다.

## 아직 단순화한 부분
- 아직 WAL이 없어 flush 전 메모리 상태는 durable하지 않습니다.
- SSTable이 누적되기만 하므로 read amplification과 space amplification이 계속 커집니다.

## 다음에 확장한다면
- WAL을 붙여 crash 후에도 memtable 복원을 보장할 수 있습니다.
- manifest와 compaction을 추가하면 실제 mini storage engine에 더 가까워집니다.

## `02 WAL Recovery`로 넘길 질문
- flush 전에 어떤 로그를 남겨야 crash 이후 memtable을 되살릴 수 있는가?
- 겹치는 SSTable이 많아졌을 때 compaction은 어떤 단위로 일어나야 하는가?
