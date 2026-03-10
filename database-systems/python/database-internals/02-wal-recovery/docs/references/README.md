# References

## 1. Historical assignment family: WAL Recovery

- 출처 유형: 과거 과제군
- 확인일: 2026-03-10
- 왜 참고했는가: Python에서도 동일한 recovery 규칙을 축소 없이 유지하기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 요구를 append-before-apply와 stop-on-corruption 중심으로 유지했습니다.

## 2. Database Internals, Chapter 6

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: WAL이 왜 memtable보다 먼저 기록돼야 하는지 설명을 보강하기 위해 참고했습니다.
- 무엇을 반영했는가: README와 docs에서 durability 관점의 배경 설명을 강화했습니다.
