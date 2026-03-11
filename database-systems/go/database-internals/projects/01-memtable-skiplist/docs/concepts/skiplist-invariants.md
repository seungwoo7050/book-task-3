# SkipList Invariants

## 핵심 invariant

- level 0 연결 리스트는 전체 키 집합을 오름차순으로 포함한다.
- 상위 level은 level 0의 부분집합 shortcut이다.
- 어떤 키를 tombstone으로 바꿔도 key ordering은 깨지지 않는다.

## 학습 포인트

- 이 프로젝트의 목적은 "확률적 밸런싱 자료구조를 구현한다" 자체보다 flush 전에 필요한 ordered MemTable semantics를 고정하는 데 있다.
- tombstone을 유지해야 이후 SSTable flush, compaction, recovery가 같은 삭제 의미를 공유할 수 있다.
- byte-size accounting은 정확한 allocator accounting이 아니라 flush threshold 의사결정을 위한 근사치면 충분하다.

