# References

## 1. Repository-designed bridge project: Clustered KV Capstone

- 출처 유형: 현재 레포 설계
- 확인일: 2026-03-10
- 왜 참고했는가: Python 입문 트랙에서도 분산 요청 흐름을 실제 서비스 경계까지 이어 보는 단계가 필요했습니다.
- 무엇을 반영했는가: FastAPI boundary를 포함한 self-contained capstone 문서 구조를 만들었습니다.

## 2. Designing Data-Intensive Applications

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: routing과 replication을 서비스 API 관점으로 연결해 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: README와 docs에서 static topology와 replicated write pipeline이 더 분명해졌습니다.

## 3. Database Internals

- 출처 유형: 책
- 확인일: 2026-03-10
- 왜 참고했는가: 각 node의 local store가 단일 노드 storage engine과 어떻게 이어지는지 설명하기 위해 참고했습니다.
- 무엇을 반영했는가: 문서가 분산 레포지만 local storage 역할을 놓치지 않도록 보강했습니다.
