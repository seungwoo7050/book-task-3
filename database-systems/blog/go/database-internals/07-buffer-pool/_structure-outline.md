# Structure Outline

## Chosen arc

1. cache optimization보다 page lifecycle manager라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 첫 page fetch, dirty flush, pinned eviction failure를 먼저 보여 준다.
3. page identity, pin count, dirty signaling, pinned eviction policy를 invariant로 정리한다.
4. 마지막에는 동시성/async IO가 아직 없다는 점을 따로 분리한다.

## Why this structure

- 이 랩은 LRU보다 page metadata가 더 중요해서, replacer 일반론보다 pin/dirty 충돌을 앞세우는 편이 맞다.
- demo가 너무 짧기 때문에 dirty flush와 pinned eviction failure를 추가 관찰값으로 보강했다.
- source-only nuance인 "다른 victim을 찾지 않고 바로 실패"를 명확히 적어야 현재 구현 경계가 선명해진다.

## Rejected alternatives

- buffer pool 일반론을 길게 푸는 구조는 버렸다.
- LRU cache 테스트만 중심에 두는 구조도 버렸다.
- lock manager나 B-tree 연결을 미리 가져오는 서사는 현재 Todo 범위를 벗어나 제외했다.
