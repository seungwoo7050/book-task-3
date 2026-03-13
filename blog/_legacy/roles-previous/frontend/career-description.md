# Frontend 경력기술서

> 프론트엔드 포지션 제출용으로 정리한 프로젝트 기반 경력기술서 초안입니다.

## 한 줄 소개

React, TypeScript, Next.js 기반으로 제품형 UI를 구현하고, 브라우저 런타임 특성과 검증 자동화까지 함께 고려하는 프론트엔드 개발자입니다.

## 핵심 역량 요약

- 제품형 UI 설계: 운영 콘솔, 온보딩 포털, 비디오 편집 UI처럼 상호작용 밀도가 높은 화면 구성 경험
- 브라우저 API 활용: FFmpeg WASM, WebGL 2.0, Web Audio API, IndexedDB, Web Workers 활용 경험
- 상태/검증 흐름 설계: React Hook Form, Zod, TanStack Query, Playwright 기반 검증 루프 구성
- 구조 이해: 프론트엔드 구현뿐 아니라 React internals, 백엔드/API 경계, 시스템 구조까지 함께 학습하며 문제를 넓게 보는 습관

## 대표 경험 1. mini-vrew

- 형태: 프론트엔드 단독 개발 및 배포
- 링크:
  - GitHub: <https://github.com/seungwoo7050/mini-vrew>
  - Deploy: <https://mini-vrew.vercel.app>
- 핵심 내용:
  - 브라우저 기반 비디오 편집 웹앱을 직접 설계하고 구현했습니다.
  - 비디오 플레이어, waveform, trimming, captions, filters, export를 하나의 사용자 흐름으로 연결했습니다.
- 기여 포인트:
  - React 19, TypeScript, Vite 기반 제품형 UI 구조 설계
  - FFmpeg WASM, WebGL, Web Audio API를 실제 UX에 연결
  - IndexedDB 기반 로컬 저장 흐름 구성
- 프론트엔드 관점의 의미:
  - 브라우저가 제공하는 저수준 기능을 사용자 경험으로 번역하는 경험을 확보했습니다.

## 대표 경험 2. front-react 포트폴리오 트랙

- 위치: [front-react](../../../front-react/README.md)
- 핵심 내용:
  - 웹 기초, React internals, 제품형 UI까지 `9`개 프로젝트를 순차적으로 구현하고 검증했습니다.
  - 특히 `Ops Triage Console`, `Client Onboarding Portal`에서 운영 화면과 고객-facing 플로우를 각각 설계했습니다.
- 기여 포인트:
  - Next.js App Router 기반 화면 구성
  - optimistic update, retry, draft restore, route guard, form validation 구현
  - typecheck, Vitest, Playwright를 묶은 검증 체계 정리
- 프론트엔드 관점의 의미:
  - "컴포넌트를 만들 수 있다" 수준을 넘어 실제 제품 화면과 사용자 흐름을 설명 가능한 결과물로 정리했습니다.

## 대표 경험 3. 42서울 정규과정 수료

- 형태: 정규 교육 과정
- 핵심 내용:
  - C 언어 기반 문제 해결, 시스템 프로그래밍, 메모리 관리, 네트워크 등 기초를 단계적으로 수행했습니다.
- 프론트엔드 관점의 의미:
  - 화면 구현에 필요한 디테일뿐 아니라 런타임과 시스템 동작 원리까지 함께 이해하려는 기반을 만들었습니다.
  - 에러를 추상적으로 넘기지 않고 원인 단위로 좁혀 가는 디버깅 태도를 갖추게 됐습니다.

## 기술 스택

### 핵심 스택

- React
- Next.js
- TypeScript
- Vite
- TanStack Query
- React Hook Form
- Zod
- Playwright
- Vitest

### 브라우저/클라이언트 런타임

- FFmpeg WASM
- WebGL 2.0
- Web Audio API
- IndexedDB
- Web Workers

### 보조 이해

- React Native 기반 모바일 UI 흐름
- API/인증/데이터 모델에 대한 백엔드 기초 이해
- 테스트와 문서화를 포함한 재현 가능한 프로젝트 관리

## 검증과 재현 습관

- UI 프로젝트도 `typecheck + unit test + E2E`를 함께 묶어 검증합니다.
- README, docs, notion, blog를 분리해 다른 사람이 다시 읽고 따라올 수 있는 구조를 남깁니다.
- 구현 결과를 "보여 주는 화면"뿐 아니라 "다시 검증 가능한 경로"까지 포함해 정리합니다.

## 성장 방향

- 실무 제품에서 더 큰 사용자 트래픽과 협업 구조를 경험하며 프론트엔드 설계 감각을 더 넓히고 싶습니다.
- 장기적으로는 제품 UI를 잘 만드는 사람을 넘어, 프론트엔드 아키텍처와 품질 기준을 함께 제안할 수 있는 개발자로 성장하고 싶습니다.
