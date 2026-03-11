# backend-fastapi

실무 FastAPI 백엔드에서 반복해서 만나는 문제를 작은 랩으로 쪼개고, 마지막에 capstone으로 다시 조합하는 학습용 레포입니다. 목표는 기능 목록을 늘리는 것이 아니라, 각 문제를 어떤 경계로 나눴고 어떤 수준까지 검증했는지 스스로 설명할 수 있게 만드는 것입니다.

## 이 레포가 푸는 문제

- 인증, 인가, 데이터 API, 비동기 작업, 실시간 전달, 운영성까지를 한 번에 뭉개지 않고 단계별로 학습하기 어렵다는 문제
- 단일 백엔드와 MSA를 같은 도메인 안에서 비교 설명하기 어렵다는 문제
- 학습 레포가 시간이 지나면 "그래서 무슨 문제를 풀었고 답이 뭐였는지"가 흐려진다는 문제

## 내가 만든 답

- `labs/`에서 주제별 문제를 독립 실행 가능한 작은 FastAPI 워크스페이스로 분해했습니다.
- `capstone/workspace-backend`에서 필수 트랙을 단일 백엔드 기준선으로 다시 통합했습니다.
- `capstone/workspace-backend-v2-msa`에서 같은 도메인을 `gateway + services` 구조로 다시 분해해 비교할 수 있게 했습니다.
- 각 프로젝트는 `README -> problem -> fastapi -> docs -> notion` 순서로 읽히도록 공개 표면을 분리했습니다.

## 현재 검증 상태

- 마지막 기록된 실제 검증 실행일은 `2026-03-10`입니다.
- `2026-03-09`에 `labs/A-auth-lab`부터 `labs/G-ops-lab`, `capstone/workspace-backend`를 재검증했습니다.
- `2026-03-10`에 `labs/H-service-boundary-lab`부터 `labs/K-distributed-ops-lab`, `capstone/workspace-backend-v2-msa`를 재검증했습니다.
- 세부 명령과 한계는 [docs/verification-report.md](docs/verification-report.md)에 기록했습니다.

## 먼저 읽을 순서

1. [docs/README.md](docs/README.md)에서 루트 문서 지도를 확인합니다.
2. [docs/labs-curriculum.md](docs/labs-curriculum.md)에서 전체 순서와 선수 지식을 확인합니다.
3. 관심 있는 랩의 `README.md`에서 문제 요약과 내 답을 먼저 읽습니다.
4. 같은 랩의 `problem/README.md`에서 canonical problem statement와 성공 기준을 확인합니다.
5. `fastapi/README.md`에서 실행과 검증을 따라가고, `docs/README.md`와 `notion/README.md`에서 설계와 학습 로그를 읽습니다.

## 랩 지도

