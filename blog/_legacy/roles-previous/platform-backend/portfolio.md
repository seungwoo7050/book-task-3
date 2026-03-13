# Platform / Backend Portfolio

> PDF/Notion 제출용으로 정리한 플랫폼/백엔드 포지션 제출본입니다.  
> 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Platform / Backend Engineer |
| 한 줄 포지셔닝 | 인증·인가, 서비스 경계, 비동기 처리, 운영성, 재현 가능한 검증 경로를 중심으로 서비스 구조를 설계하는 백엔드 개발자 |
| 핵심 스택 | Go, FastAPI, PostgreSQL, Redis, JWT/RBAC, Docker, async jobs, observability |
| 대표 프로젝트 | `Workspace SaaS API`, `workspace-backend-v2-msa`, `collab-saas-security-review` |
| 링크 | [backend-go](../../../backend-go/README.md) · [backend-fastapi](../../../backend-fastapi/README.md) · [security-core](../../../security-core/README.md) |
| 핵심 검증 | `go test ./...` · `make e2e` · `make smoke` · `make test` · `make demo-capstone` |

## 대표 프로젝트 1. Workspace SaaS API

프로젝트: [18 Workspace SaaS API](../../../backend-go/study/05-portfolio-projects/18-workspace-saas-api/README.md)

**문제**  
JWT auth, 조직 단위 RBAC, invitation, issue workflow, async notification을 갖춘 B2B SaaS API를 로컬에서 완결형으로 재현해야 했습니다.

**내가 한 일**  
Go 기반으로 API server, worker, Postgres repository, Redis cache/session store, OpenAPI, e2e, smoke 경로를 구성했습니다. owner/admin/member 권한 체계와 invitation, project/issue/comment 흐름을 제품형 API 도메인으로 정리했습니다.

**검증**  
`go test ./...`, `make e2e`, `make smoke`, `make -C study test-portfolio-repro`로 재현 경로를 유지했습니다.

**왜 이 역할에 맞는가**  
인증/인가, 데이터 모델, 비동기 처리, 로컬 재현성을 하나의 제출 가능한 서비스 표면으로 정리한 점이 플랫폼/백엔드 포지션과 가장 직접적으로 연결됩니다.

## 대표 프로젝트 2. workspace-backend-v2-msa

프로젝트: [workspace-backend-v2-msa](../../../backend-fastapi/capstone/workspace-backend-v2-msa/README.md)

**문제**  
단일 백엔드 기준선을 남겨 둔 채, 같은 협업형 도메인을 `gateway + identity-service + workspace-service + notification-service` 구조로 다시 분해해 내부 경계와 분산 복잡성을 설명해야 했습니다.

**내가 한 일**  
public route shape는 gateway가 유지하고, 내부에서는 서비스별 DB ownership을 지키도록 경계를 나눴습니다. 댓글 생성 뒤에는 outbox, Redis Streams consumer, websocket fan-out으로 이어지는 비동기 전달 경로를 구성했습니다.

**검증**  
README 기준 `make lint`, `make test`, `make smoke`, `docker compose up --build` 경로를 제공합니다.

**왜 이 역할에 맞는가**  
서비스 분해, eventual consistency, 인증 경계, 운영 복잡도를 함께 설명할 수 있다는 점이 플랫폼/백엔드 역할 적합성을 보여 줍니다.

## 대표 프로젝트 3. collab-saas-security-review

프로젝트: [90-capstone-collab-saas-security-review](../../../security-core/study/90-capstone-collab-saas-security-review/README.md)

**문제**  
crypto, auth, backend, dependency finding을 개별적으로 설명하는 데서 끝나지 않고, 실제 운영 관점의 remediation board와 artifact 세트로 통합해야 했습니다.

**내가 한 일**  
`JSON bundle -> consolidated review -> remediation board -> report/artifacts` 파이프라인을 만들었습니다. `review`와 `demo` CLI를 통해 결과 JSON과 보고서 세트를 재생성할 수 있게 했습니다.

