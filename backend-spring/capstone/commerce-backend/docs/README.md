# commerce-backend 설계 메모

이 문서는 baseline capstone이 현재 어디까지 구현되었고, 왜 일부 깊이를 남겼는지 요약한다.

## 현재 구현 범위

- login surface와 `me` endpoint
- admin product 생성과 public product listing
- cart item 생성과 order placement
- checkout 시 stock decrement
- PostgreSQL, Redis, Mailpit, Redpanda가 포함된 Compose 환경

## 의도적 단순화

- auth는 contract-level 중심이며 full persisted stack은 아니다
- payment는 아직 없다
- notification과 event consumer는 완전히 연결되지 않았다

## 왜 baseline이 필요한가

- 이 버전은 최종 답이 아니라 비교 기준점이다
- modular monolith를 baseline으로 남겨야 `commerce-backend-v2`의 개선 축이 선명해진다
- 랩 학습을 하나의 커머스 도메인으로 다시 묶는 첫 단계 역할을 한다
