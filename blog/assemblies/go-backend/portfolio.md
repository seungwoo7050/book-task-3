# Go Backend Portfolio

> PDF/Notion 제출용 조립본입니다. 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Go Backend Engineer |
| 한 줄 포지셔닝 | JWT auth, RBAC, worker 분리, Postgres/Redis 재현성을 갖춘 제품형 Go API를 설계하는 백엔드 개발자 |
| 핵심 스택 | Go, PostgreSQL, Redis, JWT, RBAC, OpenAPI, Docker |
| 대표 프로젝트 | `18 Workspace SaaS API`, `workspace-backend-v2-msa`, `17 Game Store Capstone` |
| 링크 | [backend-go](../../../backend-go/README.md) · [backend-fastapi](../../../backend-fastapi/README.md) |

## 공통 코어 요약

- 42서울 정규과정 수료
- [`ft_transcendence`](https://github.com/animasyn/ft_transcendence)에서 Django 백엔드 전담, 42 OAuth, JWT, TOTP 기반 2FA 경험 확보
- [cs-core](../../../cs-core/README.md), [network-atda](../../../network-atda/README.md), [database-systems](../../../database-systems/README.md)로 시스템/네트워크/데이터 기반 강화

## backend-common 요약

FastAPI 기반 `workspace-backend`와 `workspace-backend-v2-msa`를 통해 인증/인가, 서비스 경계, async notification, verification report 구조를 공통 백엔드 기준선으로 다졌습니다.

## 대표 프로젝트 1. 18 Workspace SaaS API

JWT auth, 조직 단위 RBAC, invitation, issue workflow, async notification을 로컬에서 완결형으로 재현하는 대표 포트폴리오 과제입니다. API server와 worker를 분리하고, Postgres/Redis와 smoke/e2e를 함께 정리해 제품형 API 관점으로 마감했습니다.

![workspace saas api evidence](../../assets/captures/go-backend/workspace-saas-api-evidence.png)

## 대표 프로젝트 2. workspace-backend-v2-msa

Go 주력 결과물에 붙는 공통 백엔드 기반입니다. 같은 협업형 도메인을 gateway와 내부 서비스로 나눠 서비스 경계, outbox, Redis Streams, websocket fan-out을 설명 가능한 형태로 정리했습니다.

## 대표 프로젝트 3. 17 Game Store Capstone

잔액 차감, 인벤토리 반영, 구매 기록 저장, outbox 기록을 한 흐름으로 묶은 capstone입니다. transaction과 outbox를 제품형 도메인 안에서 설명하는 보조 근거로 사용합니다.

## 선택 부착 모듈

> 삭제 가능 - Infobank 제출 경험을 함께 보여 주고 싶을 때만 유지

`Infobank` 모듈을 붙이면 release gate, compare artifact, 제출용 proof를 함께 정리한 과제형 제품화 경험을 보강할 수 있습니다.

> 삭제 가능 - 보안/운영 흐름을 보강하고 싶을 때만 유지

`Bithumb` 모듈을 붙이면 cloud security control plane과 remediation/report 흐름을 백엔드 보조 근거로 덧붙일 수 있습니다.

## 마무리

이 제출본은 Go를 언어 숙련도 자체보다 제품형 API 설계와 재현 가능한 검증의 관점으로 보여 줍니다. 권한 경계, 데이터 모델, 비동기 처리, smoke/e2e를 함께 설명할 수 있다는 점이 핵심입니다.