**검증**  
`make test-capstone`, `make demo-capstone`과 CLI review 명령으로 검증했습니다.

**왜 이 역할에 맞는가**  
서비스 운영에서 중요한 것은 기능 나열보다 우선순위와 근거를 남기는 것이라는 점을 코드와 산출물로 보여 줄 수 있습니다.

## 보조 프로젝트와 학습 아카이브

| 영역 | 근거 | 플랫폼/백엔드 관점에서 의미 |
| --- | --- | --- |
| 서비스 API 표면 | [backend-node](../../../backend-node/README.md) | NestJS 기반 제출용 서비스 표면과 문서 중심 구조 정리 |
| 모듈형 백엔드 | [backend-spring](../../../backend-spring/README.md) | modular monolith, Redis, Kafka, idempotent payment 구성 경험 |
| 과제형 제품화 | [infobank](../../../infobank/README.md) | 공식 답과 확장 답을 분리하며 release readiness를 설명하는 구조 |
| 인프라/클라우드 보안 | [bithumb](../../../bithumb/README.md) | cloud security control plane과 local artifact 생성 흐름 이해 |

## 검증 근거

```bash
# Go 대표 포트폴리오 API
cd backend-go/study/05-portfolio-projects/18-workspace-saas-api/solution/go
go test ./...
make e2e
make smoke

# FastAPI MSA capstone
cd backend-fastapi/capstone/workspace-backend-v2-msa
make test
make smoke
```

```bash
# Security / remediation artifact
cd security-core
make test-capstone
make demo-capstone
```

생성 산출물 예시:

```text
.artifacts/capstone/demo/01-service-profile.json
.artifacts/capstone/demo/06-remediation-board.json
.artifacts/capstone/demo/07-report.md
```

## 지원처 맞춤 삭제 가능 블록

> 삭제 가능 - Go 중심 공고가 아닐 때 제거

**선택 스택 - Go**  
Go에서는 [`18 Workspace SaaS API`](../../../backend-go/study/05-portfolio-projects/18-workspace-saas-api/README.md)를 대표 결과물로 삼고 있습니다. JWT auth, RBAC, invitation, worker 분리, Postgres/Redis 재현 경로를 함께 설명할 수 있습니다.

> 삭제 가능 - FastAPI/Python 중심 공고가 아닐 때 제거

**선택 스택 - FastAPI/Python**  
FastAPI에서는 [`workspace-backend-v2-msa`](../../../backend-fastapi/capstone/workspace-backend-v2-msa/README.md)를 중심으로 gateway, service boundary, Redis Streams, websocket fan-out, outbox/eventual consistency를 설명할 수 있습니다.

> 삭제 가능 - Node/NestJS 중심 공고가 아닐 때 제거

**선택 스택 - Node/NestJS**  
Node/NestJS에서는 [`10-shippable-backend-service`](../../../backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md)를 통해 Postgres, Redis, Docker Compose, Swagger를 포함한 채용 제출용 서비스 표면을 보여 줄 수 있습니다.

> 삭제 가능 - Spring 중심 공고가 아닐 때 제거

**선택 스택 - Spring Boot**  
Spring에서는 [`commerce-backend-v2`](../../../backend-spring/capstone/commerce-backend-v2/README.md)를 통해 modular monolith, JPA + Flyway, Redis cart/throttling, outbox + Kafka notification을 설명할 수 있습니다.

## 마무리 요약

저는 백엔드 기능을 만드는 것에 그치지 않고, 권한 경계, 비동기 전달, 운영성, 재현 가능한 검증 경로까지 함께 정리하는 방식을 중요하게 생각합니다. `Workspace SaaS API`와 `workspace-backend-v2-msa`는 제품형 서비스 구조를, `collab-saas-security-review`는 운영 판단 기준과 산출물 생성을 보여 줍니다. 플랫폼/백엔드 포지션에서는 이 조합이 제가 구조와 실행 근거를 함께 남기는 개발자라는 점을 가장 잘 드러낸다고 생각합니다.
