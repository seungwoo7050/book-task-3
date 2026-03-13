# backend-fastapi blog

이 폴더는 `backend-fastapi`의 각 독립 프로젝트를 처음부터 끝까지 따라가기 위한 최종 블로그 모음이다. 목적은 기능 요약을 모아 두는 것이 아니라, 각 랩과 capstone이 어떤 질문에서 시작됐고 어떤 코드와 검증을 거쳐 지금의 구조에 닿았는지 읽는 순서를 분명하게 만드는 데 있다.

## 이 시리즈를 읽는 방법
1. 먼저 관심 있는 프로젝트의 `00-series-map.md`를 읽고, 그 글이 붙잡는 질문과 구현 흐름부터 잡습니다.
2. 이어서 같은 폴더의 `10-development-timeline.md`로 넘어가 코드, 테스트, CLI가 실제로 어떤 순서로 맞물렸는지 따라갑니다.
3. `_legacy`는 이전 초안 보관소이고, `_evidence-ledger.md`와 `_structure-plan.md`는 필요할 때만 뒤에서 확인하는 보조 문서입니다.

## 필수 트랙
- [A-auth-lab](labs/A-auth-lab/00-series-map.md): 로컬 인증을 refresh rotation과 CSRF까지 끌고 가는 시작점
- [B-federation-security-lab](labs/B-federation-security-lab/00-series-map.md): OIDC, 2FA, recovery code로 인증 상태 기계를 한 단계 더 잘게 쪼개는 글
- [C-authorization-lab](labs/C-authorization-lab/00-series-map.md): 로그인에서 물러서서 역할, 초대, 소유권 규칙만 고립해 보는 글
- [D-data-api-lab](labs/D-data-api-lab/00-series-map.md): CRUD보다 목록 semantics와 optimistic locking을 먼저 붙잡는 글
- [E-async-jobs-lab](labs/E-async-jobs-lab/00-series-map.md): 요청-응답 밖으로 작업을 밀어내며 outbox와 retry 상태를 설명하는 글
- [F-realtime-lab](labs/F-realtime-lab/00-series-map.md): WebSocket 연결 상태와 presence를 별도 모델로 세우는 글
- [G-ops-lab](labs/G-ops-lab/00-series-map.md): health, metrics, CI, target shape를 운영 질문으로 분리하는 글
- [workspace-backend](capstone/workspace-backend/00-series-map.md): 앞선 랩의 경계를 하나의 협업형 백엔드로 다시 조합하는 기준선

## 심화 트랙
- [H-service-boundary-lab](labs/H-service-boundary-lab/00-series-map.md): identity와 workspace를 claims만으로 잇는 첫 MSA 분해 단계
- [I-event-integration-lab](labs/I-event-integration-lab/00-series-map.md): comment 저장과 notification 생성을 eventual consistency로 끊어 보는 글
- [J-edge-gateway-lab](labs/J-edge-gateway-lab/00-series-map.md): public API shape를 gateway에 남기고 내부 계약을 단순화하는 글
- [K-distributed-ops-lab](labs/K-distributed-ops-lab/00-series-map.md): 분산 구조의 health, metrics, request correlation을 따로 읽는 글
- [workspace-backend-v2-msa](capstone/workspace-backend-v2-msa/00-series-map.md): 단일 백엔드 기준선을 MSA로 다시 풀고 장애 복구까지 비교하는 최종판

## 읽을 때 기억할 기준
- A~G는 문제 하나를 깊게 파고드는 랩이고, `workspace-backend`는 그 경계들을 단일 백엔드로 다시 조합한 기준선입니다.
- H~K는 MSA로 넘어가며 경계를 어디서 끊고, 이벤트와 gateway, 운영성을 어떤 순서로 늘려 갔는지 보여 줍니다.
- `workspace-backend-v2-msa`는 마지막 비교판입니다. v1에서 단순했던 것이 어디서 복잡해졌는지, 어떤 검증은 끝났고 어떤 검증은 아직 불안정한지까지 함께 읽어야 합니다.
