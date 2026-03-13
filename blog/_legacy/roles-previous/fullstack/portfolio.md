# Fullstack Portfolio

> PDF/Notion 제출용으로 정리한 풀스택 포지션 제출본입니다.  
> 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Fullstack Engineer |
| 한 줄 포지셔닝 | React/Next.js 기반 사용자 흐름을 만들고, API·인증·데이터·비동기 처리까지 이어지는 제품 경계를 함께 설계하는 개발자 |
| 핵심 스택 | React, Next.js, TypeScript, Go, FastAPI, PostgreSQL, Redis, Docker |
| 대표 프로젝트 | `mini-vrew`, `Client Onboarding Portal`, `Workspace SaaS API` |
| 링크 | [mini-vrew GitHub](https://github.com/seungwoo7050/mini-vrew) · [front-react](../../../front-react/README.md) · [backend-go](../../../backend-go/README.md) |
| 핵심 검증 | `npm run verify --workspace @front-react/client-onboarding-portal` · `go test ./...` · `make e2e` · `make smoke` |

## 대표 프로젝트 1. mini-vrew

**문제**  
사용자에게 보이는 편집 화면과 실제 브라우저 처리 파이프라인을 분리하지 않고 하나의 제품 흐름으로 연결해야 했습니다.

**내가 한 일**  
React 19, TypeScript, Vite 기반 UI를 설계하고, FFmpeg WASM, WebGL, Web Audio API를 이용해 업로드부터 편집, 자막, 필터, export까지 이어지는 클라이언트 중심 제품 경험을 만들었습니다.

**검증**  
README 기준 `npm run test`와 공개 배포본 재확인으로 기능 흐름을 검증했습니다.

**왜 풀스택 역할에 맞는가**  
비록 프론트엔드 단독 프로젝트지만, 사용자 흐름과 처리 파이프라인을 함께 설계했다는 점에서 "기능 화면"과 "시스템 동작"을 동시에 보는 습관을 잘 보여 줍니다.

![mini-vrew 실행 화면](../../assets/mini-vrew.png)

## 대표 프로젝트 2. Client Onboarding Portal

프로젝트: [02-client-onboarding-portal](../../../front-react/study/frontend-portfolio/02-client-onboarding-portal/README.md)

**문제**  
sign-in, workspace profile, invite, review, submit retry까지 이어지는 onboarding flow를 끊기지 않는 사용자 경험으로 만들어야 했습니다.

**내가 한 일**  
Next.js 기반 UI에서 validation, draft restore, route guard, retry 흐름을 설계했습니다. 프론트엔드 안에서 form state, route state, local persistence, service boundary를 분리해 실제 백엔드와 연결될 수 있는 형태로 정리했습니다.

**검증**  
`npm run verify --workspace @front-react/client-onboarding-portal`로 typecheck, unit test, Playwright E2E를 함께 실행했습니다.

**왜 풀스택 역할에 맞는가**  
사용자 흐름을 화면에서 끝내지 않고 인증, 제출, 실패 복구 같은 API 경계를 전제로 UI를 설계했다는 점이 풀스택 포지션에 잘 맞습니다.

![client onboarding portal 실행 화면](../../assets/client-onboarding-portal.png)

## 대표 프로젝트 3. Workspace SaaS API

프로젝트: [18 Workspace SaaS API](../../../backend-go/study/05-portfolio-projects/18-workspace-saas-api/README.md)

**문제**  
JWT auth, 조직 단위 RBAC, invitation, issue workflow, notification을 포함한 B2B SaaS API를 로컬에서 완결형으로 재현해야 했습니다.

**내가 한 일**  
Go 기반으로 API server, worker, Postgres repository, Redis cache/session, OpenAPI, smoke/e2e 흐름을 구성했습니다. owner/admin/member RBAC와 invitation, project/issue/comment 도메인을 제품형 경계로 묶었습니다.

**검증**  
`cd solution/go && go test ./...`, `make e2e`, `make smoke`, `make -C study test-portfolio-repro`로 재현 경로를 정리했습니다.

**왜 풀스택 역할에 맞는가**  
사용자에게 보이는 기능 요구를 API·권한·데이터 모델·비동기 알림으로 연결하는 경험을 보여 줄 수 있습니다.

## 보조 프로젝트와 학습 아카이브

| 영역 | 근거 | 풀스택 관점에서 의미 |
| --- | --- | --- |
| 프론트엔드 제품형 UI | [front-react](../../../front-react/README.md) | 운영 화면과 고객-facing 플로우를 각각 설계 |
| 서비스 경계 분해 | [workspace-backend-v2-msa](../../../backend-fastapi/capstone/workspace-backend-v2-msa/README.md) | gateway, identity, workspace, notification 서비스 분리와 outbox/eventual consistency 학습 |
| 과제형 제품화 | [infobank](../../../infobank/README.md) | stage -> capstone -> official answer 구조로 제품 요구를 정리하는 경험 |
| 검증 자동화 | 현재 워크스페이스 전반 | UI 테스트, API 테스트, smoke/demo CLI를 함께 남기는 습관 |

## 검증 근거

```bash
# 프론트엔드 사용자 흐름
cd front-react/study
npm run verify --workspace @front-react/client-onboarding-portal

# 제품형 API
cd backend-go/study/05-portfolio-projects/18-workspace-saas-api/solution/go
go test ./...
make e2e
make smoke
```

풀스택 역할에서는 화면과 API를 따로 보여 주는 것보다, 두 영역이 하나의 제품 흐름으로 이어진다는 점이 중요하다고 생각합니다. 그래서 저는 UI 프로젝트와 API 프로젝트를 각각 따로 두되, 검증 기준은 모두 "다시 실행 가능한 상태"로 맞추고 있습니다.

## 마무리 요약

저는 프론트엔드에서 시작했지만, 사용자 흐름을 끝까지 책임지기 위해 인증, 데이터 모델, 비동기 처리, 문서화까지 자연스럽게 관심을 넓혀 왔습니다. `mini-vrew`와 `front-react`에서는 제품형 UI를, `Workspace SaaS API`와 `backend-fastapi`에서는 API와 서비스 경계를 함께 다뤘습니다. 풀스택 포지션에서는 이 조합이 제가 단순히 두 기술을 조금씩 하는 사람이 아니라, 제품 흐름을 앞뒤로 연결해 설명할 수 있는 개발자라는 점을 보여 준다고 생각합니다.
