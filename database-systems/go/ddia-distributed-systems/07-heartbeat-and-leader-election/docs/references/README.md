# References

## 1. Raft paper, leader election sections

- 출처 유형: 논문
- 확인일: 2026-03-11
- 왜 참고했는가: term, majority vote, step-down 규칙을 최소 election lab으로 압축하기 위해 참고했습니다.
- 무엇을 반영했는가: README와 개념 문서가 failure detector와 election authority를 분리해 설명합니다.

## 2. Designing Data-Intensive Applications, failure handling chapters

- 출처 유형: 책
- 확인일: 2026-03-11
- 왜 참고했는가: heartbeat와 failure detector가 왜 완전한 truth가 아니라 suspicion signal인지 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: docs가 “죽었음을 증명”이 아니라 “의심을 기반으로 authority를 교체”한다는 표현을 유지합니다.
