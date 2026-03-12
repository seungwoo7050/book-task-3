# Problem Framing — Offline Sync Foundations

## 이 프로젝트는 어떤 질문에서 시작했나

모바일 앱에서 "오프라인에서도 동작한다"는 말을 자주 듣는다. 하지만 실제로 오프라인 상태에서 데이터를 만들고, 네트워크가 돌아왔을 때 서버와 동기화하는 과정에는 생각보다 많은 문제가 숨어 있다.

전송 실패는 어디까지 재시도할 것인가? 같은 요청을 두 번 보내면 서버가 어떻게 반응해야 하는가? 재시도해도 영원히 실패하는 요청은 어떻게 격리할 것인가? 서버가 부여한 ID와 로컬 ID는 어떻게 합칠 것인가?

이 프로젝트는 채팅 앱(`realtime-chat`)을 만들기 전에, 이런 동기화 기초 문제만 따로 꺼내서 먼저 풀어보는 **브리지 프로젝트**다. 채팅이라는 복잡한 도메인을 얹기 전에, 동기화 엔진 자체가 제대로 작동하는지를 격리된 환경에서 확인한다.

## 풀어야 했던 다섯 가지 문제

1. **Outbox queue** — 오프라인에서 생성한 mutation을 순서대로 쌓는 큐
2. **Retry와 DLQ** — 실패한 요청을 재시도하되, 일정 횟수를 넘기면 Dead Letter Queue로 분리
3. **Idempotency key** — 같은 요청이 두 번 전송되어도 서버가 한 번만 처리하도록 보장
4. **Reconnect flush** — 네트워크가 복구되면 대기 중인 큐를 일괄 전송
5. **Conflict merge** — 서버가 부여한 필드(serverId, updatedAt)를 로컬 레코드에 병합

## 명시적으로 하지 않은 것

- 실제 네트워크 요청 (모든 것은 `FakeSyncServer`로 시뮬레이션)
- UI 상의 동기화 상태 표시 (앱 shell은 상태 요약만 보여줌)
- 충돌 해결의 복잡한 케이스 (last-write-wins가 아닌 머지 전략)

## 이 과제가 학습 경로에서 차지하는 위치

이 프로젝트는 `product-systems` 그룹의 첫 번째 과제다. 여기서 다진 queue/retry/idempotency 패턴이 이후 `realtime-chat`의 pending message 모델과 `incident-ops-mobile-client`의 persistent outbox에 그대로 재사용된다.
