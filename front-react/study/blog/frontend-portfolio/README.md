# Frontend Portfolio

이 트랙은 학습용 실습을 넘어 "실제 제품처럼 읽히는 결과물"을 만드는 단계다. 같은 프론트엔드 작업이라도 내부도구형 UI, 고객-facing onboarding, 실시간 협업은 전혀 다른 긴장을 만든다. 그래서 세 프로젝트 모두 구현 자체뿐 아니라 실패 복구, 시연 흐름, 검증 전략까지 함께 읽히도록 문서를 나눠 두었다.

## 읽는 순서

1. [01 Ops Triage Console](01-ops-triage-console/00-series-map.md)
   - dense queue, optimistic mutation, failure proof를 가진 internal tool 기록
2. [02 Client Onboarding Portal](02-client-onboarding-portal/00-series-map.md)
   - sign-in gate, draft restore, submit retry를 가진 customer-facing flow 기록
3. [03 Realtime Collab Workspace](03-realtime-collab-workspace/00-series-map.md)
   - presence, reconnect replay, conflict surface를 가진 collaboration capstone 기록

첫 프로젝트가 내부 운영자의 작업 surface를 다룬다면, 두 번째 프로젝트는 고객이 실제로 통과해야 하는 onboarding flow를, 세 번째는 여러 사용자가 동시에 만지는 상태 모델을 다룬다. 같은 트랙 안에서도 시선이 단계적으로 넓어진다.
