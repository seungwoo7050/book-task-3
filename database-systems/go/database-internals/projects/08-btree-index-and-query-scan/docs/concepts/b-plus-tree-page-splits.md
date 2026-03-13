# B+Tree Page Splits

이 프로젝트는 `07-buffer-pool`에서 본 "고정 크기 page를 안정적으로 나누고 다시 찾는 감각"을 index 쪽으로 옮긴다. 실제 disk pager와 latch는 아직 넣지 않지만, split 규칙만큼은 page-oriented 설계를 그대로 따른다.

## 핵심 요점

- leaf는 정렬된 `(key -> row ids)` 엔트리를 가진다.
- leaf가 꽉 차면 절반을 새 sibling leaf로 옮기고, 오른쪽 leaf의 첫 key를 부모에 올린다.
- internal node는 child pointer 사이 경계 key만 저장한다.
- range scan은 linked leaf를 따라가며 key order를 유지한다.

## 이 프로젝트에서 일부러 생략한 것

- delete 후 merge / redistribution
- variable-length page packing
- buffer pool pin / unpin과의 직접 결합
- concurrent latch coupling

지금 단계의 목표는 "split이 lookup과 range scan의 shape를 어떻게 바꾸는가"를 먼저 손으로 잡는 것이다.
