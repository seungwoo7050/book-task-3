# 회고

## 이번 단계에서 명확해진 것
- consistency는 복제 유무보다 read/write quorum 겹침 조건으로 설명하는 편이 더 선명합니다.
- stale read는 “장애가 났다”보다 “응답 집합이 어디와 겹치지 않는가”로 설명해야 이해가 빠릅니다.

## 아직 단순화한 부분
- concurrent write conflict를 다루지 않았습니다.
- sloppy quorum과 repair path도 없습니다.
- latency나 geo-distribution 비용도 없습니다.

## 다음에 확장한다면
- read repair와 hinted handoff를 붙여 eventual convergence를 더 현실적으로 보여 줄 수 있습니다.
- leader election을 붙여 어떤 replica를 우선 신뢰할지 운영 관점 질문으로 넘어갈 수 있습니다.
