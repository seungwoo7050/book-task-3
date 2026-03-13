# 03-rest-api-foundations structure plan

## 중심 질문

- 같은 Books CRUD를 왜 Express와 NestJS 두 레인으로 다시 풀었는가
- Express composition root와 Nest module DI의 차이는 코드에서 어디서 드러나는가
- 두 레인이 정말 같은 계약을 지키는지는 어떤 검증으로 확인했는가

## 10-development-timeline.md

- 오프닝: 이 프로젝트가 backend-node 전체 비교 학습의 출발점이라는 점을 먼저 놓는다.
- Phase 1: Express에서 service -> controller -> router -> app을 손으로 연결한 장면.
- Phase 2: NestJS에서 module/controller/service로 같은 계약을 framework DI 위에 다시 얹은 장면.
- Phase 3: unit/e2e 테스트가 두 레인의 공통 CRUD surface를 비교 가능하게 만드는 장면.
- 강조 포인트: 비교의 목적은 승부가 아니라 "계층 분리와 DI가 어느 레벨에서 드러나는가"를 코드로 보는 데 있다.