| 트랙 | 경로 | 문제 요약 | 답 형태 | 검증 위치 |
| --- | --- | --- | --- | --- |
| 필수 | [labs/A-auth-lab](labs/A-auth-lab/README.md) | 로컬 계정 인증에서 가입, 이메일 검증, 재설정, 세션 보호를 어디까지 한 묶음으로 가져갈지 정리 | 단일 FastAPI 인증 워크스페이스 | [labs/A-auth-lab/fastapi/README.md](labs/A-auth-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/B-federation-security-lab](labs/B-federation-security-lab/README.md) | 로컬 인증 이후 Google OIDC, 2FA, recovery code를 어떻게 보강할지 정리 | 연합 로그인과 보안 강화를 추가한 FastAPI 워크스페이스 | [labs/B-federation-security-lab/fastapi/README.md](labs/B-federation-security-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/C-authorization-lab](labs/C-authorization-lab/README.md) | 인증과 별개로 역할, 초대, 소유권 규칙을 어떻게 분리할지 정리 | RBAC 중심 FastAPI 워크스페이스 | [labs/C-authorization-lab/fastapi/README.md](labs/C-authorization-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/D-data-api-lab](labs/D-data-api-lab/README.md) | 협업형 CRUD API에서 정렬, 필터, 충돌 제어를 어떻게 설명할지 정리 | 데이터 API 중심 FastAPI 워크스페이스 | [labs/D-data-api-lab/fastapi/README.md](labs/D-data-api-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/E-async-jobs-lab](labs/E-async-jobs-lab/README.md) | 요청-응답과 비동기 작업 경계를 어떻게 안전하게 끊을지 정리 | Celery, Redis, outbox 기반 워크스페이스 | [labs/E-async-jobs-lab/fastapi/README.md](labs/E-async-jobs-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/F-realtime-lab](labs/F-realtime-lab/README.md) | 실시간 연결과 presence를 데이터 처리와 섞지 않고 어떻게 다룰지 정리 | WebSocket 중심 FastAPI 워크스페이스 | [labs/F-realtime-lab/fastapi/README.md](labs/F-realtime-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/G-ops-lab](labs/G-ops-lab/README.md) | 학습용 백엔드에서도 무엇을 운영 기준으로 설명해야 하는지 정리 | health, metrics, CI 문서화 워크스페이스 | [labs/G-ops-lab/fastapi/README.md](labs/G-ops-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [capstone/workspace-backend](capstone/workspace-backend/README.md) | 분리 학습한 인증, 인가, 데이터 API, 알림을 단일 제품 구조로 어떻게 다시 조합할지 정리 | 단일 FastAPI capstone v1 | [capstone/workspace-backend/fastapi/README.md](capstone/workspace-backend/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 심화 | [labs/H-service-boundary-lab](labs/H-service-boundary-lab/README.md) | 단일 백엔드를 어떤 서비스 경계로 쪼갤지와 DB ownership을 어떻게 설명할지 정리 | `identity-service`와 `workspace-service` 분리 워크스페이스 | [labs/H-service-boundary-lab/fastapi/README.md](labs/H-service-boundary-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 심화 | [labs/I-event-integration-lab](labs/I-event-integration-lab/README.md) | 서비스 간 비동기 전달과 eventual consistency를 어떻게 검증할지 정리 | outbox + consumer 기반 MSA 워크스페이스 | [labs/I-event-integration-lab/fastapi/README.md](labs/I-event-integration-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 심화 | [labs/J-edge-gateway-lab](labs/J-edge-gateway-lab/README.md) | public API와 내부 서비스를 gateway에서 어떻게 분리할지 정리 | edge gateway 추가 MSA 워크스페이스 | [labs/J-edge-gateway-lab/fastapi/README.md](labs/J-edge-gateway-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 심화 | [labs/K-distributed-ops-lab](labs/K-distributed-ops-lab/README.md) | 여러 서비스를 어떤 운영 기준으로 함께 관찰할지 정리 | 분산 운영성 중심 MSA 워크스페이스 | [labs/K-distributed-ops-lab/fastapi/README.md](labs/K-distributed-ops-lab/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 심화 | [capstone/workspace-backend-v2-msa](capstone/workspace-backend-v2-msa/README.md) | 같은 협업 도메인을 MSA로 다시 풀었을 때 무엇이 단순해지고 무엇이 복잡해지는지 비교 | MSA capstone v2 | [capstone/workspace-backend-v2-msa/fastapi/README.md](capstone/workspace-backend-v2-msa/fastapi/README.md), [docs/verification-report.md](docs/verification-report.md) |

## 이 레포를 읽을 때 기준

- 각 랩은 독립 실행을 우선합니다. 공통 패키지를 억지로 추출하지 않고, 랩마다 필요한 구조를 스스로 갖춥니다.
- `problem/README.md`는 canonical problem statement이고, 프로젝트 `README.md`는 문제 요약과 답안 인덱스 역할을 맡습니다.
- `fastapi/README.md`는 실행과 검증, `docs/README.md`는 설계 설명, `notion/README.md`는 학습 로그를 담당합니다.
- `capstone/workspace-backend`는 단일 백엔드 기준선이고, `capstone/workspace-backend-v2-msa`는 같은 도메인의 MSA 비교판입니다.
- 이 레포는 "학습 가능하고 다시 실행 가능한 상태"를 목표로 하며, 곧바로 운영 배포 가능한 제품을 주장하지 않습니다.

## 포트폴리오로 확장하려면

- 도메인을 그대로 복제하지 말고, 자신이 설명하기 쉬운 문제 영역으로 바꿉니다.
- 기능 수보다 "왜 이 문제를 따로 풀었는가", "어디까지 검증했는가", "무엇을 일부러 남겼는가"를 README에 먼저 적습니다.
- 테스트 통과만 적지 말고, 문서 수준 가정과 실제 실행한 사실을 분리해서 기록합니다.
- MSA를 가져갈 때는 서비스 수보다 경계 선택 이유와 새로 생기는 운영 비용을 먼저 설명합니다.

## 기준 문서

- 루트 문서 지도: [docs/README.md](docs/README.md)
- 저장소 규칙과 문서 원칙: [docs/repo-standards.md](docs/repo-standards.md)
- 전체 FastAPI 학습 순서: [docs/labs-curriculum.md](docs/labs-curriculum.md)
- 마지막 기록된 검증 결과: [docs/verification-report.md](docs/verification-report.md)
- Compose 기반 health probe 스크립트: [tools/compose_probe.sh](tools/compose_probe.sh)
