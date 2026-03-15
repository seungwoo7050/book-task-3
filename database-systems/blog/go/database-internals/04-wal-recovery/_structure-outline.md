# Structure Outline

## Chosen arc

1. durability 전체가 아니라 append-before-apply와 replay policy라는 범위를 먼저 제한한다.
2. demo와 추가 재실행으로 reopen recovery와 WAL rotation 결과를 먼저 보여 준다.
3. record format, stop-on-corruption, reopen ordering, WAL rotation을 invariant로 정리한다.
4. 마지막에 group commit과 distributed recovery가 아직 없다는 점을 따로 못 박는다.

## Why this structure

- 이 랩은 file format과 store orchestration이 함께 있기 때문에 두 층을 분리해서 설명해야 읽기 쉽다.
- 단순 demo만으로는 rotation이 보이지 않아 추가 재실행 결과를 초반 evidence로 꼭 넣었다.
- recovery policy는 테스트와 docs가 명확히 맞물리는 지점이라 invariant 장의 중심으로 두는 편이 좋다.

## Rejected alternatives

- WAL 일반론 위주 설명은 버렸다.
- 테스트 케이스만 요약하는 구조도 버렸다.
- fsync semantics를 과도하게 확장하는 서술은 현재 근거 범위를 벗어나 제외했다.
