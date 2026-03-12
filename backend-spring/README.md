# backend-spring

Spring Boot 백엔드에서 반복해서 만나는 문제를 작은 랩으로 분해하고, 마지막에 커머스 캡스톤으로 다시 조합하는 학습용 레포입니다. 목표는 기능 수집이 아니라 "무슨 문제를 왜 풀었고, 어디까지 검증했는지"를 스스로 설명할 수 있는 결과물을 남기는 것입니다.

## 이 레포가 푸는 문제

- 인증, 인가, JPA, 이벤트, 캐시, 운영성을 한 번에 뭉개면 학습 포인트와 실패 원인이 섞이는 문제
- 학습 레포가 시간이 지나면 "그래서 무슨 문제를 풀었고 답이 뭐였는지"가 흐려지는 문제
- 같은 도메인에서 기준선 baseline과 더 강한 결과물을 비교 설명하기 어려운 문제

## 내가 만든 답

- `labs/`에서 주제별 문제를 독립 실행 가능한 Spring Boot 워크스페이스로 분해했습니다.
- `capstone/commerce-backend`에서 개별 랩 학습을 하나의 커머스 백엔드 baseline으로 다시 조합했습니다.
- `capstone/commerce-backend-v2`에서 같은 도메인을 더 깊게 구현해 대표 결과물로 삼았습니다.
- 각 프로젝트는 `README -> problem -> spring -> docs -> notion` 순서로 읽히도록 공개 표면을 분리했습니다.

## 현재 검증 상태

- 마지막 기록된 실제 검증 실행일은 `2026-03-09`입니다.
- 그 시점에 7개 랩과 2개 캡스톤의 `make lint`, `make test`, `make smoke`, Compose health 확인을 다시 실행했습니다.
- 세부 범위와 아직 증명하지 않은 영역은 [docs/verification-report.md](docs/verification-report.md)에 기록했습니다.

## 먼저 읽을 순서

1. [docs/README.md](docs/README.md)에서 루트 문서 지도를 확인합니다.
2. [docs/curriculum.md](docs/curriculum.md)에서 전체 순서와 각 랩이 무엇을 가르치는지 확인합니다.
3. 관심 있는 랩이나 캡스톤의 `README.md`에서 문제 요약과 내 답을 먼저 읽습니다.
4. 같은 프로젝트의 `problem/README.md`에서 canonical problem statement와 성공 기준을 확인합니다.
5. `spring/README.md`에서 실행과 검증을 따라가고, `docs/README.md`와 `notion/README.md`에서 설계와 학습 로그를 읽습니다.

## 랩과 캡스톤 지도

| 트랙 | 경로 | 문제 요약 | 답 형태 | 검증 위치 |
| --- | --- | --- | --- | --- |
| 필수 | [labs/A-auth-lab](labs/A-auth-lab/README.md) | 로컬 계정 인증에서 가입, refresh rotation, 복구 흐름을 어디까지 기본 인증으로 볼지 정리 | 단일 Spring 인증 랩 | [labs/A-auth-lab/spring/README.md](labs/A-auth-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/B-federation-security-lab](labs/B-federation-security-lab/README.md) | 로컬 인증 이후 OAuth2 federation, 2FA, audit를 어떻게 보강할지 정리 | 인증 강화 Spring 랩 | [labs/B-federation-security-lab/spring/README.md](labs/B-federation-security-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/C-authorization-lab](labs/C-authorization-lab/README.md) | 인증과 별개로 membership, role, ownership 규칙을 어떻게 분리할지 정리 | RBAC 중심 Spring 랩 | [labs/C-authorization-lab/spring/README.md](labs/C-authorization-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/D-data-jpa-lab](labs/D-data-jpa-lab/README.md) | JPA를 CRUD 마법처럼 숨기지 않고 설계 선택으로 드러내는 방법 정리 | JPA 중심 Spring 랩 | [labs/D-data-jpa-lab/spring/README.md](labs/D-data-jpa-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/E-event-messaging-lab](labs/E-event-messaging-lab/README.md) | request-response만으로 끝나지 않는 백엔드에서 이벤트 경계를 어떻게 설명할지 정리 | outbox 중심 Spring 랩 | [labs/E-event-messaging-lab/spring/README.md](labs/E-event-messaging-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/F-cache-concurrency-lab](labs/F-cache-concurrency-lab/README.md) | 캐시, 멱등성, 재고 경합을 한 시나리오에서 어떻게 묶어 설명할지 정리 | cache/concurrency Spring 랩 | [labs/F-cache-concurrency-lab/spring/README.md](labs/F-cache-concurrency-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 필수 | [labs/G-ops-observability-lab](labs/G-ops-observability-lab/README.md) | 운영성을 부록이 아니라 백엔드 기본기로 어떻게 다룰지 정리 | ops/observability Spring 랩 | [labs/G-ops-observability-lab/spring/README.md](labs/G-ops-observability-lab/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 기준선 | [capstone/commerce-backend](capstone/commerce-backend/README.md) | 개별 랩을 하나의 커머스 백엔드 baseline으로 다시 조합하는 방법 정리 | baseline capstone | [capstone/commerce-backend/spring/README.md](capstone/commerce-backend/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |
| 대표 결과물 | [capstone/commerce-backend-v2](capstone/commerce-backend-v2/README.md) | 같은 도메인을 더 깊게 구현해 면접에서 설명 가능한 결과물로 끌어올리는 방법 정리 | portfolio-grade capstone | [capstone/commerce-backend-v2/spring/README.md](capstone/commerce-backend-v2/spring/README.md), [docs/verification-report.md](docs/verification-report.md) |

## 대표 결과물과 baseline의 관계

- [commerce-backend-v2](capstone/commerce-backend-v2/README.md)는 이 레포의 대표 결과물입니다.
- [commerce-backend](capstone/commerce-backend/README.md)는 비교용 baseline을 의도적으로 보존한 버전입니다.
- 두 캡스톤은 경쟁 관계가 아니라 "왜 v2가 필요한가"를 설명하기 위한 짝입니다.

## 이 레포를 읽을 때 기준

- 각 랩은 독립 실행을 우선합니다. 공통 코드를 억지로 추출하지 않고, 각 주제를 스스로 설명 가능한 단위로 남깁니다.
- `problem/README.md`는 문제 정의와 성공 기준, 프로젝트 `README.md`는 문제 요약과 내 답, `spring/README.md`는 실행과 검증 진입점, `docs/README.md`는 설계 설명, `notion/README.md`는 학습 로그를 맡습니다.
- 이 레포는 학습 가능하고 다시 실행 가능한 상태를 목표로 하며, 곧바로 운영 배포 가능한 제품을 주장하지 않습니다.

## 기준 문서

- 루트 문서 지도: [docs/README.md](docs/README.md)
- 저장소 규칙과 문서 원칙: [docs/repo-standards.md](docs/repo-standards.md)
- 전체 학습 순서: [docs/curriculum.md](docs/curriculum.md)
- 마지막 기록된 검증 결과: [docs/verification-report.md](docs/verification-report.md)
- 공개 포지셔닝 가이드: [docs/publication-status.md](docs/publication-status.md)
