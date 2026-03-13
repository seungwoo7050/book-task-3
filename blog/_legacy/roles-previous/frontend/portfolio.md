# Frontend Portfolio

> PDF/Notion 제출용으로 정리한 프론트엔드 포지션 제출본입니다.  
> 기준일: 2026년 3월 13일

| 항목 | 내용 |
| --- | --- |
| 포지션 | Frontend Engineer |
| 한 줄 포지셔닝 | React, TypeScript, Next.js 기반으로 제품형 UI를 설계하고, 브라우저 런타임 한계를 고려해 사용자 경험을 완성하는 프론트엔드 개발자 |
| 핵심 스택 | React, Next.js, TypeScript, Vite, TanStack Query, React Hook Form, Zod, Playwright |
| 대표 프로젝트 | `mini-vrew`, `Ops Triage Console`, `Client Onboarding Portal` |
| 링크 | [mini-vrew GitHub](https://github.com/seungwoo7050/mini-vrew) · [mini-vrew Deploy](https://mini-vrew.vercel.app) · [front-react](../../../front-react/README.md) |
| 핵심 검증 | `npm run test`, `npm run verify --workspace @front-react/ops-triage-console`, `npm run verify --workspace @front-react/client-onboarding-portal` |

## 대표 프로젝트 1. mini-vrew

**문제**  
브라우저 안에서 업로드, 재생, 파형 확인, 트리밍, 자막 편집, 필터, 내보내기까지 이어지는 비디오 편집 흐름을 하나의 프론트엔드 제품 경험으로 연결해야 했습니다.

**내가 한 일**  
React 19, TypeScript, Vite 기반 구조를 설계하고, FFmpeg WASM, WebGL 2.0, Web Audio API, IndexedDB를 조합해 무거운 처리와 상호작용 UI를 한 화면 안에 통합했습니다. 단순 기능 목록이 아니라 플레이어, waveform, captions, filters, export를 제품 흐름으로 정리하는 데 집중했습니다.

**검증**  
README 기준 `npm run test`와 배포본 재확인으로 기능 흐름을 검증했고, 공개 배포본을 기준으로 실제 사용자 흐름을 다시 점검할 수 있습니다.

**왜 프론트엔드 역할에 맞는가**  
브라우저 API와 복합 상호작용 UI를 다뤘다는 점, 그리고 "보이는 화면"만이 아니라 로컬 처리 성능과 사용자 경험을 함께 설계했다는 점이 프론트엔드 포지션과 가장 직접적으로 연결됩니다.

![mini-vrew 실행 화면](../../assets/mini-vrew.png)

## 대표 프로젝트 2. Ops Triage Console

프로젝트: [01-ops-triage-console](../../../front-react/study/frontend-portfolio/01-ops-triage-console/README.md)

**문제**  
운영 화면처럼 데이터가 많고 상태 전이가 잦은 UI에서 triage workflow를 어떻게 설계하고 검증할지 보여 주는 프로젝트가 필요했습니다.

**내가 한 일**  
dashboard summary, queue, saved view, bulk action, optimistic update, rollback, retry를 포함한 운영 콘솔을 Next.js App Router 기반으로 구성했습니다. UI 상태 관리뿐 아니라 실패 후 복구와 keyboard-only 동선까지 검증 범위에 넣었습니다.

**검증**  
`npm run verify --workspace @front-react/ops-triage-console` 기준으로 typecheck, Vitest, Playwright E2E를 함께 실행하도록 정리했습니다.

**왜 프론트엔드 역할에 맞는가**  
단순히 예쁜 화면보다 제품 운영 화면에서 중요한 정보 구조, 상호작용 밀도, 실패 처리 UX를 설명할 수 있다는 점을 보여 줍니다.

![ops triage console 실행 화면](../../assets/ops-triage-console.png)

## 대표 프로젝트 3. Client Onboarding Portal

프로젝트: [02-client-onboarding-portal](../../../front-react/study/frontend-portfolio/02-client-onboarding-portal/README.md)

**문제**  
고객-facing onboarding flow에서 validation, draft restore, route guard, submit retry를 끊기지 않는 사용자 경험으로 묶어야 했습니다.

**내가 한 일**  
sign-in, onboarding wizard, invite, review, submit retry를 하나의 포털 흐름으로 만들었습니다. React Hook Form, Zod, TanStack Query를 사용해 폼 유효성, 진행 상태, 로컬 draft 복구를 분리하고 연결했습니다.

**검증**  
`npm run verify --workspace @front-react/client-onboarding-portal`로 typecheck, unit test, Playwright E2E를 묶었습니다.

**왜 프론트엔드 역할에 맞는가**  
복잡한 사용자 흐름에서 입력 검증과 단계 이동, 실패 후 재시도까지 UI 품질을 유지하는 역량을 보여 주기 좋습니다.

## 보조 프로젝트와 학습 아카이브

| 영역 | 근거 | 프론트엔드 관점에서 의미 |
| --- | --- | --- |
| 웹 기초 | [front-react](../../../front-react/README.md) | semantic layout, DOM state, networked UI를 단계적으로 학습하고 정리 |
| React internals | [react-internals](../../../front-react/study/react-internals/README.md) | VDOM, render pipeline, hooks/runtime을 직접 구현하며 프레임워크 동작 원리 이해 |
| 모바일 | [mobile](../../../mobile/README.md) | React Native `10`개 verified 프로젝트로 모바일 상호작용과 제품 흐름 감각 확장 |
| 시스템 이해 | [42서울](https://42.fr/en/homepage/) 및 현재 워크스페이스 전반 | 프론트엔드에 머무르지 않고 백엔드, 네트워크, 시스템 구조까지 연결해 사고하는 습관 |

## 검증 근거

```bash
# mini-vrew
npm install
npm run test

# front-react 포트폴리오 트랙
cd front-react/study
npm run verify --workspace @front-react/ops-triage-console
npm run verify --workspace @front-react/client-onboarding-portal
```

프론트엔드 프로젝트에서는 "동작 화면"만큼이나 "다시 검증 가능한 상태"가 중요하다고 생각합니다. 그래서 UI 프로젝트도 typecheck, unit test, E2E를 함께 묶어 두는 방식을 일관되게 유지하고 있습니다.

## 마무리 요약

저는 제품형 UI를 설계할 때 브라우저 API, 상태 전이, 실패 처리, 검증 루프를 함께 봅니다. `mini-vrew`에서는 무거운 브라우저 처리와 상호작용 UI를 연결했고, `front-react` 포트폴리오 트랙에서는 운영 화면과 고객-facing 플로우를 각각 설계해 보였습니다. 프론트엔드 포지션에서는 이 두 경험이 제가 사용자 경험과 구현 복잡도를 함께 다루는 개발자라는 점을 가장 잘 보여 준다고 생각합니다.
