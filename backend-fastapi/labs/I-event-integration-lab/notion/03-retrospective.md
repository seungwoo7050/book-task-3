# 회고

## 이번 랩에서 얻은 것

- outbox를 “비동기 작업 테크닉”이 아니라 “서비스 간 handoff 경계”로 다시 보게 되었다.
- comment 저장 성공과 알림 생성 성공을 분리하면 장애 허용 범위를 더 명확하게 설명할 수 있다.
- idempotent consumer는 메시징 기술의 옵션이 아니라, 중복 전달을 전제로 설계를 바꾸는 태도에 가깝다.

## 이번 랩의 약점

- 실제 운영에서는 retry, dead letter, lag 관측이 중요하지만 이 랩은 거기까지 다루지 않는다.
- Redis Streams를 최소 형태로만 써서 운영 난이도를 축소했다.
- 알림을 사용자 화면까지 보여 주는 edge API와 websocket 전달은 아직 다음 랩의 몫이다.

## 다음 랩으로 넘기는 질문

- public API는 여전히 어떻게 안정적으로 유지할 것인가
- 브라우저 쿠키, CSRF, access token refresh는 어디에서 처리할 것인가
- 이벤트가 최종 사용자 경험으로 이어지려면 gateway는 어떤 fan-out 책임을 가져야 하는가
