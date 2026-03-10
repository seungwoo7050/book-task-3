# Approach Log — Realtime Chat

## 첫 번째 결정: 메시지 모델을 어떻게 설계할 것인가

처음에는 메시지를 단순한 `{ text, sender, timestamp }` 객체로 잡으려 했다.
하지만 pending 상태를 표현하려면 `serverId`가 null일 수 있어야 하고, status 필드가 필요했다.

결국 `MessageRecord`에는 `clientId`(로컬 생성 시 부여), `serverId`(서버 ack 후 채워짐), `status`('pending' | 'sent') 세 가지 identity 관련 필드가 들어갔다. 이 구조 덕분에 "아직 서버가 모르는 메시지"와 "서버가 확인한 메시지"를 하나의 배열에서 자연스럽게 섞어 보여줄 수 있었다.

## 두 번째 결정: Ack reconciliation을 어떻게 할 것인가

서버에서 `{ clientId, serverId }` 형태의 ack가 오면, 배열을 순회하면서 `clientId`가 일치하는 메시지를 찾아 `serverId`를 채우고 status를 `sent`로 바꾸는 방식을 택했다.

다른 선택지로는 Map 기반 lookup이 있었지만, 이 프로젝트에서는 메시지 수가 학습 범위 안에서 제한적이므로 배열 순회로 충분했다. 중요한 건 구조가 아니라 "ack가 도착하면 정확히 어떤 레코드가 어떻게 바뀌는가"를 테스트로 증명하는 것이었다.

## 세 번째 결정: Replay 필터링 기준 — eventId vs. serverId

재연결 후 서버가 보내는 replay 이벤트를 걸러내는 기준이 두 가지 있었다.

1. `eventId > lastEventId`로 시간순 필터링
2. `serverId` 기준 중복 제거 (dedupe)

둘 다 필요하다는 결론에 도달했다. `lastEventId` 필터는 "이미 본 범위"를 빠르게 잘라내고, `serverId` dedupe는 같은 메시지가 두 번 들어오는 edge case를 막는다. 이 두 단계를 별개 함수(`applyReplayEvents`, `dedupeReplay`)로 분리해서 각각 독립적으로 테스트할 수 있게 했다.

## 네 번째 결정: Typing/Presence를 어디에 둘 것인가

타이핑 상태는 메시지와 근본적으로 다르다. 저장할 필요가 없고, 수초 내에 사라지며, 서버 ack도 필요 없다.
그래서 WatermelonDB 스키마에 넣지 않고, 단순한 `Record<string, boolean>` 인메모리 상태로 분리했다.

이 분리가 중요했던 이유는, 만약 typing 상태를 DB에 넣으면 쓸데없는 write가 발생하고, replay 시에도 typing 이벤트를 영속 데이터처럼 처리해야 하는 혼란이 생기기 때문이다.

## 다섯 번째 결정: WatermelonDB 스키마 정의

로컬 영속성에는 WatermelonDB를 선택했다. React Native 생태계에서 SQLite 기반 동기화를 가장 직관적으로 제공하는 라이브러리이기 때문이다. 스키마에는 `messages` 테이블 하나만 정의했고, 컬럼은 소스코드의 `MessageRecord` 인터페이스와 1:1로 대응하게 설계했다.

version을 1에서 시작한 이유는, 이후 스키마 마이그레이션을 학습할 여지를 남기기 위해서다.
