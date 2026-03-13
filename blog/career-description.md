# 프로젝트 기반 경력기술서

> 이 문서는 실무 회사 경력 이전 단계에서 제출할 수 있도록, 교육 과정과 개인 프로젝트 중심으로 정리한 경력기술서 초안입니다.

## 기본 요약

- 포지션: 프론트엔드 중심 제품 개발자 / 풀스택 협업 가능 인재
- 핵심 키워드: React, TypeScript, Next.js, 제품형 UI, 검증 자동화, 시스템 이해, 자기주도 학습
- 한 줄 소개:
  - 42서울 정규과정 수료 이후 프론트엔드 단독 배포 프로젝트를 직접 완성했고, 현재는 프론트엔드, 백엔드, 모바일, 보안, 네트워크, CS 기초를 아우르는 대규모 학습 레포를 학습 순서에 맞게 전부 구현·검증·문서화하고 있습니다.

## 기술 역량 요약

### Frontend

- React 19, TypeScript, Next.js, Vite 기반 UI 개발
- TanStack Query, React Hook Form, Zod를 활용한 상태/검증 흐름 구성
- 제품형 화면 설계 경험: 운영 콘솔, 온보딩 포털, 미디어 편집 UI
- Playwright, Vitest 기반 검증 루프 구성

### Browser / Client Runtime

- FFmpeg WASM 기반 브라우저 내 비디오 처리
- WebGL 2.0 기반 실시간 필터 렌더링
- Web Audio API 기반 오디오 디코딩과 waveform 시각화
- IndexedDB, Web Workers 등 브라우저 측 비동기 처리 경험

### Backend / System

- Go, FastAPI, Node.js/NestJS, Spring Boot 기반 API 및 서비스 구조 학습
- 인증/인가, 데이터 API, 캐시, 비동기 작업, 이벤트, 운영성, observability 구성 경험
- REST, JWT, RBAC, WebSocket, queue, outbox, retry, idempotency 개념 적용 경험

### Computer Science / Infra

- 알고리즘, 운영체제, 시스템 프로그래밍, 네트워크, 데이터베이스 내부 구조 학습
- Docker, Helm, ArgoCD, Terraform 등 인프라/배포 학습 경험
- 테스트, benchmark, demo CLI, 문서화까지 포함한 재현 가능한 프로젝트 관리 경험

## 프로젝트 경력

### 1. 42서울 정규과정 수료

- 형태: 정규 교육 과정
- 설명:
  - C 언어 기반 문제 해결, 시스템 프로그래밍, 메모리 관리, 프로세스/시그널, 동시성, 네트워크, 인프라 성격의 프로젝트를 단계적으로 수행하며 개발 기초 체력을 다졌습니다.
  - 단순 문법 학습보다 구현 제약이 강한 과제를 반복하면서 low-level 문제를 끝까지 추적하는 습관을 만들었습니다.
- 얻은 역량:
  - 운영체제와 시스템 동작 원리에 대한 감각
  - 협업 과제 환경에서 요구사항을 해석하고 결과물을 완성하는 경험
  - 에러를 추상적으로 넘기지 않고 원인 단위로 좁혀 가는 디버깅 태도

### 2. mini-vrew

- 형태: 프론트엔드 단독 개발 및 배포
- 링크:
  - GitHub: <https://github.com/seungwoo7050/mini-vrew>
  - Deploy: <https://mini-vrew.vercel.app>
- 설명:
  - 브라우저에서 동작하는 비디오 편집 웹앱을 직접 설계하고 구현했습니다.
  - 업로드, 재생, 파형 시각화, 트리밍, 자막 편집, 필터, 썸네일, 내보내기까지 하나의 흐름으로 연결했습니다.
- 주요 기여:
  - React 19, TypeScript, Vite 기반 프론트엔드 구조 설계
  - FFmpeg WASM, WebGL, Web Audio API 등 브라우저 저수준 기능을 실제 UX에 연결
  - IndexedDB 기반 로컬 저장 흐름 구성
- 의미:
  - 화면 구성 능력뿐 아니라 브라우저 런타임 한계와 성능 특성을 고려하는 개발 경험을 확보했습니다.

### 3. 현재 워크스페이스 전체 프로젝트 순차 완료

- 형태: 장기 자기주도 학습 및 구현 아카이브
- 설명:
  - 현재 워크스페이스의 주요 프로젝트들을 학습 순서에 맞게 순차적으로 완료했습니다.
  - 단순히 코드를 작성하는 데서 끝내지 않고, 각 저장소를 `문제 정의 -> 구현 -> 검증 -> 문서화` 흐름으로 다시 정리했습니다.

#### 대표 구성

- Frontend:
  - [`front-react`](../front-react/README.md)
  - 웹 기초, React internals, 제품형 포트폴리오 앱까지 `9`개 프로젝트 구성
- Backend:
  - [`backend-go`](../backend-go/README.md): `18`개 verified 프로젝트
  - [`backend-fastapi`](../backend-fastapi/README.md): 랩 + capstone 구조
  - [`backend-node`](../backend-node/README.md): Node/NestJS 비교 기반 아키텍처 트랙
  - [`backend-spring`](../backend-spring/README.md): Spring Boot 랩 + 커머스 capstone
- Algorithm / CS / Network:
  - [`algorithm`](../algorithm/README.md): `53/53 verified`
  - [`cs-core`](../cs-core/README.md), [`cpp-server`](../cpp-server/README.md), [`network-atda`](../network-atda/README.md)
- Mobile / Security / Cloud:
  - [`mobile`](../mobile/README.md): React Native `10`개 verified 프로젝트
  - [`security-core`](../security-core/README.md): 보안 판단 기준을 코드와 artifact로 재현
  - [`bithumb`](../bithumb/README.md): AWS-first cloud security track
- 과제형 캡스톤:
  - [`infobank`](../infobank/README.md): 추천 시스템, 챗봇 QA Ops 과제형 결과물

#### 이 경험에서 만든 강점

- 프로젝트를 작은 단위로 분해하고, 순서를 재설계하는 능력
- 테스트, E2E, benchmark, demo CLI로 "다시 실행 가능한 프로젝트"를 남기는 습관
- 학습 기록을 README, docs, notion, blog로 정리해 타인에게 설명 가능한 결과물로 바꾸는 문서화 역량

## 검증 및 재현 방식

제가 만든 프로젝트의 공통 특징은 "구현했다"에서 끝나지 않는다는 점입니다.

- 프론트엔드 프로젝트는 typecheck, unit test, E2E까지 묶어 검증합니다.
- 백엔드 및 시스템 프로젝트는 `go test`, `pytest`, `make smoke`, `demo CLI` 등으로 재현 경로를 남깁니다.
- 예를 들어 [`security-core`](../security-core/README.md)에서는 `make demo-capstone` 실행만으로 review artifact 세트를 다시 생성할 수 있습니다.

## 함께 일할 때 기대할 수 있는 점

- 화면만 만들고 끝내지 않고, API 계약과 운영성까지 연결해 이해하려고 합니다.
- 새로운 기술을 빠르게 쓰는 것보다, 문제를 분해하고 검증 기준을 세우는 방식을 중요하게 생각합니다.
- 낯선 분야도 학습 순서를 설계해 끝까지 완수하는 편입니다.

## 보완 방향

- 실무 조직 안에서의 협업 이력과 운영 환경 경험은 앞으로 더 채워야 할 영역입니다.
- 다만 지금까지의 프로젝트들은 혼자서도 긴 호흡의 주제를 끝까지 밀고 가며, 결과물을 타인이 검토 가능한 형태로 정리할 수 있다는 점을 보여 줍니다.
