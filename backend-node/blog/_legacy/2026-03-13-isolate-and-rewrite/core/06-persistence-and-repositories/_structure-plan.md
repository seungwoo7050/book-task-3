# 06-persistence-and-repositories structure plan

## 중심 질문

- 메모리 저장소를 SQLite로 바꾸면서도 API 계약을 어떻게 유지했는가
- Express raw SQL repository와 Nest TypeORM repository는 어디서 가장 다르게 보이는가
- persistence 교체가 끝났다는 사실을 API와 DB 양쪽에서 어떻게 증명했는가

## 10-development-timeline.md

- 오프닝: 이 프로젝트의 초점이 "DB 사용법"이 아니라 "저장 전략 교체 후에도 상위 계약을 유지하는 법"이라는 점을 분명히 한다.
- Phase 1: Express에서 schema 초기화와 raw SQL repository를 만든 장면.
- Phase 2: NestJS에서 entity/repository injection으로 같은 계약을 ORM 위에 옮긴 장면.
- Phase 3: API 응답과 실제 DB 상태를 함께 검증한 장면.
- 강조 포인트: 이후 이벤트 설계는 이 persistence boundary가 있어야 자연스럽게 올라간다는 점.
