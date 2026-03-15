# Structure Outline

## Chosen arc

1. 읽기 최적화 일반론이 아니라 miss-fast path와 bounded scan path라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 실제 bytes read와 footer 값을 먼저 보여 준다.
3. Bloom sizing, sparse block boundary, footer layout, 두 갈래 lookup 경로를 invariant로 정리한다.
4. 마지막에 learned index나 cache 연동이 아직 없다는 점을 분리한다.

## Why this structure

- 이 랩은 관찰 가능한 수치가 중요해서 `bytes_read`와 footer offsets를 초반 evidence로 드는 편이 효과적이다.
- Bloom과 sparse index가 각자 다른 역할을 하므로 두 경로를 섞지 않고 분리해 설명해야 한다.
- MurmurHash3 기반 구현은 docs와 함께 source 근거를 짚어 주는 편이 품질이 높다.

## Rejected alternatives

- Bloom filter 이론만 길게 푸는 구조는 버렸다.
- SSTable 전체 설명으로 되돌아가는 구조도 버렸다.
- range scan이나 cache 얘기를 미리 끌어오는 서사는 현재 범위를 벗어나 제외했다.
