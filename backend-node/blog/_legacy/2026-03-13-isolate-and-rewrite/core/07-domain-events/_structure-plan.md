# 07-domain-events structure plan

## 중심 질문

- 왜 persistence 다음 단계가 queue가 아니라 event boundary 정리였는가
- Express `EventEmitter`와 NestJS listener registration은 어떤 차이로 드러나는가
- 성공 경로에서만 이벤트가 나간다는 사실을 어떤 테스트가 고정하는가

## 10-development-timeline.md

- 오프닝: 이 프로젝트의 주제가 "이벤트 기능 추가"가 아니라 "서비스 본문에서 side effect를 빼내는 것"이라는 점을 분명히 한다.
- Phase 1: Express에서 `EventBus`를 감싸고 성공 후 발행 규칙을 세운 장면.
- Phase 2: NestJS에서 `@OnEvent()` listener와 service 발행 시점을 분리한 장면.
- Phase 3: 실패 연산에서는 이벤트가 나가지 않는다는 사실을 테스트로 증명한 장면.
- 강조 포인트: 이후 capstone 통합에서 이벤트가 service 본문을 비대하게 만들지 않는 기반이 여기서 생긴다는 점.
