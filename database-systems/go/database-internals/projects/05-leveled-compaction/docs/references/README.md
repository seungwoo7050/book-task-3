# References

## 1. Historical assignment family: Compaction

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: merge ordering과 level manager 역할을 현재 Go 구현에 맞게 재해석하기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 문서에서 merge 우선순위와 tombstone drop 조건을 명시적으로 정리했습니다.

## 2. Database Internals, compaction-related chapters

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: leveled compaction의 배경과 write amplification trade-off를 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: docs에서 merge ordering과 manifest atomicity의 의미를 더 분명하게 연결했습니다.
