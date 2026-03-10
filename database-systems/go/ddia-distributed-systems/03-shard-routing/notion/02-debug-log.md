# 디버그 포인트

이 파일은 과거를 꾸며내는 로그가 아니라, 다시 읽거나 다시 구현할 때 가장 먼저 의심할 지점을 프로젝트 기준으로 정리한 메모입니다.

## 먼저 확인할 세부 지점
### 1. 빈 ring이나 단일 노드 경계 조건이 깨지는 경우
- 의심 파일: `../internal/routing/routing.go`
- 깨지는 징후: 기본 edge case를 놓치면 이후 모든 cluster 논의가 불안정해집니다.
- 확인 테스트: `TestEmptyAndSingleNodeRouting`
- 다시 볼 질문: ring이 비었을 때와 node 하나일 때를 별도 경로로 다루는가?

### 2. virtual node 분포가 치우치는 경우
- 의심 파일: `../internal/routing/routing.go`
- 깨지는 징후: hash나 virtual node 수 설정이 나쁘면 일부 노드에 키가 몰립니다.
- 확인 테스트: `TestDistributionAndRebalance`
- 다시 볼 질문: virtual node 생성 규칙이 node별로 충분히 다른 hash space를 만들고 있는가?

### 3. batch routing 결과가 단건 routing과 다르게 나오는 경우
- 의심 파일: `../internal/routing/routing.go`
- 깨지는 징후: 대량 routing helper가 따로 놀면 데모와 실제 cluster routing 설명이 갈라집니다.
- 확인 테스트: `TestBatchRouting`
- 다시 볼 질문: batch helper가 내부적으로 단건 route와 같은 함수를 재사용하는가?
