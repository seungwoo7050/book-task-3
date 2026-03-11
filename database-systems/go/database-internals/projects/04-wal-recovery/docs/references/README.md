# References

## 1. Historical assignment family: WAL Recovery

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: append-only log와 replay 요구를 현재 저장 엔진 구조에 맞게 되살리기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 문서에서 append-before-apply, stop-on-corruption, WAL rotation을 핵심 요구로 정리했습니다.

## 2. Database Internals, Chapter 6

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: durability와 recovery 배경 설명을 보강하기 위해 참고했습니다.
- 무엇을 반영했는가: 개념 문서에서 WAL record format과 recovery policy의 의미를 더 친절하게 설명했습니다.
