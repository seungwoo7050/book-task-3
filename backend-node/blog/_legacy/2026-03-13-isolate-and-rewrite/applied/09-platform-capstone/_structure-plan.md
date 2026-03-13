# 09-platform-capstone structure plan

## 중심 질문

- 이전 프로젝트에서 만든 규약을 capstone에서 어떻게 한 서비스로 합쳤는가
- auth, books, events, persistence는 어디서만 서로 만나게 했는가
- capstone의 완성도를 무엇보다 e2e가 잘 보여 주는 이유는 무엇인가

## 10-development-timeline.md

- 오프닝: capstone이 "새 개념 추가"가 아니라 "기존 규약의 통합 테스트"라는 점을 먼저 밝힌다.
- Phase 1: AppModule이 TypeORM, EventEmitter, Auth, Books, Events를 묶는 장면.
- Phase 2: service는 저장과 발행까지만 하고 listener가 후속 로그를 받는 장면.
- Phase 3: 12개 e2e 시나리오가 통합 서비스의 경계를 한 번에 증명하는 장면.
- 강조 포인트: 다음 프로젝트는 이 capstone을 더 어렵게 만드는 것이 아니라 더 제출 가능한 surface로 다시 패키징하는 단계라는 점.
