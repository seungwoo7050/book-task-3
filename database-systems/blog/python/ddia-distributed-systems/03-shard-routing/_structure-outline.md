# Structure Outline

## Chosen arc

1. 문제 범위를 먼저 정의해 cluster control plane 기대를 걷어낸다.
2. Ring과 Router surface를 보여 준 뒤 demo와 distribution 수치를 붙인다.
3. 그다음 hash ordering, wrap-around, virtual node, moved key 계산을 invariant로 정리한다.
4. 마지막에는 검증 범위와 운영상 비어 있는 부분을 분리해 과장을 막는다.

## Why this structure

- 이 랩은 API 수가 적어서 파일 설명보다 "placement invariant" 중심 서술이 더 효율적이다.
- 테스트가 이미 분산도와 이동량을 숫자로 표현하므로, 문서도 그 수치를 재사용해 추상적 설명을 줄이는 편이 좋다.
- shard routing을 membership system과 혼동하기 쉬워서, boundary를 마지막에 다시 못 박는 구성이 필요하다.

## Rejected alternatives

- consistent hashing 일반론을 길게 풀어내는 구조는 버렸다.
- key별 예시만 나열하는 구조도 버렸다. 이 랩의 핵심은 개별 key보다 분산과 이동량의 aggregate다.
- cluster 운영 시나리오를 상상으로 덧붙이는 구조는 source-first 원칙에 맞지 않아 제외했다.
