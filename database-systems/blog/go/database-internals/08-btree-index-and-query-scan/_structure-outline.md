# Structure Outline

## Chosen arc

1. full SQL 엔진이 아니라 split/cursor/planner의 최소 표면이라는 범위를 먼저 잡는다.
2. demo와 추가 재실행으로 planner 전략과 split 결과를 먼저 보여 준다.
3. duplicate key row-id list, split separator, linked-leaf cursor, rule-based fallback을 invariant로 정리한다.
4. 마지막에는 cost-based optimizer와 MVCC가 아직 없다는 점을 분리한다.

## Why this structure

- 이 랩은 자료구조와 planner가 같이 나오기 때문에 둘의 연결점을 먼저 드러내는 편이 읽기 좋다.
- root separator key와 duplicate row-id list는 테스트에서 바로 확인되는 강한 증거라 초반에 가져오는 게 효과적이다.
- planner가 작은 만큼, 과장 없이 "rule-based only"를 계속 강조해야 문서 품질이 유지된다.

## Rejected alternatives

- B+Tree 일반론을 길게 푸는 구조는 버렸다.
- planner만 따로 떼어 설명하는 구조도 버렸다.
- 디스크 page layout까지 상상으로 이어 붙이는 서사는 현재 소스 범위를 벗어나 제외했다.
