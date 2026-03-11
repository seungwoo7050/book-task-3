# I-event-integration-lab 설계 문서

이 폴더는 I-event-integration-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

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

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [학습 노트](../notion/README.md)
