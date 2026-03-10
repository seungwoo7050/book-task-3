# backend-fastapi

이 저장소는 FastAPI 백엔드를 한 번에 크게 만드는 대신, 실무에서 반복해서 마주치는 주제를 작은 랩으로 나눠 학습하도록 설계한 학습용 레포입니다. 목표는 "정답 복제"가 아니라, 각 랩에서 설계 의도와 검증 습관을 익히고 이를 바탕으로 더 나은 개인 포트폴리오 레포를 스스로 완성할 수 있게 돕는 것입니다.

## 이 레포가 가르치는 것

- 인증, 인가, 데이터 API, 비동기 작업, 실시간 통신, 운영성까지 FastAPI 백엔드의 핵심 주제를 분리해서 연습하는 방법
- 같은 협업형 도메인을 단일 백엔드와 MSA로 각각 설명하는 방법
- 기능 구현만이 아니라 "왜 이렇게 나눴는가", "무엇을 일부러 단순화했는가", "어디까지 검증했는가"를 문서로 남기는 방법
- 작은 랩에서 익힌 패턴을 마지막 capstone에서 하나의 SaaS형 백엔드로 다시 조합하는 방법

## 먼저 이렇게 읽기

1. [docs/labs-curriculum.md](docs/labs-curriculum.md)에서 전체 커리큘럼과 추천 순서를 확인합니다.
2. 관심 있는 랩의 `README.md`를 열어 학습 목표와 범위를 확인합니다.
3. 같은 랩의 `problem/README.md`에서 문제 정의와 성공 기준을 읽습니다.
4. `fastapi/README.md`에서 실제 실행과 검증 방법을 따라갑니다.
5. `docs/README.md`와 `notion/README.md`로 넘어가 설계 포인트와 학습 노트를 정리합니다.

## 랩 지도

| 경로 | 핵심 주제 | 이 랩이 주는 포트폴리오 신호 |
| --- | --- | --- |
| [labs/A-auth-lab](labs/A-auth-lab/README.md) | 로컬 계정 인증, 세션, 복구 흐름 | 보안 기본기와 상태 전이 설계 |
| [labs/B-federation-security-lab](labs/B-federation-security-lab/README.md) | Google OIDC, 2FA, 회복 코드, 감사 로그 | 외부 인증 연동과 보안 강화 흐름 |
| [labs/C-authorization-lab](labs/C-authorization-lab/README.md) | RBAC, 초대, 소유권 규칙 | 권한 경계와 서비스 계층 설계 |
| [labs/D-data-api-lab](labs/D-data-api-lab/README.md) | CRUD, 정렬/필터링, 소프트 삭제, 낙관적 락 | 데이터 API 구조화와 변경 충돌 처리 |
| [labs/E-async-jobs-lab](labs/E-async-jobs-lab/README.md) | Celery, Redis, outbox, idempotency | 비동기 작업 안정성과 재시도 전략 |
| [labs/F-realtime-lab](labs/F-realtime-lab/README.md) | WebSocket 인증, presence, fan-out | 실시간 이벤트 전달과 연결 상태 관리 |
| [labs/G-ops-lab](labs/G-ops-lab/README.md) | health/readiness, metrics, CI, 배포 문서 | 운영 가능성을 설명하는 최소 백엔드 |
| [capstone/workspace-backend](capstone/workspace-backend/README.md) | capstone v1, 단일 백엔드 통합 | 분리 학습 내용을 하나의 제품형 구조로 합치는 능력 |
| [labs/H-service-boundary-lab](labs/H-service-boundary-lab/README.md) | 서비스 분리, DB ownership, bearer claims | 서비스 경계를 어디서 끊어야 하는지 설명 |
| [labs/I-event-integration-lab](labs/I-event-integration-lab/README.md) | outbox, Redis Streams, idempotent consumer | 이벤트 기반 통합과 eventual consistency 설명 |
| [labs/J-edge-gateway-lab](labs/J-edge-gateway-lab/README.md) | edge gateway, cookie/CSRF, request id 전파 | public API와 내부 서비스를 분리해 설명 |
| [labs/K-distributed-ops-lab](labs/K-distributed-ops-lab/README.md) | 서비스별 health, JSON 로그, metrics, AWS target shape | 다중 서비스 운영 기준을 문서와 검증으로 설명 |
| [capstone/workspace-backend-v2-msa](capstone/workspace-backend-v2-msa/README.md) | capstone v2, MSA 재편 | 같은 도메인을 단일 백엔드와 MSA로 비교 설계 |

## 이 레포를 읽을 때 기억할 점

- 각 랩은 독립 실행을 우선합니다. 공통 패키지를 억지로 추출하지 않고, 랩마다 필요한 구조를 스스로 갖춥니다.
- `capstone/workspace-backend`는 단일 백엔드 기준선인 v1입니다.
- `capstone/workspace-backend-v2-msa`는 같은 도메인을 MSA로 다시 분해한 v2입니다.
- capstone은 랩 코드를 그대로 import 하지 않습니다. 앞선 랩에서 익힌 개념을 다시 구현하고 조합합니다.
- 현재 `notion/`은 공개용 학습 노트이고, 이전 버전은 같은 경로의 `notion-archive/`에 백업으로 남아 있습니다.
- 이 레포는 "학습 가능하고 다시 실행 가능한 상태"를 목표로 하며, 곧바로 운영 배포 가능한 제품을 주장하지 않습니다.

## 포트폴리오로 확장하려면

- 도메인을 그대로 복제하지 말고, 자신이 설명하기 쉬운 문제 영역으로 바꿉니다.
- 각 랩의 단일 주제를 유지하되, README에 왜 그 주제를 따로 분리했는지 직접 서술합니다.
- 테스트 통과만 적지 말고 "무엇은 검증했고 무엇은 아직 문서 수준인지"를 분리해서 기록합니다.
- capstone을 만들 때는 기능 수를 늘리기보다 경계가 명확한 서비스 구조, 에러 모델, 배포 가정을 정교하게 다듬는 쪽이 더 설득력 있습니다.
- MSA를 포트폴리오로 가져갈 때는 서비스 수보다 경계 선택 이유와 새로 생기는 운영 비용을 먼저 설명합니다.

## 검증과 기준 문서

- 저장소 규칙과 문서 원칙: [docs/repo-standards.md](docs/repo-standards.md)
- 마지막 기록된 검증 결과: [docs/verification-report.md](docs/verification-report.md)
- 전체 FastAPI 학습 순서: [docs/labs-curriculum.md](docs/labs-curriculum.md)
- Compose 기반 health probe 스크립트: [tools/compose_probe.sh](tools/compose_probe.sh)
