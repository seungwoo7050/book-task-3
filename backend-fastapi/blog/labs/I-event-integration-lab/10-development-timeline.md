# I-event-integration-lab 개발 타임라인

## 1. 이번 랩은 인증보다 handoff에 초점을 옮긴 상태로 시작한다

`problem/README.md`가 먼저 잡아 준 질문은 분명했다. 댓글 저장과 알림 생성이 같은 시점에 끝나지 않아도 되는 구조를 설명하고, outbox -> relay -> consumer 흐름이 실제로 이어지는지 보여 주는 것이다. 성공 기준도 정확했다. comment 생성이 outbox에 기록되고, relay 뒤에 `notification-service`가 stream을 consume하며, 같은 consume를 두 번 실행해도 중복 알림이 저장되지 않아야 한다.

이 문장을 실제 코드와 맞춰 보자마자 H 랩과의 차이가 눈에 들어왔다. compose에서 더 이상 `identity-service`를 띄우지 않는다. 대신 `workspace-service`, `notification-service`, `redis` 세 축이 올라온다. 이벤트 통합을 설명하는 랩이니, 인증 서비스까지 함께 넣어 서사를 넓히지 않겠다는 의도가 분명했다.

## 2. 런타임의 중심은 outbox와 consumer 사이의 handoff였다

`fastapi/compose.yaml`을 보면 `workspace-service`는 `REDIS_URL`, `REDIS_STREAM_NAME`을 받고, `notification-service`는 `REDIS_URL`, `REDIS_STREAM_NAME`, `REDIS_PUBSUB_CHANNEL`을 받는다. 이 시점에서 이미 관계가 정리된다.

- workspace 쪽은 event를 만들고 stream으로 넘긴다.
- notification 쪽은 stream을 읽고 자기 DB에 알림을 저장한다.
- Redis는 두 서비스 사이 handoff 지점이다.

즉, 이 랩의 질문은 "서비스를 나눌까 말까"가 아니라 "나뉜 뒤에 전달을 어디서 끊을까"로 옮겨 와 있다.

## 3. comment 저장과 outbox 적재는 같은 서비스 트랜잭션 안에 묶여 있었다

그 다음으로 본 곳은 `services/workspace-service/app/domain/services/platform.py`였다. 여기서 `create_comment()`는 task와 project, membership을 확인한 뒤 comment row를 저장한다. 그리고 같은 흐름 안에서 workspace 멤버들을 순회하며 actor를 제외한 recipient마다 `OutboxEvent`를 `queued` 상태로 적재한다.

이 구조가 중요한 이유는 comment와 outbox를 같은 DB에서 커밋한다는 점 때문이다. 알림 서비스까지 한 트랜잭션으로 묶지는 않지만, 적어도 "댓글은 저장됐는데 event가 아예 사라졌다"는 종류의 손실을 workspace 서비스 내부에서는 줄이려는 설계다. 이 랩의 eventual consistency는 comment 저장 이후부터 시작하지, comment 저장 이전부터 시작하지 않는다.

## 4. relay는 전달 완료가 아니라 stream handoff 완료를 뜻했다

`relay_outbox()`를 보면 pending outbox를 읽어 Redis `xadd()`로 stream에 넣고, 곧바로 event status를 `relayed`로 바꾼다. 이 지점에서 조금 더 조심해서 읽어야 했다.

여기서 `relayed`는 notification-service가 실제로 notification row를 저장했다는 뜻이 아니다. 그보다는 workspace-service 입장에서 "내 책임 범위인 stream handoff는 끝났다"는 뜻에 가깝다. consumer 쪽 저장 성공과는 별도 단계다.

이 경계 덕분에 설명이 선명해진다.

- comment 저장과 outbox 적재는 workspace-service의 local transaction
- Redis Stream push는 relay 단계의 handoff
- notification row 저장은 notification-service의 local transaction

세 단계를 하나의 원자적 성공처럼 포장하지 않는 것이 이 랩을 정확하게 읽는 방법이었다.

## 5. consumer는 offset 저장 대신 receipt로 중복을 흡수했다

가장 흥미로운 부분은 `services/notification-service/app/domain/services/notifications.py`였다. 이 consumer는 `xread({stream_name: "0-0"}, count=100)`으로 stream의 처음부터 읽는다. 별도 consumer group도 없고, last ID를 저장하는 로직도 없다. 처음 봤을 때는 "그러면 두 번째 consume에서 같은 이벤트를 또 읽지 않나?"라는 의문이 바로 생겼다.

답은 같은 파일과 `repositories/notifications_repository.py`, `db/models/notifications.py`에 있었다. consumer는 각 event의 `event_id`를 기준으로 먼저 `has_receipt()`를 확인한다. 이미 같은 `event_id`의 `ConsumerReceipt`가 있으면 건너뛴다. 없으면 notification row를 저장하고, 동시에 `ConsumerReceipt(event_id, event_name)`도 저장한다.

