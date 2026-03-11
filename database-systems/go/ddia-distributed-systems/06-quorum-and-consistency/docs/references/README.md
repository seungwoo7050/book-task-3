# References

## 1. Designing Data-Intensive Applications, replication and consistency chapters

- 출처 유형: 책
- 확인일: 2026-03-11
- 왜 참고했는가: quorum read/write와 stale read 예시를 현재 프로젝트 문제로 압축하기 위해 참고했습니다.
- 무엇을 반영했는가: README와 개념 문서가 `W + R > N` 규칙과 consistency trade-off를 설명형으로 정리합니다.

## 2. Dynamo-style quorum literature

- 출처 유형: 논문/시스템 설계 문헌
- 확인일: 2026-03-11
- 왜 참고했는가: sloppy quorum, hinted handoff, vector clock처럼 이번 단계에서 일부러 제외할 범위를 선명하게 나누기 위해 참고했습니다.
- 무엇을 반영했는가: 문제 문서가 single-version register와 고정 quorum 정책만 현재 범위로 선언합니다.
