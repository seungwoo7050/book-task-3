# workspace-backend-v2-msa 문서 지도

이 문서는 v1 기준선에서 v2로 넘어오면서 어떤 경계가 새로 생겼는지 추적하는 개념 지도다. v2의 목적은 서비스를 많이 늘리는 데 있지 않고, 같은 협업형 도메인을 다른 아키텍처로 다시 설명할 수 있게 만드는 데 있다.

## 먼저 보면 좋은 질문

- 왜 `platform`을 그대로 두지 않고 `identity/workspace/notification`으로 나눴는가
- public API는 왜 gateway에서 유지하는가
- outbox, stream, pub/sub은 각각 어느 경계에 필요한가
- v1보다 좋아진 점과 나빠진 점은 무엇인가
- 무엇이 실제 검증된 사실이고, 무엇이 아직 target shape 문서 수준의 가정인가

## 이 문서에서 중심으로 보는 구조

- `gateway`는 public route shape, cookie, CSRF, request id, websocket edge를 담당한다.
- `identity-service`는 회원가입, 로그인, email verify, refresh rotation과 token 발급을 맡는다.
- `workspace-service`는 workspace, invite, project, task, comment와 outbox를 소유한다.
- `notification-service`는 stream consumer, dedupe receipt, pub/sub 발행을 맡는다.
- 각 서비스는 자기 DB만 읽고 쓰며, 사용자 정보는 claims와 event payload로만 전달한다.

## 읽고 나면 설명할 수 있어야 하는 것

- 브라우저 쿠키와 CSRF가 왜 gateway에만 있어야 하는가
- 서비스별 DB ownership과 bearer claims 규칙
- `comment.created.v1` 흐름과 eventual consistency
- notification-service 장애가 comment 생성과 분리되어야 하는 이유
- 운영 문서에서 target shape와 실제 검증 완료를 어떻게 구분해야 하는가

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [AWS target shape](aws-deployment.md)
- [현재 학습 노트](../notion/README.md)