즉, 이 랩의 dedupe 전략은 offset 전진이 아니라 receipt 기록이다. consumer는 stream을 다시 읽어도 괜찮고, 중복 흡수는 애플리케이션 저장소에서 해결한다. 문제 정의가 consumer group을 일부러 제외 범위로 둔 이유도 여기서 자연스럽게 이해됐다. 이 랩은 복잡한 broker 운영보다 idempotent consumer의 핵심 아이디어를 먼저 고정하려는 단계다.

여기서 한 줄 더 줄여 써야 하는 부분도 있다. 현재 `consume()`은 `xread({stream_name: "0-0"}, count=100)`을 한 번 호출해 최대 100개 메시지만 훑는다. 즉 "receipt가 있으니 backlog 전체를 마음 편히 무한 replay해도 된다"는 식으로 쓰면 과하다. 지금 구현과 검증이 보장하는 것은 "같은 엔트리를 다시 읽어도 중복 row를 남기지 않는다"까지이고, 대량 backlog drain 정책은 별도 루프나 운영 제어 없이 자동으로 증명된 상태는 아니다.

## 6. system test도 그 아이디어에 맞춰 서술을 줄였다

`tests/test_system.py`는 이 랩의 초점 이동을 아주 직접적으로 보여 준다. 여기서는 더 이상 auth 서비스에서 토큰을 받아 오지 않는다. 테스트 안에서 JWT를 바로 서명해 owner/collaborator token을 만든다.

처음에는 이게 너무 단순해 보일 수도 있다. 하지만 실제로는 의도가 분명하다. 이 랩은 인증 경계를 재검증하려는 게 아니라, event handoff와 consumer idempotency를 검증하려는 랩이다. 그래서 system test도 그 관심사만 남기고 나머지를 걷어냈다.

테스트 흐름은 다음 순서로 진행된다.

1. owner 토큰으로 workspace 생성
2. collaborator invite/accept
3. project, task 생성
4. comment 생성
5. outbox pending 1건 확인
6. `workspace-service`에서 relay 실행
7. `notification-service`에서 consume 두 번 실행
8. 첫 consume는 `processed == 1`, 두 번째 consume는 `processed == 0`
9. collaborator 알림 목록에 실제 row 1건 저장 확인

이 시나리오는 이 랩의 질문을 거의 그대로 코드로 옮긴 셈이다.

동시에 이 시나리오가 무엇을 아직 안 보는지도 분명하다. system test는 single event handoff와 dedupe만 잠그고, 100건을 넘는 backlog batch나 반복 consume loop가 끝까지 drain되는지는 다루지 않는다.

## 7. 검증 결과는 두 층으로 나뉘었다

이번에도 명령을 다시 돌려 현재 상태를 확인했다.

`make lint`는 통과했다. 서비스 둘과 상위 tests까지 정적 검사는 깨지지 않았다.

하지만 `make test`는 통과하지 못했다. `services/workspace-service` 테스트 collection 단계에서 로컬 `python3` 환경의 `argon2` 누락 때문에 `ModuleNotFoundError: No module named 'argon2'`가 발생했다. H 랩 때와 비슷하게, 이 실패는 event integration 로직 자체보다 host Python dependency 상태에 더 가까운 문제였다.

반면 compose 기반 검증은 살아 있었다. `make smoke`는 통과했고, `python3 -m pytest tests/test_system.py -q`도 통과했다. 특히 후자는 실제로 comment -> outbox -> relay -> consume -> dedupe -> notification persistence까지 밟는 end-to-end 확인이라, 이 랩의 핵심 설계를 설명하는 데 가장 강한 근거가 됐다.

## 8. 이 랩을 지금 시점에서 어떻게 읽어야 하는가

이 랩은 분산 시스템 전체를 구현하는 단계가 아니다. consumer group도 없고, dead-letter queue도 없고, replay UI도 없다. 대신 그보다 먼저 고정해야 할 한 가지를 분명하게 보여 준다.

바로 "중복 읽기를 피하는 것"보다 "중복 읽기가 일어나도 결과를 한 번만 남기는 것"이 더 중요한 순간이 있다는 점이다.

그래서 이 랩의 정답은 다음처럼 요약된다.

- synchronous write는 workspace DB에서 끝낸다.
- asynchronous handoff는 Redis Stream으로 넘긴다.
- consumer는 여러 번 읽을 수 있다고 가정한다.
- 최종 중복 방지는 `ConsumerReceipt`로 흡수한다.

이 관점을 놓치지 않으면, J 이후의 gateway나 더 복잡한 운영 설계를 읽을 때도 기준이 흔들리지 않는다.
