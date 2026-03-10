# 지식 인덱스

## 먼저 적용할 판단 규칙

- outbox는 “이벤트를 저장하는 테이블”이 아니라 저장 성공과 전달 성공을 분리하는 계약이다.
- relay와 consumer를 분리해야 장애 위치를 설명할 수 있다.
- consume를 두 번 돌렸을 때 결과가 늘어나면 idempotency가 없는 것이다.

## 핵심 개념과 사용 조건

### `outbox`

언제 쓰는가:
- 댓글 저장은 성공해야 하지만, 이후 알림 전달은 나중에 회복되어도 될 때
- DB commit과 broker publish를 같은 원자적 사건으로 만들 수 없을 때

실패 징후:
- comment 저장 후 relay 전에 프로세스가 죽으면 무엇이 남았는지 설명할 수 없다.
- 저장은 됐는데 이벤트가 유실됐는지 확인할 수 없다.

이 랩의 근거:
- [../fastapi/services/workspace-service/app/db/models/platform.py](../fastapi/services/workspace-service/app/db/models/platform.py)
- [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)

### `relay`

왜 따로 두는가:
- outbox를 브로커로 옮기는 단계와 원본 트랜잭션을 분리해야 recovery 지점을 설명할 수 있다.
- relay를 별도 endpoint로 두면 “pending outbox -> relayed” 상태 변화를 검증하기 쉽다.

이 랩의 근거:
- [../fastapi/services/workspace-service/app/api/v1/routes/platform.py](../fastapi/services/workspace-service/app/api/v1/routes/platform.py)
- [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)

### `idempotent consumer`

언제 쓰는가:
- consumer 재기동, stream replay, drain 재시도 뒤에도 결과를 한 번만 남겨야 할 때

실패 징후:
- 같은 이벤트를 두 번 consume하면 알림이 두 건 생긴다.
- dedupe 기준이 테이블에 없어서 재처리 자체를 두려워한다.

이 랩의 근거:
- [../fastapi/services/notification-service/app/db/models/notifications.py](../fastapi/services/notification-service/app/db/models/notifications.py)
- [../fastapi/services/notification-service/app/domain/services/notifications.py](../fastapi/services/notification-service/app/domain/services/notifications.py)

### `eventual consistency`

언제 받아들여야 하는가:
- 저장 성공과 전달 성공이 같은 시점이 아니어도 되는 도메인일 때
- “지금 즉시 알림이 안 와도, recovery 후 eventually 와야 한다”는 기준이 성립할 때

이 랩의 근거:
- [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)

## 이 랩에서 제일 빨리 확인하는 순서

1. [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)에서 comment 생성 후 pending outbox가 1이 되는지 본다.
2. 같은 테스트에서 relay 1회, consume 2회를 보고 두 번째 consume 결과가 0인지 확인한다.
3. [../fastapi/services/notification-service/app/db/models/notifications.py](../fastapi/services/notification-service/app/db/models/notifications.py)에서 `consumer_receipts` 존재 이유를 본다.

## 실패 징후와 먼저 의심할 것

| 징후 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| 댓글은 있는데 알림이 없다 | outbox, relay | 저장 성공과 전달 성공이 분리돼 있기 때문이다 |
| consume를 두 번 했더니 알림이 두 개다 | idempotent consumer | receipt 또는 dedupe 키가 약하다 |
| relay를 브로커 publish와 같은 함수에서 바로 처리하고 싶다 | outbox 경계 약화 | recovery 지점을 잃는다 |

## 참고 자료

- 제목: `labs/E-async-jobs-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 비동기 작업과 이벤트 전달의 차이를 다시 정리하기 위해 읽었다.
  - 배운 점: job queue와 domain event는 목적이 다르며, I 랩은 후자에 더 가깝다.
  - 반영 결과: problem framing과 approach log의 범위 설명에 반영했다.
- 제목: `labs/I-event-integration-lab/fastapi/tests/test_system.py`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: relay 1회와 consume 2회가 실제로 무엇을 증명하는지 기록하기 위해 확인했다.
  - 배운 점: dedupe는 “두 번째 consume이 성공해도 결과가 늘지 않는다”로 가장 쉽게 설명된다.
  - 반영 결과: `05-development-timeline.md`와 debug log에 반영했다.
