# References

## 1. Historical assignment family: Index and Filter Optimization

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: Bloom filter와 sparse index를 현재 SSTable 구현에 맞게 재조립하기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 문서에서 filter/index를 하나의 lookup pipeline으로 설명하게 됐습니다.

## 2. Database Internals, SSTable optimization sections

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: 읽기 최적화가 storage engine 전체 비용에 미치는 배경을 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: docs에서 sizing과 bounded scan 의미를 더 친절하게 풀었습니다.
