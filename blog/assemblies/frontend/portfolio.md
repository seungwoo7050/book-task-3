# Frontend Portfolio

> PDF/Notion 제출용 조립본입니다. 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Frontend Engineer |
| 한 줄 포지셔닝 | React, TypeScript, Next.js 기반으로 제품형 UI를 설계하고, 브라우저 런타임 한계까지 함께 다루는 프론트엔드 개발자 |
| 핵심 스택 | React, Next.js, TypeScript, Vite, TanStack Query, React Hook Form, Zod, Playwright |
| 대표 프로젝트 | `mini-vrew`, `Ops Triage Console`, `Client Onboarding Portal` |
| 링크 | [mini-vrew GitHub](https://github.com/seungwoo7050/mini-vrew) · [mini-vrew Deploy](https://mini-vrew.vercel.app) · [front-react](../../../front-react/README.md) |

## 공통 코어 요약

- 42서울 정규과정에서 시스템과 디버깅의 기초를 쌓았습니다.
- 상세 사례는 [`ft_transcendence`](https://github.com/animasyn/ft_transcendence) 하나만 사용하며, Django 백엔드 전담, 42 OAuth, JWT, TOTP 기반 2FA 경험으로 정리합니다.
- [cs-core](../../../cs-core/README.md), [network-atda](../../../network-atda/README.md), [database-systems](../../../database-systems/README.md)을 통해 화면 뒤의 시스템 구조까지 함께 이해하는 기반을 만들었습니다.

## 대표 프로젝트 1. mini-vrew

브라우저 안에서 업로드, 재생, 파형 확인, 트리밍, 자막 편집, 필터, export까지 이어지는 비디오 편집 흐름을 단독으로 설계하고 배포했습니다. FFmpeg WASM, WebGL, Web Audio API, IndexedDB를 제품형 UX와 연결했다는 점이 가장 강한 프론트엔드 근거입니다.

![mini-vrew](../../assets/captures/frontend/mini-vrew.png)

## 대표 프로젝트 2. Ops Triage Console

운영 화면처럼 데이터가 많고 상태 전이가 잦은 UI를 Next.js App Router 기반으로 구성했습니다. optimistic update, rollback, retry, keyboard-only 동선까지 검증 범위에 넣어 운영 화면의 밀도를 설명 가능한 결과물로 정리했습니다.

![ops triage console](../../assets/captures/frontend/ops-triage-console.png)

## 대표 프로젝트 3. Client Onboarding Portal

sign-in, onboarding wizard, invite, review, submit retry를 하나의 고객-facing 플로우로 정리했습니다. React Hook Form, Zod, TanStack Query를 이용해 validation, route guard, draft restore를 실제 사용자 흐름처럼 연결했습니다.

## 보조 프로젝트와 학습 아카이브

| 영역 | 근거 | 의미 |
| --- | --- | --- |
| React internals | [front-react](../../../front-react/README.md) | 프레임워크 동작 원리를 직접 구현하며 이해 |
| 모바일 | [mobile](../../../mobile/README.md) | 제품형 상호작용을 모바일 감각으로 확장 |
| 공통 코어 | [common-core module](../../modules/common-core/portfolio.md) | 시스템, 네트워크, 데이터 계층까지 연결해 사고하는 기반 |

## 마무리

저는 프론트엔드에서 화면만이 아니라 브라우저 API, 상태 전이, 실패 처리, 검증 루프를 함께 봅니다. `mini-vrew`와 `front-react` 포트폴리오 트랙은 제가 제품형 UI를 설명 가능한 결과물로 정리해 온 개발자라는 점을 가장 잘 보여 줍니다.
