# Range Cursor And Rule-Based Planner

index를 만든 다음 바로 SQL planner로 넘어가면 너무 갑자기 커진다. 이 lab은 그 사이에 있는 가장 작은 다리를 둔다.

## range cursor

- `start <= key <= end` 범위를 만족하는 첫 leaf entry를 찾는다.
- 이후에는 linked leaf를 따라가며 정렬된 순서로 row id를 꺼낸다.
- 범위 끝을 넘으면 즉시 종료한다.

## rule-based planner

- equality predicate가 index column에 걸리면 `index-point-lookup`
- range predicate가 index column에 걸리면 `index-range-scan`
- 그 외에는 `full-scan`

이 planner는 cost-based optimizer가 아니다. 그 대신 "왜 지금 이 질의가 index를 탈 수 있는가"를 한 줄 설명으로 돌려준다.
