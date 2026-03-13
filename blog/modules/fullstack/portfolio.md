# Fullstack Portfolio Module

| 항목 | 내용 |
| --- | --- |
| 포지셔닝 | 사용자 흐름을 화면과 API, 인증, 데이터, 검증 루프까지 연결하는 풀스택 모듈 |
| 대표 프로젝트 | `mini-vrew`, `Client Onboarding Portal`, `workspace-backend-v2-msa` |
| 핵심 스택 | React, Next.js, TypeScript, FastAPI, PostgreSQL, Redis, Docker |

## 메인 프로젝트

### mini-vrew

사용자에게 보이는 편집 화면과 실제 브라우저 처리 파이프라인을 하나의 제품 흐름으로 연결한 단독 개발/배포 프로젝트입니다.

### Client Onboarding Portal

sign-in, validation, draft restore, submit retry까지 이어지는 onboarding flow를 제품형 UI로 설계했습니다.

### backend-common 연계

`workspace-backend`와 `workspace-backend-v2-msa`는 인증, 워크스페이스 도메인, 알림을 API 경계와 비동기 전달로 설명하는 공통 백엔드 기반입니다.

## 메인 캡처

![mini-vrew](../../assets/captures/fullstack/mini-vrew.png)
![workspace backend v2 msa evidence](../../assets/captures/fullstack/workspace-backend-v2-msa-evidence.png)

## 마무리

이 모듈은 프론트엔드와 백엔드를 단순히 둘 다 해 봤다는 의미가 아니라, 사용자 흐름을 앞뒤로 끊기지 않게 연결하는 역량을 보여 주는 재료입니다.
