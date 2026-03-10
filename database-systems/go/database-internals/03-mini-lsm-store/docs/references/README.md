# References

## 1. Historical assignment family: LSM Tree Core

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: flush, read path, reopen 요구를 하나의 최소 저장 엔진 흐름으로 복원하기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 문서에서 write path와 read path를 상위 orchestration 관점으로 다시 묶었습니다.

## 2. Database Internals, Chapter 3

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: LSM tree의 write amplification과 read path 배경 설명을 보강하기 위해 참고했습니다.
- 무엇을 반영했는가: 개념 문서에서 flush lifecycle과 newest-first read path를 더 친절하게 설명했습니다.
