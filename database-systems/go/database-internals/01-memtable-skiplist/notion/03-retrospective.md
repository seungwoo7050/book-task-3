# 회고

## 이번 단계에서 명확해진 것
- 정렬된 in-memory write path가 먼저 안정돼야 그 위에 SSTable과 flush를 얹을 수 있다는 점이 분명해졌습니다.
- element 수가 아니라 byte size를 추적해야 다음 단계 threshold 기반 flush가 자연스럽습니다.
- tombstone은 삭제의 부수 효과가 아니라 이후 단계 전체가 공유하는 계약이라는 점을 확인했습니다.

## 아직 단순화한 부분
- 단일 스레드 구현이라 concurrent writer 상황은 설명하지 못합니다.
- seek, range scan, iterator invalidation 같은 고급 탐색 API는 아직 없습니다.

## 다음에 확장한다면
- range iterator와 seek API를 넣어 read path 학습으로 자연스럽게 연결할 수 있습니다.
- 동시성 제어를 붙이거나 lock-free 대안을 비교하면 자료구조 선택의 폭이 넓어집니다.

## `02 SSTable Format`로 넘길 질문
- 이 정렬 순서를 파일 포맷으로 내보낼 때 footer와 index는 어디에 둘 것인가?
- missing과 tombstone을 on-disk lookup에서 어떻게 구분할 것인가?
