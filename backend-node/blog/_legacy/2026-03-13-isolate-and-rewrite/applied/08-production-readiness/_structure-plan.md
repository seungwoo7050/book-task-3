# 08-production-readiness structure plan

## 중심 질문

- 운영성 문제를 왜 domain feature보다 먼저 별도 프로젝트로 뺐는가
- runtime config, health/readiness, structured logging은 어떤 순서로 붙었는가
- 이 프로젝트의 검증이 unit보다 e2e와 stdout에 더 기대는 이유는 무엇인가

## 10-development-timeline.md

- 오프닝: applied 단계의 시작이 기능 통합이 아니라 운영 surface 정리라는 점을 먼저 세운다.
- Phase 1: runtime config를 타입과 서비스로 고정한 장면.
- Phase 2: health/readiness endpoint와 structured logging interceptor를 붙인 장면.
- Phase 3: env patch를 바꿔 가며 200/503과 stdout logging을 확인한 장면.
- 강조 포인트: capstone이 이 프로젝트를 건너뛰면 "기능은 되지만 운영 표면이 없는 서비스"가 된다는 점.
