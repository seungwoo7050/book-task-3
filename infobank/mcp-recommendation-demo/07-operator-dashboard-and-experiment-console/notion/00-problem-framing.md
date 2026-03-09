# 00 — 문제 정의: 왜 운영 대시보드가 필요한가

## 배경

stage 05까지 usage log, feedback loop, compare snapshot이 모두 API 레벨에서 동작하고 있었다.  
stage 06에서 compatibility gate와 release gate까지 붙었다.  

그런데 이 기능들을 확인하려면 매번 `curl`이나 테스트 코드를 직접 실행해야 했다.  
운영자가 "지금 baseline이랑 candidate 중 어느 쪽이 나은지" 한 화면에서 확인할 수 없다는 것은, 사실상 실험을 돌리는 의미가 반감된다는 뜻이다.

## 문제 정의

> MCP 추천 시스템의 전체 운영 흐름 — catalog 관리, 추천 실험, usage 집계, feedback, compare snapshot, release candidate — 을  
> 운영자가 한 화면에서 조작하고 결과를 즉시 확인할 수 있는 대시보드를 설계하라.

## 요구 사항 분해

### 1. Operator Dashboard

- Catalog CRUD: MCP 도구 목록을 조회·수정·추가·삭제
- Usage Totals: impression / click / accept 집계를 실시간 표시
- Compare Snapshot: baseline vs candidate의 nDCG@3, uplift 등 핵심 지표 시각화

### 2. Experiment Console

- 실험 생성: name, hypothesis, baseline/candidate strategy, traffic split 입력
- 상태 토글: draft → running → completed 전환
- 삭제: 더 이상 필요 없는 실험 제거

### 3. Release Console (v2 확장)

- Release Candidate CRUD: RC 생성·조회·수정·삭제
- Compatibility & Release Gate 실행: 버튼 하나로 gate 결과 확인
- Artifact Export Preview: 제출용 JSON 증빙 미리보기

### 4. Feedback Loop 통합

- 대시보드에서 직접 feedback을 남기고, 다음 candidate 추천에 반영되는지 확인
- "채택 로그 남기기" 버튼으로 usage event도 즉석에서 기록

## 이 stage가 커버하지 않는 것

- 인증/인가(RBAC): stage 08 v3에서 처리
- 비동기 워커 기반 백그라운드 작업: stage 08 v3의 pg-boss 영역
- CSS/디자인 시스템 자체의 깊은 논의: 대시보드는 기능 구현에 집중

## 선행 stage 의존성

| stage | 대시보드가 소비하는 API |
|-------|------------------------|
| 02 | `/api/catalog` — catalog CRUD |
| 04 | `/api/recommendations`, `/api/recommendations/candidate` |
| 05 | `/api/usage-events`, `/api/feedback`, `/api/evals/*`, `/api/compare/*` |
| 06 | `/api/compatibility/*`, `/api/release-gate/*`, `/api/submission/*` |

결국 이 stage는 "이미 만들어 둔 API 9개 이상을 하나의 React 컴포넌트에서 소비하는 통합 뷰"를 만드는 일이다.
