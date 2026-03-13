# Node Backend Portfolio

> PDF/Notion 제출용 조립본입니다. 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Node.js Backend Engineer |
| 한 줄 포지셔닝 | NestJS 기반 서비스 표면에 인증, 저장소, 캐시, Swagger, Compose 재현성을 함께 정리하는 백엔드 개발자 |
| 핵심 스택 | Node.js, TypeScript, NestJS, PostgreSQL, Redis, Swagger, Docker Compose |
| 대표 프로젝트 | `10 shippable-backend-service`, `workspace-backend-v2-msa`, `09 platform-capstone` |
| 링크 | [backend-node](../../../backend-node/README.md) · [backend-fastapi](../../../backend-fastapi/README.md) |

## 공통 코어 요약

- 42서울 정규과정과 공통 코어 프로젝트를 통해 시스템/네트워크/데이터 기반을 다졌습니다.
- `ft_transcendence`는 Django 백엔드 전담, 42 OAuth, JWT, TOTP 기반 2FA 경험으로 정리합니다.

## backend-common 요약

FastAPI 기준선에서 인증/인가, API 경계, async notification, verification report 구조를 학습했습니다. Node 제출본에서도 이 감각을 공통 기반으로 사용합니다.

## 대표 프로젝트 1. 10 shippable-backend-service

학습용 capstone을 Postgres, Redis, Docker Compose, Swagger까지 포함한 채용 제출용 NestJS 서비스 표면으로 다시 패키징한 대표 결과물입니다. JWT auth, RBAC, Books CRUD, migration, cache, throttling을 하나의 실행 가능한 표면으로 정리했습니다.

![node health ready](../../assets/captures/node-backend/health-ready.png)

## 대표 프로젝트 2. 09 platform-capstone

REST, pipeline, auth, persistence, events, 운영성 규약을 단일 NestJS 서비스로 통합한 capstone입니다. `10`번 프로젝트의 기준선 역할을 하는 보조 근거로 사용합니다.

## 선택 부착 모듈

> 삭제 가능 - Infobank 제출 경험을 함께 보여 주고 싶을 때만 유지

`Infobank` 모듈을 붙이면 compare artifact, release gate, proof 문서를 포함한 제출형 결과물 경험을 보강할 수 있습니다.

> 삭제 가능 - 보안/운영 흐름을 함께 보여 주고 싶을 때만 유지

`Bithumb` 모듈을 붙이면 cloud security control plane과 remediation/report 흐름을 보조 사례로 덧붙일 수 있습니다.

## 마무리

이 제출본은 Node.js 백엔드를 단순 언어 학습이 아니라, 실제 채용 제출용 서비스 표면으로 정리한 경험을 보여 줍니다. 실행과 문서, Swagger와 검증 루프를 함께 설명할 수 있다는 점이 핵심입니다.
