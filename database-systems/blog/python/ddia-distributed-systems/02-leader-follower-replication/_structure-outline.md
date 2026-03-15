# Structure Outline

## Chosen arc

1. 문제 범위를 먼저 좁혀 reader가 election/consensus를 기대하지 않게 만든다.
2. leader, log, follower 세 surface를 보여 준 뒤 첫 sync demo를 붙인다.
3. 그다음 sequential offset, watermark, idempotent apply를 invariant 중심으로 해부한다.
4. 마지막에 pytest와 수동 replay 결과를 묶어 "지금 검증된 것"과 "아직 비어 있는 것"을 분리한다.

## Why this structure

- 이 랩은 구현량이 작아서 파일별 설명보다 invariant별 설명이 더 읽기 좋다.
- 복제 랩에서 가장 흔한 오해는 "distributed system 전체를 풀었다"는 식의 과장이라서, boundary를 마지막 장에서 다시 한 번 못 박아야 한다.
- demo 출력이 매우 짧기 때문에, 추가 replay snippet을 별도로 포함해 idempotency를 눈에 보이게 만들었다.

## Rejected alternatives

- README 확장판처럼 디렉터리 안내만 반복하는 구조는 버렸다.
- DDIA replication 일반론을 길게 설명하는 구조는 버렸다.
- leader/follower를 각각 독립 섹션으로 나누는 구조도 버렸다. 이 랩의 핵심은 둘의 상호작용이기 때문이다.
