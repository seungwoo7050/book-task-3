# Replay And Ack

- client message는 `clientId`로 먼저 생성된다.
- 서버 ack가 오면 `serverId`를 채우고 status를 `sent`로 바꾼다.
- reconnect 후 replay는 `eventId > lastEventId`만 적용한다.
- replay 대상 이벤트는 `serverId` 또는 `eventId` 기준으로 dedupe한다.
