# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- set/tag/offset 분해: simulator가 어떤 줄을 보고 있는지 설명하려면 주소 분해가 먼저다.
- LRU hit/miss/eviction 상태 전이: 단순 구현보다 상태가 어떻게 변하는지 말할 수 있어야 디버깅이 쉬워진다.
- blocked transpose와 diagonal 처리: 정답 여부보다 cache conflict를 줄이는 설계 이유가 핵심이다.
- spatial locality와 temporal locality: miss 수치를 해석할 때 가장 자주 다시 쓰는 두 축이다.
- miss budget을 설계 목표로 읽기: `<300`, `<1300`, `<2000` 같은 목표는 구현 품질의 설명 가능한 기준점이다.

## 재현 중 막히면 먼저 확인할 것

- simulator reasoning: `../docs/concepts/cache-sim-lru.md`
- transpose 전략: `../docs/concepts/transpose-strategies.md`
- 현재 검증 순서와 수치: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- 성능 과제는 최적화 트릭보다 측정 기준이 먼저 있어야 문서가 흔들리지 않는다.
- cache와 비용 모델을 설명하는 습관은 `proxylab`의 캐시 설계나 이후 시스템 성능 문서에도 그대로 이어진다.
