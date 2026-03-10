# References

## 1. Repository-designed bridge project: Clustered KV Capstone

- 출처 유형: 현재 레포 설계
- 확인일: 2026-03-10
- 왜 참고했는가: 과거 과제군에는 저장 엔진과 분산 경로를 하나로 묶는 단계가 없어서 별도 캡스톤이 필요했습니다.
- 무엇을 반영했는가: 현재 커리큘럼은 routing, replication, storage를 실제 write pipeline으로 연결하는 마지막 단계를 갖게 됐습니다.

## 2. Designing Data-Intensive Applications

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: partitioning, replication, consensus 이전 단계의 서비스 경계를 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: docs와 README에서 static topology와 replicated write pipeline을 큰 그림으로 설명합니다.

## 3. Database Internals

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: local node store가 disk-backed storage engine 관점과 어떻게 이어지는지 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: storage 엔진과 분산 요청이 만나는 지점을 문서화했습니다.
