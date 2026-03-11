# References

## 1. Designing Data-Intensive Applications, replication and durability chapters

- 출처 유형: 책
- 확인일: 2026-03-11
- 왜 참고했는가: follower lag, retry, quorum ack를 작은 replication lab으로 압축하기 위해 참고했습니다.
- 무엇을 반영했는가: README와 개념 문서가 commit과 convergence를 분리해 설명합니다.

## 2. Raft / log replication teaching materials

- 출처 유형: 논문/강의 자료
- 확인일: 2026-03-11
- 왜 참고했는가: follower별 next index와 retry 개념을 full consensus 없이 떼어 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: 내부 구현이 `append`, `ack`, `nextIndex`, `matchIndex`, `commitIndex`를 최소 단위로 노출합니다.
