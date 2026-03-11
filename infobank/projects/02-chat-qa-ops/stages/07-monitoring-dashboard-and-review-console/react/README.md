# React 구현 안내

`08/v1-regression-hardening/react`의 dashboard slice를 그대로 가져와 overview, failures, session review, eval runner 화면 구조를 학습용으로 분리했다.

## 실행 및 검증

- 의존성 설치: `pnpm install`
- 테스트: `pnpm test --run`

## 현재 상태

- 상태: 복제된 mocked UI 테스트까지 확인했다.
- 남은 범위: stage07/python snapshot API를 직접 바라보도록 환경 변수 wiring은 사용자가 지정해야 한다., 실제 persistence와 background refresh는 capstone 버전에서만 다룬다.

## 먼저 볼 파일

- `src/pages/Overview.tsx`
- `src/pages/SessionReview.tsx`
- `src/pages/EvalRunner.tsx`
- `src/api/client.ts`
