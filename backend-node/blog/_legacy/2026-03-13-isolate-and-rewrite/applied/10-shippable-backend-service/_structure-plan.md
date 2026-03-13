# 10-shippable-backend-service structure plan

## 중심 질문

- 09 capstone을 왜 그대로 두지 않고 별도 shippable surface로 다시 포장했는가
- Postgres, Redis, Swagger, cache, throttling은 코드에서 어떤 순서로 드러나는가
- 이 프로젝트의 핵심 검증이 `ECONNREFUSED -> compose up -> 16 passed` 흐름인 이유는 무엇인가

## 10-development-timeline.md

- 오프닝: 이 프로젝트가 "새 기능 추가"보다 "제출 가능한 실행 계약 만들기"라는 점을 먼저 세운다.
- Phase 1: runtime config, bootstrap, migration-aware DB options, compose surface를 정리한 장면.
- Phase 2: Redis cache와 login throttling을 Books/Auth에 연결한 장면.
- Phase 3: 인프라가 없으면 e2e가 실패하고, compose 뒤에는 16개 시나리오가 통과하는 장면.
- 강조 포인트: shippable 서비스의 품질은 코드보다도 "어떤 전제로 어떻게 다시 띄우는가"를 설명할 수 있는 데 있다.
