# References

## 1. Historical assignment family: LSM Tree Core

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: 정렬 삽입, tombstone, ordered iteration 같은 최소 성공 기준을 되살리기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 요구와 보조 스타터 코드를 Go API 기준으로 다시 설계했습니다.

## 2. Database Internals, Chapter 3

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: memtable이 flush 이전 단계에서 어떤 역할을 맡는지 설명을 보강하기 위해 참고했습니다.
- 무엇을 반영했는가: README와 개념 메모에서 ordered write path와 memtable 책임 범위를 더 분명히 적었습니다.
