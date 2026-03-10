# 문제 정의

## 문제

단일 백엔드에서 자연스럽게 함께 있던 인증과 워크스페이스 도메인을 처음으로 분리한다. 핵심 질문은 "어디서 경계를 끊어야 하며, 서비스가 서로의 DB를 읽지 않고도 동작할 수 있는가"이다.

## 성공 기준

- `identity-service`가 토큰을 발급한다.
- `workspace-service`가 그 토큰 claims만으로 workspace를 생성한다.
- 두 서비스가 각자 자기 DB만 읽고, cross-DB 조회를 하지 않는다.

## 제외 범위

- 이벤트 브로커
- edge gateway
- websocket과 실시간 전달
