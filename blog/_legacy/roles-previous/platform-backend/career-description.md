# Platform / Backend 경력기술서

> 플랫폼/백엔드 포지션 제출용으로 정리한 프로젝트 기반 경력기술서 초안입니다.

## 한 줄 소개

인증·인가, 서비스 경계, 비동기 처리, 운영성, 재현 가능한 검증 경로를 중심으로 제품형 API와 서비스 구조를 설계하는 백엔드 개발자입니다.

## 핵심 역량 요약

- API 설계: JWT auth, refresh, RBAC, invitation, issue/comment workflow, OpenAPI
- 서비스 구조: modular monolith, gateway/service boundary, worker 분리, outbox/eventual consistency
- 운영성: smoke test, reproducible local environment, cache, throttling, observability
- 산출물 중심 습관: CLI demo, report/artifact 생성, 문서화된 재현 경로 유지

## 대표 경험 1. 현재 워크스페이스의 백엔드/플랫폼 대표군

- 주요 근거:
  - [backend-go](../../../backend-go/README.md)
  - [backend-fastapi](../../../backend-fastapi/README.md)
  - [security-core](../../../security-core/README.md)
- 핵심 내용:
  - Go `18`개 verified 프로젝트, FastAPI 랩/캡스톤, security artifact 생성 capstone을 통해 API와 서비스 경계를 반복적으로 설계하고 검증했습니다.
  - 특히 `Workspace SaaS API`, `workspace-backend-v2-msa`, `collab-saas-security-review`를 대표 결과물로 정리했습니다.
- 플랫폼/백엔드 관점의 의미:
  - 단일 API, 분산 서비스, 운영 판단 artifact를 각각 다른 형태로 구현하며 구조적 사고를 확장했습니다.

## 대표 경험 2. 42서울 정규과정 수료

- 형태: 정규 교육 과정
- 핵심 내용:
  - 시스템 프로그래밍, 메모리 관리, 네트워크, 문제 해결 중심 과정을 수행했습니다.
- 플랫폼/백엔드 관점의 의미:
  - 런타임과 시스템 동작에 대한 기반 이해를 바탕으로, 서비스 구조를 더 깊게 추적하는 습관을 만들었습니다.

## 대표 경험 3. mini-vrew

- 형태: 프론트엔드 단독 개발 및 배포
- 링크:
  - GitHub: <https://github.com/seungwoo7050/mini-vrew>
  - Deploy: <https://mini-vrew.vercel.app>
- 플랫폼/백엔드 관점의 의미:
  - 사용자 요구를 기능 파이프라인으로 연결해 보는 출발점이 된 프로젝트입니다.
  - 백엔드 중심 포지션에서는 주력 경험은 아니지만, 제품 관점을 잃지 않고 서버 구조를 설계하려는 태도를 보여 주는 보조 근거로 활용할 수 있습니다.

## 기술 스택

### 핵심 스택

- PostgreSQL
- Redis
- JWT / RBAC
- Docker / Compose
- async jobs / outbox / event processing
- smoke test / demo CLI / reproducible local environment

> 삭제 가능 - Go 중심 공고가 아닐 때 제거

### 선택 스택 - Go

- 대표 프로젝트: [18 Workspace SaaS API](../../../backend-go/study/05-portfolio-projects/18-workspace-saas-api/README.md)
- 강점:
  - 제품형 API 표면
  - worker 분리
  - Postgres/Redis 재현성
  - e2e/smoke 검증

> 삭제 가능 - FastAPI/Python 중심 공고가 아닐 때 제거

### 선택 스택 - FastAPI / Python

- 대표 프로젝트: [workspace-backend-v2-msa](../../../backend-fastapi/capstone/workspace-backend-v2-msa/README.md)
- 강점:
  - gateway와 내부 서비스 경계
  - 서비스별 DB ownership
  - Redis Streams consumer
  - websocket fan-out

> 삭제 가능 - Node/NestJS 중심 공고가 아닐 때 제거

### 선택 스택 - Node / NestJS

- 대표 프로젝트: [10-shippable-backend-service](../../../backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md)
- 강점:
  - Postgres, Redis, Swagger, Docker Compose를 갖춘 제출용 표면
  - JWT auth, RBAC, cache, throttling

> 삭제 가능 - Spring 중심 공고가 아닐 때 제거

### 선택 스택 - Spring Boot

- 대표 프로젝트: [commerce-backend-v2](../../../backend-spring/capstone/commerce-backend-v2/README.md)
- 강점:
  - modular monolith
  - JPA + Flyway
  - Redis cart/throttling
  - outbox + Kafka notification

## 검증과 재현 습관

- 백엔드 프로젝트는 `go test`, `make e2e`, `make smoke`, `pytest`, demo CLI를 통해 로컬에서 재현 가능한 상태를 남깁니다.
- 단순 기능 설명보다 "어떻게 다시 검증하는지"를 README 표면에 드러내는 방식을 일관되게 유지합니다.
- security-core에서는 artifact 생성까지 포함해 운영 판단 결과를 파일로 남기는 흐름을 구축했습니다.

## 성장 방향

- 실무에서는 더 큰 서비스와 팀 단위 운영 경험을 통해 observability, failure handling, 운영 복잡도에 대한 감각을 넓히고 싶습니다.
- 장기적으로는 특정 프레임워크 사용자에 머무르지 않고, 서비스 구조와 운영 기준을 함께 설계하는 플랫폼/백엔드 엔지니어로 성장하고 싶습니다.
