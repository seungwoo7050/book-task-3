# I-event-integration-lab 문서 지도

이 문서는 “댓글 저장과 알림 전달은 같은 트랜잭션이 아니다”라는 사실을 서비스 경계에서 어떻게 설명할지 정리하는 개념 지도다. 핵심은 `workspace-service`가 outbox까지 책임지고, `notification-service`는 stream consume와 dedupe만 맡는다는 점을 분명히 하는 데 있다.

## 먼저 보면 좋은 질문

- outbox가 왜 여전히 필요한가
- stream payload에는 무엇을 넣고 무엇을 넣지 않는가
- idempotent consumer는 어떤 실패를 흡수하는가
- relay와 consumer를 같은 서비스에 두지 않는 이유는 무엇인가

## 이 문서에서 중심으로 보는 구조

- `workspace-service`는 comment 저장과 outbox 적재를 같은 트랜잭션으로 끝낸다.
- 별도 relay가 outbox를 Redis Streams로 밀어 넣는다.
- `notification-service`는 stream을 읽고 receipt 테이블로 dedupe를 보장한다.
- 결과적으로 comment 저장과 알림 생성은 eventual consistency 관계가 된다.

## 읽고 나면 설명할 수 있어야 하는 것

- `comment.created.v1` 계약
- relay와 consume의 책임 차이
- eventual consistency가 허용하는 지연
- 중복 읽기가 있어도 결과를 한 번만 남기는 구조

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [학습 노트](../notion/README.md)
